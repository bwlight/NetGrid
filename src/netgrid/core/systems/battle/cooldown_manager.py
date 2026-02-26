from __future__ import annotations

class CooldownManager:
    """
    Tracks and updates ability cooldowns for each Cyberkin.
    """

    def __init__(self):
        pass

    def apply_cooldown(self, actor, ability_id: str, turns: int):
        actor.cooldowns[ability_id] = turns

    def tick_cooldowns(self, actor):
        expired = []

        for ability_id, turns in actor.cooldowns.items():
            new_value = turns - 1
            if new_value <= 0:
                expired.append(ability_id)
            else:
                actor.cooldowns[ability_id] = new_value

        for ability_id in expired:
            del actor.cooldowns[ability_id]

    def is_usable(self, actor, ability_id: str) -> bool:
        return ability_id not in actor.cooldowns
