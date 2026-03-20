from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class QuestCategory(str, Enum):
    MAIN = "main"
    SIDE = "side"
    BOND = "bond"
    SECTOR = "sector"
    EVENT = "event"


@dataclass
class QuestStep:
    id: str
    description: str
    conditions: List[str] = field(default_factory=list)
    rewards: List[str] = field(default_factory=list)


@dataclass
class Quest:
    id: str
    name: str
    category: QuestCategory
    sector: Optional[str]
    description: Optional[str]
    steps: List[QuestStep]
