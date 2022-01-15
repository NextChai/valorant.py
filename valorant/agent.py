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

from typing import TYPE_CHECKING, List, Tuple

from .abc import Hashable
from .media import Icon

if TYPE_CHECKING:
    from .types.agent import (
        Agent as AgentPayload,
        AgentRole as AgentRolePayload,
        AgentAbility as AgentAbilityPayload,
        AgentVoiceLine as AgentVoiceLinePayload,
        AgentMedia as AgentMediaPayload
    )
    from .state import ConnectionState
    
__all__: Tuple[str, ...] = (
    'AgentMedia',
    'AgentVoiceLine',
    'AgentAbility',
    'AgentRole',
    'Agent'
)


class AgentMedia(Hashable):
    __slots__: Tuple[str, ...] = (
        'id',
        'wwise',
        'wave'
    )
    
    def __init__(self, *, data: AgentMediaPayload, state: ConnectionState) -> None:
        self.id: int = data['id']
        self.wwise: str = data['wwise']
        self.wave: str = data['wave']


class AgentVoiceLine:
    __slots__: Tuple[str, ...] = (
        'min_duration', 
        'max_duration', 
        'media'
    )
    
    def __init__(self, *, data: AgentVoiceLinePayload, state: ConnectionState) -> None:
        self.min_duration: float = data['minDuration']
        self.max_duration: float = data['maxDuration']
        self.media: List[AgentMedia] = [AgentMedia(data=m, state=state) for m in data['mediaList']]


class AgentAbility:
    __slots__: Tuple[str, ...] = (
        'slot', 
        'display_name', 
        'description', 
        'display_icon'
    )
    
    def __init__(self, *, data: AgentAbilityPayload, state: ConnectionState) -> None:
        self.slot: str = data['slot']
        self.display_name: str = data['displayName']
        self.description: str = data['description']
        self.display_icon: Icon = Icon._from_url(data['displayIcon'])


class AgentRole(Hashable):
    __slots__: Tuple[str, ...] = (
        'uuid',
        'display_name',
        'description',
        'asset_path'
    )
    
    def __init__(self, *, data: AgentRolePayload, state: ConnectionState) -> None:
        self.uuid: str = data['uuid']
        self.display_name: str = data['displayName']
        self.description: str = data['description']
        self.asset_path: str = data['assetPath']
        
        
class Agent(Hashable):
    __slots__: Tuple[str, ...] = (
        'uuid', 
        'display_name', 
        'description', 
        'developer_name',
        'character_tags',
        'display_icon', 
        'display_icon_small', 
        'bust_portrait',
        'full_portrait', 
        'kill_feed_portrait',
        'background',
        'asset_path',
        'is_full_portrait_right_facing',
        'is_playable_character',
        'is_available_for_test',
        'is_base_content',
        'role',
        'abilities',
        'voice_line'
    )
    
    def __init__(self, *, data: AgentPayload, state: ConnectionState) -> None:
        self.uuid: str = data['uuid']
        self.display_name: str = data['displayName']
        self.description: str = data['description']
        self.developer_name: str = data['developerName']
        self.character_tags: List[str] = data['characterTags']
        self.display_icon: Icon = Icon._from_url(data['displayIcon'])
        self.display_icon_small: Icon = Icon._from_url(data['displayIconSmall'])
        self.bust_portrait: Icon = Icon._from_url(data['bustPortrait'])
        self.full_portrait: Icon = Icon._from_url(data['fullPortrait'])
        self.kill_feed_portrait: Icon = Icon._from_url(data['killfeedPortrait'])
        self.background: Icon = Icon._from_url(data['background'])
        self.asset_path: str = data['assetPath']
        self.is_full_portrait_right_facing: bool = data['isFullPortraitRightFacing']
        self.is_playable_character: bool = data['isPlayableCharacter']
        self.is_available_for_test: bool = data['isAvailableForTest']
        self.is_base_content: bool = data['isBaseContent']
        self.role: AgentRole = AgentRole(data=data['role'], state=state)
        self.abilities: List[AgentAbility] = [AgentAbility(data=a, state=state) for a in data['abilities']]
        self.voice_line: AgentVoiceLine = AgentVoiceLine(data=data['voiceLine'], state=state)
        