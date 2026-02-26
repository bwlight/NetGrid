from __future__ import annotations

from typing import List, Optional
from status_effect import StatusEffect

class StatusEngine:
    """
    Handles applying, ticking, and expiring status effects.
    """

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # APPLY STATUS
    # ---------------------------------------------------------
    def apply_status(
        self,
        actor,
        status_id: str,
        duration: int,
        effect_type: str,
        value: int = 0
    ) -> str:
        """
        Adds a new status to the actor.
        """
        status = StatusEffect(status_id, duration, effect_type, value)
        actor.statuses.append(status)
        return f"{actor.name} is afflicted with {status_id}!"

    # ---------------------------------------------------------
    # TICK STATUSES
    # ---------------------------------------------------------
    def tick_statuses(self, actor) -> List[str]:
        """
        Ticks all statuses:
        - applies DOT/HOT
        - reduces duration
        - removes expired statuses
        Returns log messages.
        """
        logs = []
        expired = []

        for status in actor.statuses:
            # DOT/HOT effects
            tick_log = status.tick(actor)
            if tick_log:
                logs.append(tick_log)

            # Reduce duration
            status.duration -= 1
            if status.duration <= 0:
                expired.append(status)

        # Remove expired statuses
        for s in expired:
            actor.statuses.remove(s)
            logs.append(f"{actor.name}'s {s.id} expired")

        return logs

    # ---------------------------------------------------------
    # STATUS CHECK HELPERS
    # ---------------------------------------------------------
    def has_status(self, actor, status_id: str) -> bool:
        return any(s.id == status_id for s in actor.statuses)

    def consume_status(self, actor, status_id: str) -> bool:
        """
        Removes a status immediately (used for immobilize).
        """
        for s in actor.statuses:
            if s.id == status_id:
                actor.statuses.remove(s)
                return True
        return False
