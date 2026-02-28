from __future__ import annotations

from typing import Dict, List, Union, Any

from .party_loader import SynergyRulesConfig
from .relationship_system import RelationshipSystem


# A party member can be a string ID (current behavior)
# or a Cyberkin object (future behavior).
PartyMember = Union[str, Any]


class SynergyCalculator:
    def __init__(
        self,
        rules: SynergyRulesConfig,
        relationship_system: RelationshipSystem,
    ) -> None:
        self.rules = rules
        self.relationship_system = relationship_system

    # --- Internal helpers ---

    def _extract_id(self, member: PartyMember) -> str:
        """Return the ID of a party member, whether it's a string or a Cyberkin object."""
        if isinstance(member, str):
            return member
        return member.id  # Future: Cyberkin object must have .id

    def _extract_ids(self, members: List[PartyMember]) -> List[str]:
        return [self._extract_id(m) for m in members]

    # --- Synergy calculations ---

    def get_synergy_value(self, members: List[PartyMember]) -> float:
        ids = self._extract_ids(members)

        total = 0.0
        count = 0

        # Pairwise synergy calculation
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                a = ids[i]
                b = ids[j]

                # Relationship-based synergy
                rel = self.relationship_system.get_relationship_type(a, b)
                if rel and rel.name in self.rules.relationship_synergy:
                    total += self.rules.relationship_synergy[rel.name]
                    count += 1

        if count == 0:
            return 0.0

        return total / count

    def get_synergy_tier(self, members: List[PartyMember]):
        value = self.get_synergy_value(members)

        for tier in self.rules.tiers:
            if tier.min_value <= value <= tier.max_value:
                return tier

        return None

    def apply_synergy_effects(
        self,
        base_stats: Dict[str, float],
        members: List[PartyMember],
    ) -> Dict[str, float]:
        tier = self.get_synergy_tier(members)
        if tier is None:
            return base_stats

        modified = dict(base_stats)

        for stat, multiplier in tier.stat_multipliers.items():
            if stat in modified:
                modified[stat] *= multiplier

        return modified
