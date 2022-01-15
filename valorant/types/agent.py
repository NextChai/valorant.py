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

from typing import List, TypedDict, Optional


class AgentRole(TypedDict):
    uuid: str
    displayName: str
    description: str
    displayIcon: Optional[str]
    assetPath: str
    
    
class AgentAbility(TypedDict):
    slot: str
    displayName: str
    description: str
    displayIcon: Optional[str]
    

class AgentMedia(TypedDict):
    id: int
    wwise: str
    wave: str
    
    
class AgentVoiceLine(TypedDict):
    minDuration: float
    maxDuration: float
    mediaList: List[AgentMedia]
    

class Agent(TypedDict):
    uuid: str
    displayName: str
    description: str
    developerName: str
    characterTags: List[str]
    displayIcon: Optional[str]
    displayIconSmall: Optional[str]
    bustPortrait: Optional[str]
    fullPortrait: Optional[str]
    killfeedPortrait: Optional[str]
    background: Optional[str]
    assetPath: str
    isFullPortraitRightFacing: bool
    isPlayableCharacter: bool
    isAvailableForTest: bool
    isBaseContent: bool
    role: AgentRole
    abilities: List[AgentAbility]
    voiceLine: AgentVoiceLine