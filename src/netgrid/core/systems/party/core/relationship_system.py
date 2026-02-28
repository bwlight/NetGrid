from __future__ import annotations

from typing import Dict, List, Union, Any

from .party_loader import (
    FriendshipMatrixConfig,
    RelationshipTypeConfig,
)


# A party member can be a string ID (current behavior)
# or a Cyberkin object (future behavior).
PartyMember = Union[str, Any]


class RelationshipSystem:
    def __init__(
        self,
        friendship_config: FriendshipMatrixConfig,
        relationship_types: List[RelationshipTypeConfig],
    ) -> None:
        self.friendship_config = friendship_config
        self.relationship_types = relationship_types

        # Internal friendship matrix (id -> id -> value)
        self.friendship: Dict[str, Dict[str, int]] = {
            a: {b: val for b, val in row.items()}
            for a, row in friendship_config.matrix.items()
        }

    # --- Internal helpers ---

    def _extract_id(self, member: PartyMember) -> str:
        """Return the ID of a party member, whether it's a string or a Cyberkin object."""
        if isinstance(member, str):
            return member
        return member.id  # Future: Cyberkin object must have .id

    # --- Friendship operations ---

    def get_friendship(self, a: PartyMember, b: PartyMember) -> int:
        a_id = self._extract_id(a)
        b_id = self._extract_id(b)
        return self.friendship.get(a_id, {}).get(b_id, 0)

    def modify_friendship(self, a: PartyMember, b: PartyMember, delta: int) -> int:
        a_id = self._extract_id(a)
        b_id = self._extract_id(b)

        current = self.friendship.get(a_id, {}).get(b_id, 0)
        new_value = max(0, min(100, current + delta))

        if a_id not in self.friendship:
            self.friendship[a_id] = {}
        self.friendship[a_id][b_id] = new_value

        return new_value

    # --- Relationship type classification ---

    def get_relationship_type(self, a: PartyMember, b: PartyMember) -> RelationshipTypeConfig | None:
        value = self.get_friendship(a, b)

        for rel_type in self.relationship_types:
            if rel_type.min_value <= value <= rel_type.max_value:
                return rel_type

        return None