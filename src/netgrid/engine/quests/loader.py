import json
from pathlib import Path
from typing import Dict

from .models import Quest, QuestCategory, QuestObjective, QuestReward


def load_quest_from_json(path: Path) -> Quest:
    data = json.loads(path.read_text(encoding="utf-8"))

    objectives = [
        QuestObjective(
            id=obj["id"],
            description=obj["description"],
            optional=obj.get("optional", False),
        )
        for obj in data.get("objectives", [])
    ]

    rewards_data = data.get("rewards", {})
    rewards = QuestReward(
        resonance_level_delta=rewards_data.get("resonance_level_delta", 0),
        abilities=rewards_data.get("abilities", []),
        items=rewards_data.get("items", []),
        flags=rewards_data.get("flags", []),
    )

    return Quest(
        code=data["code"],
        title=data["title"],
        category=QuestCategory(data["category"]),
        sector=data.get("sector"),
        summary=data.get("summary", ""),
        objectives=objectives,
        rewards=rewards,
        followups=data.get("followups", []),
        tags=data.get("tags", []),
        metadata=data.get("metadata", {}),
    )


def load_all_quests(root: Path) -> Dict[str, Quest]:
    quests: Dict[str, Quest] = {}
    for path in root.rglob("*.json"):
        quest = load_quest_from_json(path)
        quests[quest.code] = quest
    return quests
