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

from typing import TYPE_CHECKING, Tuple

from .abc import Hashable

if TYPE_CHECKING:
    from types.ceremony import Ceremony as CeremonyPayload
    from .state import ConnectionState

__all__: Tuple[str, ...] = (
    'Ceremony',
)
 
class Ceremony(Hashable):
    """
    Represents a Ceremony.
    
    Attributes
    ----------
    uuid: :class:`str`
        The UUID of the Ceremony.
    display_name: :class:`str`
        The display name of the Ceremony.
    asset_path: :class:`str`
        The asset path of the Ceremony.
    """
    __slots__: Tuple[str, ...] = (
        'uuid', 
        'display_name',
        'asset_path'
    )
    
    def __init__(self, *, data: CeremonyPayload, state: ConnectionState) -> None:
        self.uuid: str = data['uuid']
        self.display_name: str = data['displayName']
        self.asset_path: str = data['assetPath']