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

from typing import TYPE_CHECKING, Any, Callable, Dict, Generic, Optional, Tuple, TypeVar, Union

from .account import AccountDto

if TYPE_CHECKING:
    from .http import HTTPClient
    from .client import ValorantClient
    
CSO = TypeVar('CSO', bound='Union[HTTPClient, ValorantClient]')


class ConnectionState(Generic[CSO]):
    __slots__: Tuple[str, ...] = (
        'dispatch',
    )
    
    def __init__(self, dispatch: Callable[..., Any]) -> None:
        self.dispatch: Callable[..., Any] = dispatch
        #self._load_cache()
        
    #def _load_cache(self) -> None:
    #    self._accounts: Dict[str, AccountDto] = {}
    #    
    #def _clear_cache(self) -> None:
    #    self._accounts = {}
    #
    #def _store_account(self, data: AccountDtoPayload) -> AccountDto:
    #    account = AccountDto(data=data, state=self)
    #    self._accounts[account.puuid] = account
    #    
    #    if not self.optimized:
    #        self.dispatch('cache_entry', account)
    #    
    #    return account
    #
    #def _get_account(self, puuid: str) -> Optional[AccountDto]:
    #    return self._accounts.get(puuid)
    #
    #def _remove_account(self, puuid: str) -> Optional[AccountDto]:
    #    return self._accounts.pop(puuid, None)
    