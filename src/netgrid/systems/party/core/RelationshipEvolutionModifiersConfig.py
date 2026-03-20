from dataclasses import dataclass
from typing import Dict


@dataclass
class RelationshipEvolutionModifiersConfig:
    bonded: Dict[str, float | int]
    rival: Dict[str, float | int]
    hostile: Dict[str, float | int]
