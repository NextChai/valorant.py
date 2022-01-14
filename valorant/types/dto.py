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

from typing import TypedDict, List

# NOTE: Please note this file needs to be seperated into multiple files

class UpdateDto(TypedDict):
    id: int
    author: str
    publish: bool
    publish_locations: List[str] # NOTE: MAKE ENUM (Legal values: riotclient, riotstatus, game)
    translations: List[ContentDto]
    created_at: str
    updated_at: str
    

class StatusDto(TypedDict):
    id: int
    maintenance_status: str # NOTE: MAKE ENUM (Legal values: scheduled, in_progress, complete)
    incident_severity: str # NOTE: MAKE ENUM (Legal values: info, warning, critical)
    titles: List[ContentDto]
    updates: List[UpdateDto]
    created_at: str
    archive_at: str
    updated_at: str
    platforms: List[str] # NOTE: MAKE ENUM 	(Legal values: windows, macos, android, ios, ps4, xbone, switch)
    

class PlatformDataDto(TypedDict):
    id: str
    name: str
    locales: List[str]
    maintenances: List[StatusDto]
    incidents: List[StatusDto]
    
    
    
class LeaderboardDto(TypedDict):
    shard: str # The shard for the given leaderboard.
    actId: str # The act id for the given leaderboard. Act ids can be found using the val-content API.
    totalPlayers: float
    players: List[PlayerDto]


class RecentMatchesDto(TypedDict):
    currentTime: float
    matchIds: List[str]


class MatchlistEntryDto(TypedDict):
    matchId: str
    gameStartTimeMillis: float
    teamId: str
    

class MatchlistDto(TypedDict):
    puuid: str
    history: List[MatchlistEntryDto]


class MatchInfoDto(TypedDict):
    matchId: str
    mapId: str
    gameLengthMillis: int
    gameStartMillis: float
    provisioningFlowId: str
    isCompleted: bool
    customGameName: str
    queueId: str
    gameMode: str
    isRanked: bool
    seasonId: str
    
    
class AbilityCastsDto(TypedDict):
    grenadeCasts: int
    ability1Casts: int
    ability2Casts: int
    ultimateCasts: int
    
    
class PlayerStatsDto(TypedDict):
    score: int
    roundsPlayed: int
    kills: int
    deaths: int
    assists: int
    playtimeMillis: int
    abilityCasts: AbilityCastsDto
    

class PlayerDto(TypedDict):
    puuid: str
    gameName: str
    tagLine: str
    teamId: str
    partyId: str
    characterId: str
    stats: PlayerStatsDto
    competitiveTier: int
    playerCard: str
    playerTitle: str
    
    
class LocationDto(TypedDict):
    x: int
    y: int
    
    
class PlayerLocationsDto(TypedDict):
    puuid: str
    viewRadians: float
    location: LocationDto
    

class DamageDto(TypedDict):
    receiver: str
    damage: int
    legshots: int
    bodyshots: int
    headshots: int


class AbilityDto(TypedDict):
    grenadeEffects: str
    ability1Effects: str
    ability2Effects: str
    ultimateEffects: str


class EconomyDto(TypedDict):
    loadoutValue: int
    weapon: str
    armor: str
    remaining: int
    spent: int

    
class FinishingDamageDto(TypedDict):
    damageType: str
    damageItem: str
    isSecondaryFireMode: bool
    
    
class KillDto(TypedDict):
    timeSinceGameStartMillis: int
    timeSinceRoundStartMillis: int
    killer: str
    victim: str
    victimLocation: LocationDto
    assistants: List[str]
    playerLocations: List[PlayerLocationsDto]
    finishingDamage: FinishingDamageDto
    

class PlayerRoundStatsDto(TypedDict):
    puuid: str
    kills: List[KillDto]
    damage: List[DamageDto]
    score: int
    economy: EconomyDto
    ability: AbilityDto


class CoachDto(TypedDict):
    puuid: str
    teamId: str
    
    
class TeamDto(TypedDict):
    teamId: str
    won: bool
    roundsPlayed: int
    roundsWon: int
    numPoints: int  # Team points scored. Number of kills in deathmatch.
    
    
class RoundResultDto(TypedDict):
    roundNum: int
    roundResult: str
    roundCeremony: str
    winningTeam: str
    bombPlanter: str
    bombDefuser: str
    plantRoundTime: int
    plantPlayerLocations: List[PlayerLocationsDto]
    plantLocation: LocationDto
    plantSite: str
    defuseRoundTime: int
    defusePlayerLocations: List[PlayerLocationsDto]
    defuseLocation: LocationDto
    playerStats: List[PlayerRoundStatsDto]
    roundResultCode: str
    
    
class MatchDto(TypedDict):
    matchinfo: MatchInfoDto
    players: List[PlayerDto]
    coaches: List[CoachDto]
    teams: List[TeamDto]
    roundResults: List[RoundResultDto]
    
    
class ActiveShardDto(TypedDict):
    pass


class _AccountDtoOptional(TypedDict, total=False):
    gameName: str
    tagLine: str


class AccountDto(_AccountDtoOptional):
    puuid: str
    

class ContentItemDto(TypedDict):
    name: str
    localizedNames: str
    id: str
    assetName: str
    assetPath: str
    
    
class ActDto(TypedDict):
    name: str
    localizedNames: str
    id: str
    isActive: bool
    
    
class ContentDto(TypedDict):
    version: str
    characters: List[ContentItemDto]
    maps: List[ContentItemDto]
    chromas: List[ContentItemDto]
    skins: List[ContentItemDto]
    skinLevels: List[ContentItemDto]
    equips: List[ContentItemDto]
    gameModes: List[ContentItemDto]
    sprays: List[ContentItemDto]
    sprayLevels: List[ContentItemDto]
    charms: List[ContentItemDto]
    charmLevels: List[ContentItemDto]
    playerCards: List[ContentItemDto]
    playerTitles: List[ContentItemDto]
    acts: List[ActDto]