from __future__ import annotations

from typing import Dict, List, Tuple

from .party_loader import SynergyRulesConfig, SynergyTier
from .relationship_system import RelationshipSystem


class SynergyCalculator:
    def __init__(self, rules: SynergyRulesConfig, relationship_system: RelationshipSystem) -> None:
        self.rules = rules
        self.relationship_system = relationship_system

    def _compute_average_friendship(self, party_ids: List[str]) -> float:
        pairs: List[int] = []
        n = len(party_ids)
        for i in range(n):
            for j in range(i + 1, n):
                a = party_ids[i]
                b = party_ids[j]
                pairs.append(self.relationship_system.get_friendship(a, b))
        if not pairs:
            return float(self.relationship_system.config.default_value)
        return sum(pairs) / len(pairs)

    def get_synergy_value(self, party_ids: List[str]) -> float:
        if self.rules.calculation == "average_friendship":
            return self._compute_average_friendship(party_ids)
        # future: other calculation modes
        return self._compute_average_friendship(party_ids)

    def get_synergy_tier(self, party_ids: List[str]) -> SynergyTier | None:
        value = self.get_synergy_value(party_ids)
        for tier in self.rules.tiers:
            if tier.range_min <= value <= tier.range_max:
                return tier
        return None

    def apply_synergy_effects(
        self,
        base_stats: Dict[str, float],
        party_ids: List[str],
    ) -> Dict[str, float]:
        """
        base_stats: e.g. {\"ATK\": 100, \"DEF\": 80, \"SPD\": 50}
        returns new stats with synergy applied.
        """
        tier = self.get_synergy_tier(party_ids)
        if tier is None or not tier.effects:
            return dict(base_stats)

        result = dict(base_stats)
        for stat, modifier in tier.effects.items():
            if stat in result:
                result[stat] = result[stat] * (1.0 + modifier)
        return result
