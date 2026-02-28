from dataclasses import dataclass
from typing import Dict


@dataclass
class FriendshipMatrixConfig:
    matrix: Dict[str, Dict[str, int]]
