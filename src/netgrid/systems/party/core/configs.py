from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


# --- Friendship Matrix ---

@dataclass
class FriendshipMatrixConfig:
    matrix: Dict[str, Dict[str, int]]


# --- Relationship Types ---

@dataclass
class RelationshipTypeConfig:
    name: str
    min_value: int
    max_value: int


# --- Party Events ---

@dataclass
class PartyEventConfig:
    name: str
    effects: Dict[str, int]


# --- Evolution Modifiers ---

@dataclass
class RelationshipEvolutionModifiersConfig:
    bonded: Dict[str, float | int]
    rival: Dict[str, float | int]
    hostile: Dict[str, float | int]


# --- Synergy Rules ---

@dataclass
class SynergyTierConfig:
    name: str
    min_value: float
    max_value: float
    stat_multipliers: Dict[str, float]


@dataclass
class SynergyRulesConfig:
    relationship_synergy: Dict[str, float]
    tiers: List[SynergyTierConfig]
