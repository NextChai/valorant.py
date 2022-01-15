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

from typing import TYPE_CHECKING, Optional, Tuple, List

from .abc import Hashable
from .media import Icon

if TYPE_CHECKING:
    from .types.buddy import (
        Buddy as BuddyPayload,
        BuddyLevel as BuddyLevelPayload
    )
    from .state import ConnectionState
    

__all__: Tuple[str, ...] = (
    'BuddyLevel',
    'Buddy'
)   
    
    
class BuddyLevel(Hashable):
    """
    Represents a buddy level to a :class:`Buddy`.
    
    Attributes
    ----------
    uuid: :class:`str`
        The unique identifier of the buddy level.
    charm_level: :class:`int`
        The nnumber of the level of the buddy.
    display_name: :class:`str`
        The display name of the buddy level.
    display_icon: Optional[:class:`Icon`]
        The display icon of the buddy level, if any.
    asset_path: :class:`str`
        The asset path to the buddy level.
    """
    __slots__: Tuple[str, ...] = (
        'uuid', 
        'charm_level',
        'display_name', 
        'display_icon', 
        'asset_path'
    )
    
    def __init__(self, *, data: BuddyLevelPayload, state: ConnectionState) -> None:
        self.uuid: str = data['uuid']
        self.charm_level: int = data['charmLevel']
        self.display_name: str = data['displayName']
        self.display_icon: Optional[Icon] = Icon._from_url(icon) if (icon := data['displayIcon']) else None
        self.asset_path: str = data['assetPath']


class Buddy(Hashable):
    """
    Represents a weapon buddy.
    
    Attributes
    ----------
    uuid: :class:`str`
        The unique identifier of the buddy.
    display_name: :class:`str`
        The display name of the buddy.
    is_hidden_if_not_owned: :class:`bool`
        Whether the buddy is hidden if not owned.
    theme_uuid: :class:`str`
        The unique identifier of the buddy theme.
    display_icon: Optional[:class:`Icon`]
        The display icon of the buddy, if any.
    asset_path: :class:`str`
        The asset path to the buddy.
    levels: :class:`List[BuddyLevel]`
        The levels that the buddy has.
    """
    __slots__: Tuple[str, ...] = (
        'uuid', 
        'display_name', 
        'is_hidden_if_not_owned', 
        'theme_uuid',
        'display_icon',
        'asset_path',
        'levels'
    )

    def __init__(self, *, data: BuddyPayload, state: ConnectionState) -> None:
        self.uuid: str = data['uuid']
        self.display_name: str = data['displayName']
        self.is_hidden_if_not_owned: bool = data['isHiddenIfNotOwned']
        self.theme_uuid: str = data['themeUuid']
        self.display_icon: Optional[Icon] = Icon._from_url(icon) if (icon := data['displayIcon']) else None
        self.asset_path: str = data['assetPath']
        self.levels: List[BuddyLevel] = [BuddyLevel(data=level, state=state) for level in data['levels']]
        