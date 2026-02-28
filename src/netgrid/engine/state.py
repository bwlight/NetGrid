from dataclasses import dataclass, field
from typing import Dict, Set

from .models import Quest


@dataclass
class QuestState:
    completed: Set[str] = field(default_factory=set)
    active: Set[str] = field(default_factory=set)
    flags: Set[str] = field(default_factory=set)
    resonance_level: int = 1


class QuestManager:
    def __init__(self, quests: Dict[str, Quest]):
        self.quests = quests
        self.state = QuestState()

    def can_start(self, code: str) -> bool:
        quest = self.quests[code]
        # later: check prerequisites, flags, etc.
        return code not in self.state.completed

    def start(self, code: str) -> None:
        if self.can_start(code):
            self.state.active.add(code)

    def complete(self, code: str) -> None:
        quest = self.quests[code]
        if code not in self.state.active:
            return
        self.state.active.remove(code)
        self.state.completed.add(code)

        # apply rewards
        self.state.resonance_level += quest.rewards.resonance_level_delta
        self.state.flags.update(quest.rewards.flags)

        # auto‑unlock followups (for main story, if you want)
        for follow in quest.followups:
            if follow in self.quests:
                self.state.active.add(follow)
