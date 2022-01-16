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

from typing import TYPE_CHECKING, Any, Callable, Dict, Generic, Optional, Tuple, TypeVar, TypedDict, Union, Type

from .agent import Agent
from .buddy import Buddy, BuddyLevel
from .ceremony import Ceremony

if TYPE_CHECKING:
    from .http import HTTPClient
    from .client import ValorantClient
    
    from .types.agent import Agent as AgentPayload
    from .types.buddy import Buddy as BuddyPayload, BuddyLevel as BuddyLevelPayload
    from .types.ceremony import Ceremony as CeremonyPayload
    
    
CSO = TypeVar('CSO', bound='Union[HTTPClient, ValorantClient]')
T = TypeVar('T')


# Although this is a bit hacky, it will save me from
# writing hundreds of lines of code, all I will have to do
# to make pyright happy is specify the callable in the 
# type checking part of ConnectionState.
def cache_management_for(
    instance: ConnectionState[CSO], 
    var_name: str,
    function_name: str,
    type: Type[T] # type: ignore
):
    setattr(instance, var_name, {})
    
    def _get_cache(uuid: str) -> Optional[T]:
        return getattr(instance, var_name).get(uuid)

    def _remove_cache(uuid: str) -> Optional[T]:
        return getattr(instance, var_name).pop(uuid, None)
    
    def _store_cache(data) -> T:
        try:
            return getattr(instance, var_name)[data['uuid']]
        except KeyError:
            new = type(data=data, state=instance)
            getattr(instance, var_name)[new.uuid] = new
            return new
        
    setattr(instance, f'_get_{function_name}', _get_cache)
    setattr(instance, f'_remove_{function_name}', _remove_cache)
    setattr(instance, f'_store_{function_name}', _store_cache)
    

class ConnectionState(Generic[CSO]):
    if TYPE_CHECKING:
        _store_agent: Callable[[AgentPayload], Agent]
        _store_buddy_level: Callable[[BuddyLevelPayload], BuddyLevel]
        _store_ceremony: Callable[[CeremonyPayload], Ceremony]
    
    def __init__(self, dispatch: Callable[..., Any]) -> None:
        self.dispatch: Callable[..., Any] = dispatch
        self._load_cache()
        
        cache_management_for(self, '_agents', 'agent', Agent)
        cache_management_for(self, '_buddies', 'buddy', Buddy)
        cache_management_for(self, '_buddy_levels', 'buddy_level', BuddyLevel)
        cache_management_for(self, '_ceremonies', 'ceremony', Ceremony)
        
    def _load_cache(self) -> None:
        self._agents: Dict[str, Agent] = {}
        self._buddies: Dict[str, Buddy] = {}
        self._buddy_levels: Dict[str, BuddyLevel] = {}
        
    def _clear_cache(self) -> None:
        self._agents = {}
        self._buddies = {}
        self._buddy_levels = {}

    def _store_buddy(self, data: BuddyPayload) -> Buddy:
        try:
            return self._buddies[data['uuid']]
        except KeyError:
            buddy = Buddy(data=data, state=self)
            self._buddies[buddy.uuid] = buddy
            
            if buddy.levels:
                for level in buddy.levels:
                    if level.uuid not in self._buddy_levels:
                        self._buddy_levels[level.uuid] = level

            return buddy