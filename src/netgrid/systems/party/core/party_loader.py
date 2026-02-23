from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path(__file__).resolve().parent.parent  # .../systems/party
DATA_DIR = BASE_DIR / "data"


@dataclass
class FriendshipMatrixConfig:
    range_min: int
    range_max: int
    default_value: int
    personality_modifier: bool
    corruption_modifier: bool


@dataclass
class SynergyTier:
    name: str
    range_min: int
    range_max: int
    effects: Dict[str, float]


@dataclass
class SynergyRulesConfig:
    calculation: str
    tiers: List[SynergyTier]


@dataclass
class RelationshipTypeConfig:
    name: str
    threshold_min: int
    threshold_max: int
    effects: Dict[str, float]


@dataclass
class PartyEventConfig:
    name: str
    trigger: str
    effects: Dict[str, Any]


@dataclass
class RelationshipEvolutionModifiersConfig:
    bonded: Dict[str, Any]
    rival: Dict[str, Any]
    hostile: Dict[str, Any]


class PartyLoader:
    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = data_dir or DATA_DIR

    def _load_json(self, filename: str) -> Dict[str, Any]:
        import json

        path = self.data_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing data file: {path}")

        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def load_friendship_matrix_config(self) -> FriendshipMatrixConfig:
        data = self._load_json("friendship_matrix.json")["friendship_matrix"]
        range_cfg = data["range"]
        init_cfg = data["initialization"]

        return FriendshipMatrixConfig(
            range_min=range_cfg["min"],
            range_max=range_cfg["max"],
            default_value=init_cfg["default_value"],
            personality_modifier=init_cfg["personality_modifier"],
            corruption_modifier=init_cfg["corruption_modifier"],
        )

    def load_synergy_rules(self) -> SynergyRulesConfig:
        data = self._load_json("synergy_rules.json")["synergy_rules"]
        tiers: List[SynergyTier] = []
        for t in data["tiers"]:
            tiers.append(
                SynergyTier(
                    name=t["name"],
                    range_min=t["range"][0],
                    range_max=t["range"][1],
                    effects=t.get("effects", {}),
                )
            )
        return SynergyRulesConfig(
            calculation=data["calculation"],
            tiers=tiers,
        )

    def load_relationship_types(self) -> List[RelationshipTypeConfig]:
        data = self._load_json("relationship_types.json")["relationship_types"]
        result: List[RelationshipTypeConfig] = []
        for r in data:
            thr = r["threshold"]
            result.append(
                RelationshipTypeConfig(
                    name=r["name"],
                    threshold_min=thr["min"],
                    threshold_max=thr["max"],
                    effects=r.get("effects", {}),
                )
            )
        return result

    def load_party_events(self) -> List[PartyEventConfig]:
        data = self._load_json("party_events.json")["party_events"]
        result: List[PartyEventConfig] = []
        for e in data:
            result.append(
                PartyEventConfig(
                    name=e["name"],
                    trigger=e["trigger"],
                    effects=e.get("effects", {}),
                )
            )
        return result

    def load_relationship_evolution_modifiers(self) -> RelationshipEvolutionModifiersConfig:
        data = self._load_json("relationship_evolution_modifiers.json")[
            "relationship_evolution_modifiers"
        ]
        return RelationshipEvolutionModifiersConfig(
            bonded=data.get("bonded", {}),
            rival=data.get("rival", {}),
            hostile=data.get("hostile", {}),
        )
