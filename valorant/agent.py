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

from typing import TYPE_CHECKING, List, Optional, Tuple

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
    """
    Reprenents an :class:`Agent`'s voice line.
    
    Attributes
    ----------
    id: :class:`int`
        The ID of the voice line.
    wwise: :class:`str`
        The ``wem`` downlaod link for the voice line.
    wave: :class:`str`
        the ``wav`` download link for the voice line.
    """
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
    """
    Represents the voice line information of an :class:`Agent`.
    
    Attributes
    ----------
    min_duration: float
        The minimum duration of a voice line.
    max_duration: float
        The maximum duration of a voice line.
    media: List[:class:`AgentMedia`]
        The list of voice lines that the agent has.
    """
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
    """
    Represents an ability of an :class:`Agent`.
    
    Attributes
    ----------
    slot: :class:`str`
        The slot that the ability is in.
    display_name: :class:`str`
        The display name of the ability.
    description: :class:`str`
        The description of the ability.
    display_icon: Optional[:class:`Icon`]
        The display icon of the ability, if any.
    """
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
        self.display_icon: Optional[Icon] = Icon._from_url(icon) if (icon := data['displayIcon']) else None


class AgentRole(Hashable):
    """
    Represents the role an :class:`Agent` plays in the game.
    
    Attributes
    ----------
    uuid: :class:`str`
        The unique identifier of the role.
    display_name: :class:`str`
        The name of the role.
    description: :class:`str`
        The description of the role.
    display_icon: :class:`Icon`
        The icon of the role.
    asset_path: :class:`str`
        The path to the role's asset.
    """
    __slots__: Tuple[str, ...] = (
        'uuid',
        'display_name',
        'description',
        'display_icon',
        'asset_path'
    )
    
    def __init__(self, *, data: AgentRolePayload, state: ConnectionState) -> None:
        self.uuid: str = data['uuid']
        self.display_name: str = data['displayName']
        self.description: str = data['description']
        self.display_icon: Icon = Icon._from_url(data['displayIcon'])
        self.asset_path: str = data['assetPath']
        
        
class Agent(Hashable):
    """
    Represents an agent with Valorant.
    
    Attributes
    ----------
    uuid: :class:`str`
        The agent's UUID.
    display_name: :class:`str`
        The agent's display name.
    description: :class:`str`
        The agent's description.
    developer_name: :class:`str`
        The internal name of the agent, used by developers.
    character_tags: :class:`List[str]`
        A list of tags that describe the agent's character.
    display_icon: Optional[:class:`Icon`]
        The agent's display icon, if any.
    display_icon_small: Optional[:class:`Icon`]
        A smaller version of the agent's display icon, if any.
    bust_portrait: Optional[:class:`Icon`]
        The agent's bust portrait, if any.
    full_portrait: Optional[:class:`Icon`]
        A full portrait of the agent, if any.
    kill_feed_portrait: Optional[:class:`Icon`]
        The icon that shows up in the kill feed, if any.
    background: Optional[:class:`Icon`]
        The backhround of the agent's profile, if any.
    asset_path: :class:`str`
        The path to the agent's asset.
    is_full_portrait_right_facing: :class:`bool`
        Whether the agent's full portrait is facing right.
    is_playable_character: :class:`bool`
        Whether the agent is a playable character.
    is_available_for_test: :class:`bool`
        Whether the agent is available for testing.
    is_base_content: :class:`bool`
        Whether the agent is a base content.
    role: Optional[:class:`AgentRole`]
        The agent's role. Basically an explanation of what the agent's role is, if any.
    abilities: :class:`List[AgentAbility]`
        A list of abilities that the agent has.
    voice_line: :class:`List[AgentVoiceLine]`
        The agent's voice line. View individual voice lines in :class:`AgentMedia`.
    """
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
        self.display_icon: Optional[Icon] = Icon._from_url(icon) if (icon := data['displayIcon']) else None
        self.display_icon_small: Optional[Icon] = Icon._from_url(small_icon) if (small_icon := data['displayIconSmall']) else None
        self.bust_portrait: Optional[Icon] = Icon._from_url(bust) if (bust := data['bustPortrait']) else None
        self.full_portrait: Optional[Icon] = Icon._from_url(full) if (full := data['fullPortrait']) else None
        self.kill_feed_portrait: Optional[Icon] = Icon._from_url(kill_feed) if (kill_feed := data['killfeedPortrait']) else None
        self.background: Optional[Icon] = Icon._from_url(backgroud) if (backgroud := data['background']) else None
        self.asset_path: str = data['assetPath']
        self.is_full_portrait_right_facing: bool = data['isFullPortraitRightFacing']
        self.is_playable_character: bool = data['isPlayableCharacter']
        self.is_available_for_test: bool = data['isAvailableForTest']
        self.is_base_content: bool = data['isBaseContent']
        self.role: Optional[AgentRole] = AgentRole(data=role, state=state) if (role := data['role']) else None
        self.abilities: List[AgentAbility] = [AgentAbility(data=a, state=state) for a in data['abilities']]
        self.voice_line: AgentVoiceLine = AgentVoiceLine(data=data['voiceLine'], state=state)
        