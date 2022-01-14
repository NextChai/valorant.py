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

from typing import TYPE_CHECKING, Tuple, Optional

from .abc import Hashable

if TYPE_CHECKING:
    from .types.dto import AccountDto as AccountDtoPayload
    from .state import ConnectionState
    

class AccountDto(Hashable):
    """
    Represents a valorant account.
    """
    
    __slots__: Tuple[str, ...] = (
        '_original',
        '_state',
        'puuid',
        'game_name',
        'tag_line'
    )
    
    def __init__(self, *, data: AccountDtoPayload, state: ConnectionState) -> None:
        self._original: AccountDtoPayload = data
        self._state: ConnectionState = state
        
        self._from_data(data=data)
        
    def _from_data(self, *, data: AccountDtoPayload) -> None:
        self.puuid: str = data['puuid']
        self.game_name: Optional[str] = data.get('gameName')
        self.tag_line: Optional[str] = data.get('tagLine')
        
    async def fetch_matchlists(self):
        raise NotImplementedError
    
    
        
        