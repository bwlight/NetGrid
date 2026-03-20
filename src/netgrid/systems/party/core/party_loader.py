from __future__ import annotations

from typing import Any, Dict, List, Union
import json
import os

from .configs import (
    FriendshipMatrixConfig,
    RelationshipTypeConfig,
    PartyEventConfig,
    RelationshipEvolutionModifiersConfig,
    SynergyRulesConfig,
    SynergyTierConfig,
)

PartyMember = Union[str, Any]


class PartyLoader:
    def __init__(self, base_path: str = "data/party") -> None:
        self.base_path = base_path

    # --- Internal helpers ---

    def _extract_id(self, member: PartyMember) -> str:
        if isinstance(member, str):
            return member
        return member.id

    def _load_json(self, filename: str) -> Dict[str, Any]:
        path = os.path.join(self.base_path, filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # --- Config loaders ---

    def load_friendship_matrix_config(self) -> FriendshipMatrixConfig:
        data = self._load_json("friendship_matrix.json")
        return FriendshipMatrixConfig(matrix=data["matrix"])

    def load_relationship_types(self) -> List[RelationshipTypeConfig]:
        data = self._load_json("relationship_types.json")
        return [
            RelationshipTypeConfig(
                name=entry["name"],
                min_value=entry["min_value"],
                max_value=entry["max_value"],
            )
            for entry in data["types"]
        ]

    def load_party_events(self) -> List[PartyEventConfig]:
        data = self._load_json("party_events.json")
        return [
            PartyEventConfig(
                name=entry["name"],
                effects=entry["effects"],
            )
            for entry in data["events"]
        ]

    def load_relationship_evolution_modifiers(self) -> RelationshipEvolutionModifiersConfig:
        data = self._load_json("relationship_evolution_modifiers.json")
        return RelationshipEvolutionModifiersConfig(
            bonded=data["bonded"],
            rival=data["rival"],
            hostile=data["hostile"],
        )

    def load_synergy_rules(self) -> SynergyRulesConfig:
        data = self._load_json("synergy_rules.json")

        tiers = [
            SynergyTierConfig(
                name=tier["name"],
                min_value=tier["min_value"],
                max_value=tier["max_value"],
                stat_multipliers=tier["stat_multipliers"],
            )
            for tier in data["tiers"]
        ]

        return SynergyRulesConfig(
            relationship_synergy=data["relationship_synergy"],
            tiers=tiers,
        )

    # --- Future expansion: Cyberkin loading ---

    def load_cyberkin_object(self, member: PartyMember):
        member_id = self._extract_id(member)
        raise NotImplementedError("Cyberkin loading not implemented yet.")

    # --- Future expansion: Party state loading ---

    def load_party_state(self):
        raise NotImplementedError("Party state loading not implemented yet.")
