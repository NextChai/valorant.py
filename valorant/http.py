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
import asyncio
import aiohttp
import weakref
from urllib.parse import quote as _uriquote

from typing import (
    TYPE_CHECKING, 
    Tuple, 
    Union, 
    Any, 
    Optional,
    TypeVar, 
    Coroutine,
    Type,
    Dict,
    Callable
)
from types import TracebackType

from . import __version__
from .utils import _to_json, MISSING, _mis_if_not, json_or_text
from .enums import PlatformRouting
from .errors import *

if TYPE_CHECKING:
    from aiohttp import ClientSession
    
    from .types import (
        dto,
    )
    
    T = TypeVar('T')
    BE = TypeVar('BE', bound=BaseException)
    MU = TypeVar('MU', bound='MaybeUnlock')
    Response = Coroutine[Any, Any, T]
    
log = logging.getLogger('valorant.http')
    

__all__: Tuple[str, ...] = (
    'Route',
    'MaybeUnlock',
)
 

# https://github.com/NextChai/chai-discord.py/blob/master/discord/http.py#L113-L122
class Route:
    __slots__: Tuple[str, ...] = (
        'method',
        'path',
        'BASE',
        '_original_parameters',
        'url',
        '_url'
    )
    
    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.method: str = method
        self.path: str = path
        self.BASE: str = PlatformRouting.na.value # Base is here so we can update it
        
        self._original_parameters: Any = parameters
        self._url: Optional[str] = None
        self.url: str = self._make_url()
        
    @property
    def bucket(self) -> str:
        # Unlike dpy, we don't have channel, guild, or webhook ids to use so we'll just use path
        return self.path
    
    def _make_url(self) -> str:
        if self._url:
            return self._url
        
        url = self.BASE + self.path
        if self._original_parameters:
            url = url.format_map({k: _uriquote(v) if isinstance(v, str) else v for k, v in self._original_parameters.copy().items()})
        
        self._url = url
        return url
    
    def _update_base(self, base: PlatformRouting) -> None:
        # Internally updates the base in case the user does not want to use na1
        self.BASE = base.value
        self._url = None
        
# https://github.com/NextChai/chai-discord.py/blob/master/discord/http.py#L136-L154   
class MaybeUnlock:
    def __init__(self, lock: asyncio.Lock) -> None:
        self.lock: asyncio.Lock = lock
        self._unlock: bool = True

    def __enter__(self: MU) -> MU:
        return self

    def defer(self) -> None:
        self._unlock = False

    def __exit__(
        self,
        exc_type: Optional[Type[BE]],
        exc: Optional[BE],
        traceback: Optional[TracebackType],
    ) -> None:
        if self._unlock:
            self.lock.release()
            
            
