from __future__ import annotations

class StatusEffect:
    """
    Represents a single status effect instance on a Cyberkin.
    """

    def __init__(self, status_id: str, duration: int, effect_type: str, value: int = 0):
        self.id = status_id
        self.duration = duration
        self.type = effect_type  # "dot", "hot", "immobilize", "buff_block", etc.
        self.value = value       # damage/heal amount for DOT/HOT

    def tick(self, actor):
        """
        Applies per-turn effects (DOT/HOT).
        Returns a log message or None.
        """
        if self.type == "dot":
            actor.current_hp = max(0, actor.current_hp - self.value)
            return f"{actor.name} took {self.value} DOT damage from {self.id}"

        if self.type == "hot":
            actor.current_hp = min(actor.max_hp, actor.current_hp + self.value)
            return f"{actor.name} recovered {self.value} HP from {self.id}"

        return None
