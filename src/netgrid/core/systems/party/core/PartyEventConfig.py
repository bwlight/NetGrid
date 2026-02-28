from dataclasses import dataclass
from typing import Dict


@dataclass
class PartyEventConfig:
    name: str
    effects: Dict[str, int]
