from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Set, Optional

from netgrid.systems.quests.models import Quest, QuestStep
from netgrid.utils.logging import log


@dataclass
class QuestProgress:
    """Tracks progress for a single quest."""
    current_step: int = 0
    completed_steps: Set[str] = field(default_factory=set)
    is_completed: bool = False


class QuestState:
    """Tracks global quest progression across all quests."""
    def __init__(self):
        self.quests: Dict[str, QuestProgress] = {}

    def ensure(self, quest_id: str) -> QuestProgress:
        if quest_id not in self.quests:
            self.quests[quest_id] = QuestProgress()
        return self.quests[quest_id]


class QuestManager:
    def __init__(self, quests: Dict[str, Quest]):
        self.quests = quests
        self.state = QuestState()

    # -----------------------------
    # Quest Lifecycle
    # -----------------------------

    def start(self, quest_id: str) -> None:
        if quest_id not in self.quests:
            log(f"Quest '{quest_id}' not found.")
            return

        progress = self.state.ensure(quest_id)

        if progress.is_completed:
            log(f"Quest '{quest_id}' already completed.")
            return

        log(f"Quest '{quest_id}' started.")

    def complete(self, quest_id: str) -> None:
        if quest_id not in self.quests:
            log(f"Quest '{quest_id}' not found.")
            return

        progress = self.state.ensure(quest_id)

        if progress.is_completed:
            return

        progress.is_completed = True
        log(f"Quest '{quest_id}' fully completed.")

    # -----------------------------
    # Step Progression
    # -----------------------------

    def get_current_step(self, quest_id: str) -> Optional[QuestStep]:
        if quest_id not in self.quests:
            return None

        progress = self.state.ensure(quest_id)
        quest = self.quests[quest_id]

        if progress.current_step >= len(quest.steps):
            return None

        return quest.steps[progress.current_step]

    def advance_step(self, quest_id: str) -> None:
        if quest_id not in self.quests:
            log(f"Quest '{quest_id}' not found.")
            return

        quest = self.quests[quest_id]
        progress = self.state.ensure(quest_id)

        if progress.is_completed:
            return

        if progress.current_step >= len(quest.steps):
            self.complete(quest_id)
            return

        step = quest.steps[progress.current_step]

        # Mark step as completed
        progress.completed_steps.add(step.id)
        log(f"Completed step '{step.id}' of quest '{quest_id}'.")

        # Apply rewards (strings for now; can integrate with systems later)
        for reward in step.rewards:
            log(f"Reward granted: {reward}")

        # Move to next step
        progress.current_step += 1

        # If no more steps, complete quest
        if progress.current_step >= len(quest.steps):
            self.complete(quest_id)

    # -----------------------------
    # Condition Checking
    # -----------------------------

    def check_conditions(self, quest_id: str) -> bool:
        """Checks if the current step's conditions are met.
        Conditions are strings for now; integration with systems comes later."""
        step = self.get_current_step(quest_id)
        if not step:
            return False

        if not step.conditions:
            return True

        # Placeholder: conditions are simple flags or triggers
        # Later: integrate with party, stability, overworld, battle, etc.
        log(f"Conditions for step '{step.id}': {step.conditions}")
        return True  # Always true for now
