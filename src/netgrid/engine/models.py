from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional


class QuestCategory(str, Enum):
    MAIN = "main"
    BOND = "bond"
    SECTOR = "sector"
    STABILIZATION = "stabilization"
    SIDE = "side"


@dataclass
class QuestObjective:
    id: str
    description: str
    optional: bool = False


@dataclass
class QuestReward:
    resonance_level_delta: int = 0
    abilities: List[str] = field(default_factory=list)
    items: List[str] = field(default_factory=list)
    flags: List[str] = field(default_factory=list)


@dataclass
class Quest:
    code: str
    title: str
    category: QuestCategory
    sector: Optional[str]
    summary: str
    objectives: List[QuestObjective]
    rewards: QuestReward
    followups: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
