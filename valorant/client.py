"""
MIT License

Copyright (c) 2022 NextChai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import annotations

import sys
import logging
import traceback
import asyncio
from typing import TYPE_CHECKING, Optional, List, Dict, Callable, Tuple, Coroutine, Any, Awaitable

from valorant.state import ConnectionState

from .http import HTTPClient
from .utils import MISSING, _mis_if_not
from .enums import PlatformRouting
from .account import AccountDto

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from asyncio import AbstractEventLoop

log = logging.getLogger('valorant.client')


class ValorantClient:
    """
    
    """
    
    def __init__(
        self, 
        token: str,
        *,
        session: Optional[ClientSession] = MISSING,
        loop: Optional[AbstractEventLoop] = MISSING,
        base_override: Optional[PlatformRouting] = MISSING,
        optimized: Optional[bool] = MISSING
    ) -> None:
        self.optimized: bool = _mis_if_not(optimized, False) # type: ignore
        
        self.loop = loop = loop or asyncio.get_event_loop()
        self.http: HTTPClient = HTTPClient(token, loop, self.dispatch, session=session, base_override=base_override)
        self._connection: ConnectionState = ConnectionState(dispatch=self.dispatch, optimized=optimized) # type: ignore
        
        self._listeners: Dict[str, List[Tuple[asyncio.Future, Callable[..., bool]]]] = {}
        self.user: Optional[AccountDto] = None
        
    # Listeners
    def event(self, coro: Coroutine[Any, Any, Any]) -> Coroutine[Any, Any, Any]:
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('event registered must be a coroutine function')

        setattr(self, coro.__name__, coro)
        log.debug('%s has successfully been registered as an event', coro.__name__)
        return coro
    
    def wait_for(
        self,
        event: str,
        *,
        check: Optional[Callable[..., bool]] = None,
        timeout: Optional[float] = None,
    ) -> Awaitable[asyncio.Future[Any]]:
        future = self.loop.create_future()
        if check is None:
            def _check(*args):
                return True
            check = _check

        ev = event.lower()
        try:
            listeners = self._listeners[ev]
        except KeyError:
            listeners = []
            self._listeners[ev] = listeners

        listeners.append((future, check))
        return asyncio.wait_for(future, timeout)
            
    async def on_error(self, event_method: str, *args: Any, **kwargs: Any) -> None:
        """|coro|
        
        The default error handler provided by the client. By default this prints to :data:`sys.stderr`
        however it could be overridden to have a different implementation.
        
        Check :func:`~discord.on_error` for more details.
        """
        print(f'Ignoring exception in {event_method}', file=sys.stderr)
        traceback.print_exc()
        
    # Internal helpers
    
    # https://github.com/NextChai/chai-discord.py/blob/master/discord/client.py#L352-L361
    async def _run_event(self, coro: Callable[..., Coroutine[Any, Any, Any]], event_name: str, *args: Any, **kwargs: Any) -> None:
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception:
            try:
                await self.on_error(event_name, *args, **kwargs)
            except asyncio.CancelledError:
                pass
    
    # https://github.com/NextChai/chai-discord.py/blob/master/discord/client.py#L363-L366     
    def _schedule_event(self, coro: Callable[..., Coroutine[Any, Any, Any]], event_name: str, *args: Any, **kwargs: Any) -> asyncio.Task:
        wrapped = self._run_event(coro, event_name, *args, **kwargs)
        return asyncio.create_task(wrapped, name=f'valorantpy: {event_name}')
    
    # https://github.com/NextChai/chai-discord.py/blob/master/discord/http.py#L210-L355
    def dispatch(self, event: str, *args, **kwargs) -> None:
        log.debug('Dispatching event %s', event)
        method = f'on_{event}'
        
        listeners = self._listeners.get(event)
        if listeners:
            removed = []
            for i, (future, condition) in enumerate(listeners):
                if future.cancelled():
                    removed.append(i)
                    continue

                try:
                    result = condition(*args)
                except Exception as exc:
                    future.set_exception(exc)
                    removed.append(i)
                else:
                    if result:
                        if len(args) == 0:
                            future.set_result(None)
                        elif len(args) == 1:
                            future.set_result(args[0])
                        else:
                            future.set_result(args)
                        removed.append(i)

            if len(removed) == len(listeners):
                self._listeners.pop(event)
            else:
                for idx in reversed(removed):
                    del listeners[idx]

        try:
            coro = getattr(self, method)
        except AttributeError:
            pass
        else:
            self._schedule_event(coro, method, *args, **kwargs)
    
    async def fetch_account_by_puuid(self, puuid: str) -> AccountDto:
        account = self._connection._get_account(puuid)
        if account:
            return account
            
        data = await self.http.get_account_by_puuid(puuid, base_override=PlatformRouting.americas)
        return self._connection._store_account(data)
    
    async def fetch_account_by_riot_id(self, game_name: str, riot_id: str) -> AccountDto:
        data = await self.http.get_account_by_riot_id(game_name, riot_id, base_override=PlatformRouting.americas)
        return self._connection._store_account(data)
    
    async def fetch_client_user(self) -> AccountDto:
        if self.user:
            return self.user
        
        data = await self.http.get_account_me()
        return self._connection._store_account(data)
    
    