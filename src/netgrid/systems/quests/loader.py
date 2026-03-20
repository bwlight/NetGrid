from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List

from netgrid.systems.quests.models import (
    Quest,
    QuestStep,
    QuestCategory,
)
from netgrid.utils.errors import DataValidationError
from netgrid.utils.logging import log


QUEST_DATA_PATH = Path("data/quests")


class QuestLoader:
    @staticmethod
    def load_all() -> Dict[str, Quest]:
        if not QUEST_DATA_PATH.exists():
            raise DataValidationError(f"Quest data folder not found: {QUEST_DATA_PATH}")

        quests: Dict[str, Quest] = {}

        for file in QUEST_DATA_PATH.glob("*.json"):
            try:
                quest = QuestLoader.load_file(file)
                quests[quest.id] = quest
            except Exception as e:
                log(f"Failed to load quest from {file}: {e}")

        return quests

    @staticmethod
    def load_file(path: Path) -> Quest:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        # Validate required fields
        for field in ["id", "name", "type", "steps"]:
            if field not in raw:
                raise DataValidationError(f"Missing required quest field: {field}")

        quest_id = raw["id"]
        name = raw["name"]
        category = QuestCategory(raw["type"])
        sector = raw.get("sector")
        description = raw.get("description")

        # Parse steps
        steps: List[QuestStep] = []
        for step_raw in raw["steps"]:
            if "id" not in step_raw or "description" not in step_raw:
                raise DataValidationError(f"Step missing required fields in quest {quest_id}")

            step = QuestStep(
                id=step_raw["id"],
                description=step_raw["description"],
                conditions=step_raw.get("conditions", []),
                rewards=step_raw.get("rewards", []),
            )
            steps.append(step)

        return Quest(
            id=quest_id,
            name=name,
            category=category,
            sector=sector,
            description=description,
            steps=steps,
        )
