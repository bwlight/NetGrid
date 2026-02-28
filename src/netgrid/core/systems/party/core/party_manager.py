from __future__ import annotations

from typing import Dict, List, Union, Any

from .party_loader import (
    PartyLoader,
    FriendshipMatrixConfig,
    SynergyRulesConfig,
    RelationshipTypeConfig,
    PartyEventConfig,
    RelationshipEvolutionModifiersConfig,
)
from .relationship_system import RelationshipSystem
from .synergy_calculator import SynergyCalculator


# Type alias for future-proofing:
# A party member can be a string ID (current behavior)
# or a Cyberkin object (future behavior).
PartyMember = Union[str, Any]


class PartyManager:
    def __init__(self) -> None:
        self.loader = PartyLoader()

        # configs
        self.friendship_config: FriendshipMatrixConfig = self.loader.load_friendship_matrix_config()
        self.synergy_rules: SynergyRulesConfig = self.loader.load_synergy_rules()
        self.relationship_types: List[RelationshipTypeConfig] = self.loader.load_relationship_types()
        self.party_events: List[PartyEventConfig] = self.loader.load_party_events()
        self.evolution_modifiers: RelationshipEvolutionModifiersConfig = (
            self.loader.load_relationship_evolution_modifiers()
        )

        # systems
        self.relationship_system = RelationshipSystem(
            friendship_config=self.friendship_config,
            relationship_types=self.relationship_types,
        )
        self.synergy_calculator = SynergyCalculator(
            rules=self.synergy_rules,
            relationship_system=self.relationship_system,
        )

        # current party members (IDs for now, objects later)
        self.party: List[PartyMember] = []

    # --- Party setup ---

    def set_party(self, members: List[PartyMember]) -> None:
        """Accepts either string IDs or Cyberkin objects."""
        self.party = list(members)

    def _extract_ids(self) -> List[str]:
        """Internal helper: always return a list of IDs, even if party contains objects."""
        ids: List[str] = []
        for member in self.party:
            if isinstance(member, str):
                ids.append(member)
            else:
                # Future: Cyberkin object must have .id or .identifier
                ids.append(member.id)
        return ids

    # --- Relationship operations ---

    def get_friendship(self, a: str, b: str) -> int:
        return self.relationship_system.get_friendship(a, b)

    def modify_friendship(self, a: str, b: str, delta: int) -> int:
        return self.relationship_system.modify_friendship(a, b, delta)

    def get_relationship_type_name(self, a: str, b: str) -> str | None:
        rel = self.relationship_system.get_relationship_type(a, b)
        return rel.name if rel else None

    # --- Synergy operations ---

    def get_synergy_value(self) -> float:
        return self.synergy_calculator.get_synergy_value(self._extract_ids())

    def get_synergy_tier_name(self) -> str | None:
        tier = self.synergy_calculator.get_synergy_tier(self._extract_ids())
        return tier.name if tier else None

    def apply_synergy_to_stats(self, base_stats: Dict[str, float]) -> Dict[str, float]:
        return self.synergy_calculator.apply_synergy_effects(base_stats, self._extract_ids())

    # --- Event handling ---

    def apply_event_effects(self, event_name: str, a: str, b: str) -> None:
        event = next((e for e in self.party_events if e.name == event_name), None)
        if event is None:
            return

        effects = event.effects
        if "friendship_gain" in effects:
            self.modify_friendship(a, b, int(effects["friendship_gain"]))
        if "friendship_loss" in effects:
            self.modify_friendship(a, b, -int(effects["friendship_loss"]))

    # --- Evolution hooks ---

    def get_evolution_modifiers_for_relationship(self, a: str, b: str) -> Dict[str, float | int]:
        rel = self.relationship_system.get_relationship_type(a, b)
        if rel is None:
            return {}

        name = rel.name.lower()
        if name == "bonded":
            return self.evolution_modifiers.bonded
        if name == "rival":
            return self.evolution_modifiers.rival
        if name == "hostile":
            return self.evolution_modifiers.hostile
        return {}
