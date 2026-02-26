from __future__ import annotations

from typing import Dict, Tuple, List, Optional

from .party_loader import (
    FriendshipMatrixConfig,
    RelationshipTypeConfig,
)


class RelationshipSystem:
    def __init__(
        self,
        friendship_config: FriendshipMatrixConfig,
        relationship_types: List[RelationshipTypeConfig],
    ) -> None:
        self.config = friendship_config
        self.relationship_types = relationship_types

        # key: (id_a, id_b) sorted tuple, value: friendship int
        self._friendship: Dict[Tuple[str, str], int] = {}

    def _key(self, a: str, b: str) -> Tuple[str, str]:
        return tuple(sorted((a, b)))

    def get_friendship(self, a: str, b: str) -> int:
        key = self._key(a, b)
        return self._friendship.get(key, self.config.default_value)

    def set_friendship(self, a: str, b: str, value: int) -> None:
        clamped = max(self.config.range_min, min(self.config.range_max, value))
        self._friendship[self._key(a, b)] = clamped

    def modify_friendship(self, a: str, b: str, delta: int) -> int:
        current = self.get_friendship(a, b)
        new_value = current + delta
        self.set_friendship(a, b, new_value)
        return self.get_friendship(a, b)

    def get_relationship_type(self, a: str, b: str) -> Optional[RelationshipTypeConfig]:
        value = self.get_friendship(a, b)
        for rel in self.relationship_types:
            if rel.threshold_min <= value <= rel.threshold_max:
                return rel
        return None

    def get_all_pairs(self) -> Dict[Tuple[str, str], int]:
        return dict(self._friendship)
