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


from .http import HTTPClient
from .utils import MISSING
from .state import ConnectionState

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from asyncio import AbstractEventLoop
    
    from .agent import Agent
    from .enums import Language
    from .buddy import Buddy, BuddyLevel
    from .ceremony import Ceremony

log = logging.getLogger('valorant.client')


class ValorantClient:
    """
    The main Valorant Client.
    
    Attributes
    ----------
    loop: :class:`asyncio.AbstractEventLoop`
        The event loop the client is currently using.
    """
    
    def __init__(
        self, 
        token: str,
        *,
        session: Optional[ClientSession] = MISSING,
        loop: Optional[AbstractEventLoop] = MISSING,
    ) -> None:
        self.loop = loop = loop or asyncio.get_event_loop()
        self.http: HTTPClient = HTTPClient(token, loop, self.dispatch, session=session)
        self._connection: ConnectionState = ConnectionState(dispatch=self.dispatch) 
        
        self._listeners: Dict[str, List[Tuple[asyncio.Future, Callable[..., bool]]]] = {}
        
    # Listeners
    def event(self, coro: Coroutine[Any, Any, Any]) -> Coroutine[Any, Any, Any]:
        """
        Used to register a coroutine to be called when an event is received.
        
        Parameters
        ----------
        coro: Coroutine[Any, Any, Any]
            The coroutine to register.
            
        Returns
        --------
        coro: Coroutine[Any, Any, Any]
            The registered coroutine.
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('event registered must be a coroutine function')

        setattr(self, coro.__name__, coro)
        log.debug('%s has successfully been registered as an event', coro.__name__)
        return coro
    
    def wait_for(
        self,
        event: str,
        *,
        check: Optional[Callable[..., bool]] = MISSING,
        timeout: Optional[float] = MISSING,
    ) -> Awaitable[asyncio.Future[Any]]:
        """
        Used to wait for a specific event to be called.
        
        Parameters
        ----------
        event: :class:`str`
            The event to wait for.
        check: Optional[:class:`Callable[..., bool]`]
            A predicate to check if the the future should resolve.
        timeout: Optional[:class:`float`]
            A max amount of time to wait.
        
        Returns
        -------
        :class:`asyncio.Future`
            The future to await. The future will resolve with the arguments of the event
            you are waiting for.
        """
        future = self.loop.create_future()
        if check is MISSING:
            def _check(*args):
                return True
            check = _check
            
        if timeout is MISSING:
            timeout = None

        ev = event.lower()
        try:
            listeners = self._listeners[ev]
        except KeyError:
            listeners = []
            self._listeners[ev] = listeners

        listeners.append((future, check)) # type: ignore
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
    
    def _schedule_event(self, coro: Callable[..., Coroutine[Any, Any, Any]], event_name: str, *args: Any, **kwargs: Any) -> asyncio.Task:
        wrapped = self._run_event(coro, event_name, *args, **kwargs)
        return asyncio.create_task(wrapped, name=f'valorantpy: {event_name}')
    
    def dispatch(self, event: str, *args, **kwargs) -> None:
        """
        Used to dispatch all events and listeners to their respective handlers.
        
        Original source for this can be found here: https://github.com/NextChai/chai-discord.py/blob/master/discord/http.py#L210-L355
        
        Parameters
        ----------
        event: :class:`str`
            The event to dispatch.
        *args: Any
            The arguments to pass to the event.
        **kwargs: Any
            The keyword arguments to pass to the event.
        """
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
    
    # Methods
    async def fetch_agents(self, *, language: Optional[Language] = MISSING, is_playable_character: Optional[bool] = MISSING) -> List[Agent]:
        """|coro|
        
        Fetch all agents.
        
        Parameters
        ----------
        language: Optional[:class:`Language`]
            The language you wish to fetch agents in.
        is_playable_character: Optional[:class:`bool`]
            Whether or not you wish to fetch playable characters.
        
        Returns
        -------
        List[:class:`Agent`]
            A list of agents.
        """
        agents_data = await self.http.get_agents(language=language, is_playable_character=is_playable_character)    
        return list(map(self._connection._store_agent, agents_data))

    async def fetch_agent(self, uuid: str, *, language: Optional[Language] = MISSING) -> Agent:
        """|coro|
        
        Used to fetch an agent.
        
        Parameters
        ----------
        uuid: :class:`str`
            The UUID of the agent you wish to fetch.
        language: Optional[:class:`Language`]
            The language you wish to fetch the agent in.
        """
        agent_data = await self.http.get_agent(uuid, language=language)
        return self._connection._store_agent(agent_data)
    
    async def fetch_buddies(self, *, language: Optional[Language] = MISSING) -> List[Buddy]:
        """|coro|
        
        Used to fetch all buddies.
        
        Paramerers
        ----------
        language: Optional[:class:`Language`]
            The language you wish to fetch the buddy in.
        
        Returns
        -------
        List[:class:`Buddy`]
            A list of buddies.
        """
        buddies_data = await self.http.get_buddies(language=language)
        return list(map(self._connection._store_buddy, buddies_data))
    
    async def fetch_buddy(self, uuid: str, *, language: Optional[Language] = MISSING) -> Buddy:
        """|coro|
        
        Used to fetch a buddy from it's uuid.
        
        Parameters
        ----------
        uuid: :class:`str`
            The UUID of the buddy you wish to fetch.
        language: Optional[:class:`Language`]
            The language you wish to fetch the buddy in.
            
        Returns
        -------
        :class:`Buddy`
            The buddy that was fetched,
        """
        buddy_data = await self.http.get_buddy(uuid, language=language)
        return self._connection._store_buddy(buddy_data)
    
    async def fetch_buddy_levels(self, *, language: Optional[Language] = MISSING) -> List[BuddyLevel]:
        """|coro|
        
        Used to fetch all buddy levels.
        
        Parameters
        ----------
        language: Optional[:class:`Language`]
            The language you wish to fetch the buddy level in.
            
        Returns
        -------
        List[:class:`BuddyLevel`]
            A list of buddy levels.
        """
        buddy_levels_data = await self.http.get_buddy_levels(language=language)
        return list(map(self._connection._store_buddy_level, buddy_levels_data))
    
    async def fetch_buddy_level(self, uuid: str, *, language: Optional[Language] = MISSING) -> BuddyLevel:
        """|coro|
        
        Used to fetch a buddy level by it's uuid.
        
        Parameters
        ----------
        uuid: :class:`str`
            The UUID of the buddy level you wish to fetch.
        language: Optional[:class:`Language`]
            The language you wish to fetch the buddy level in.
            
        Returns
        -------
        :class:`BuddyLevel`
            The requested buddy level.
        """
        buddy_level_data = await self.http.get_buddy_level(uuid, language=language)
        return self._connection._store_buddy_level(buddy_level_data)
    
    async def fetch_ceremonies(self, *, language: Optional[Language] = MISSING) -> List[Ceremony]:
        """|coro|
        
        Used to fetch all ceremonies that are available.
        
        Parameters
        ----------
        language: Optional[:class:`Language`]
            The language you wish to fetch the ceremony in.
            
        Returns
        -------
        List[:class:`Ceremony`]
            A list of ceremonies.
        """
        ceremonies_data = await self.http.get_ceremonies(language=language)
        return list(map(self._connection._store_ceremony, ceremonies_data))
        
    async def fetch_ceremony(self, uuid: str, *, language: Optional[Language] = MISSING) -> Ceremony:
        """|coro|
        
        Used to fetch a ceremony by it's uuid.
        
        Parameters
        ----------
        uuid: :class:`str`
            The UUID of the ceremony you wish to fetch.
        language: Optional[:class:`Language`]
            The language you wish to fetch the ceremony in.
            
        Returns
        -------
        :class:`Ceremony`
            The requested ceremony.
        """
        ceremony_data = await self.http.get_ceremony(uuid, language=language)
        return self._connection._store_ceremony(ceremony_data)
    
    