from dataclasses import dataclass
from typing import Dict, List


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