class HTTPClient:
    __slots__: Tuple[str, ...] = (
        '__session',
        '_locks',
        '_global_over',
        'loop',
        '_base_override',
        'token',
        'user_agent',
        'dispatch'
    )
    
    def __init__(
        self, 
        token: str,
        loop: asyncio.AbstractEventLoop,
        dispatch: Callable[..., None],
        *,
        session: Optional[ClientSession] = MISSING, 
        base_override: Optional[PlatformRouting] = MISSING,
    ) -> None:
        self.__session: ClientSession = _mis_if_not(session) or aiohttp.ClientSession() # type: ignore
        self._locks: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
        self._global_over: asyncio.Event = asyncio.Event()
        self._global_over.set()
        self.loop: asyncio.AbstractEventLoop = loop
        self._base_override: Optional[PlatformRouting] = _mis_if_not(base_override)
        self.dispatch: Callable[..., None] = dispatch
        
        self.token: str = token
        
        user_agent = 'valorantpy/{} (https://github.com/NextChai/valorantpy) (Python/{}; aiohttp/{})'
        self.user_agent: str = user_agent.format(__version__, sys.version_info, aiohttp.__version__)
        
    # Basically just https://github.com/NextChai/chai-discord.py/blob/master/discord/http.py#L210-L355
    async def request(
        self,
        route: Route,
        **kwargs: Any
    ) -> Any:
        method = route.method
        bucket = route.bucket
        
        if (override := kwargs.pop('base_override', None)):
            route._update_base(override)
            url = route._make_url()
        else:
            if self._base_override is not None and self._base_override is not PlatformRouting.na1:
                route._update_base(self._base_override)
                url = route._make_url()
            else:
                url = route.url
    
        lock = self._locks.get(bucket)
        if lock is None:
            lock = asyncio.Lock()
            if bucket is not None:
                self._locks[bucket] = lock

        # header creation
        headers: Dict[str, str] = {
            'User-Agent': self.user_agent,
            'X-Riot-Token': self.token
        }
        
        # some checking if it's a JSON request
        if 'json' in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['data'] = _to_json(kwargs.pop('json'))
        
        kwargs['headers'] = headers
        
        if not self._global_over.is_set():
            # wait until the global lock is complete
            await self._global_over.wait()
            
        response: Optional[aiohttp.ClientResponse] = None
        data: Optional[Union[Dict[str, Any], str]] = None
        await lock.acquire()
        
        with MaybeUnlock(lock) as maybe_lock:
            for tries in range(5):
                try:
                    self.dispatch('request', method, url, bucket, kwargs)
                    async with self.__session.request(method, url, **kwargs) as response:
                        log.debug('%s %s with %s has returned %s', method, url, kwargs.get('data'), response.status)
                        
                        data = await json_or_text(response)
                        
                        if 300 > response.status >= 200:
                            log.debug('%s %s has received %s', method, url, data)
                            return data
                        
                        # we are being rate limited
                        if response.status == 429:
                            if not response.headers.get('Via') or isinstance(data, str):
                                # Banned by Cloudflare more than likely.
                                raise HTTPException(response, data)

                            fmt = 'We are being rate limited. Retrying in %.2f seconds. Handled under the bucket "%s"'
                            log.debug(f'Got rate limited! %s', data)
                            
                            continue

                        # we've received a 500, 502, or 504, unconditional retry
                        if response.status in {500, 502, 504}:
                            await asyncio.sleep(1 + tries * 2)
                            continue

                        # the usual error cases
                        if response.status == 403:
                            raise Forbidden(response, data)
                        elif response.status == 404:
                            raise NotFound(response, data)
                        elif response.status >= 500:
                            raise InternalServerError(response, data)
                        else:
                            raise HTTPException(response, data)
                
                # This is handling exceptions from the request
                except OSError as e:
                    # Connection reset by peer
                    if tries < 4 and e.errno in (54, 10054):
                        await asyncio.sleep(1 + tries * 2)
                        continue
                    raise
                
            if response is not None:
                # We've run out of retries, raise.
                if response.status >= 500:
                    raise InternalServerError(response, data)

                raise HTTPException(response, data)
            
            raise RuntimeError('Unreachable code in HTTP handling')
        
    def get_account_by_puuid(self, puuid: str, **kwargs) -> Response[dto.AccountDto]:
        r = Route('GET', '/riot/account/v1/accounts/by-puuid/{puuid}', puuid=puuid)
        return self.request(r, **kwargs)
    
    def get_account_by_riot_id(self, game_name: str, tag_line: str, **kwargs) -> Response[dto.AccountDto]:
        r = Route('GET', '/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}', game_name=game_name, tag_line=tag_line)
        return self.request(r, **kwargs)
    
    def get_account_me(self, **kwargs) -> Response[dto.AccountDto]:
        r = Route('GET', '/riot/account/v1/accounts/me')
        return self.request(r, **kwargs)
    
    def get_active_shards_by_name(self, game: str, puuid: str) -> Response[dto.ActiveShardDto]:
        r = Route('GET', '/riot/account/v1/active-shards/by-game/{game}/by-puuid/{puuid}', game=game, puuid=puuid)
        return self.request(r)

    def get_contents(self) -> Response[dto.ContentDto]:
        r = Route('GET', '/val/content/v1/contents')
        return self.request(r)
    
    def get_match_from_id(self, match_id: str) -> Response[dto.MatchDto]:
        r = Route('GET', '/val/match/v1/matches/{match_id}', match_id=match_id)
        return self.request(r)

    def get_matchlists_from_puuid(self, puuid: str) -> Response[dto.MatchlistDto]:
        r = Route('GET', '/val/match/v1/matchlists/by-puuid/{puuid}', puuid=puuid)
        return self.request(r)
    
    def get_recent_matches_by_queue(self, queue: str) -> Response[dto.RecentMatchesDto]:
        r = Route('GET', '/val/match/v1/recent-matches/by-queue/{queue}', queue=queue)
        return self.request(r)
    
    def get_leaderboards_by_act(self, act_id: str) -> Response[dto.LeaderboardDto]:
        r = Route('GET', '/val/ranked/v1/leaderboards/by-act/{act_id}', act_id=act_id)
        return self.request(r)
    
    def get_platform_data(self) -> Response[dto.PlatformDataDto]:
        r = Route('GET', '/val/status/v1/platform-data')
        return self.request(r)
    