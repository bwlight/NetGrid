# cooldown_manager.py V3

from typing import Dict


class CooldownManager:
    """
    Tracks and updates ability cooldowns for each BattleEntity.
    Cooldowns are stored on the entity itself:
        entity.cooldowns = { ability_id: turns_remaining }
    """

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def start_cooldown(self, entity, ability: dict) -> None:
        """
        Begins the cooldown for an ability after it is used.
        Cooldown is defined in the ability schema as an integer.
        """
        cd = ability.get("cooldown", 0)
        if cd and cd > 0:
            entity.cooldowns[ability["id"]] = cd

    def tick_cooldowns(self, entity) -> None:
        """
        Decrements all cooldowns by 1 at the start of the entity's turn.
        Removes any cooldowns that have expired.
        """
        expired = []

        for ability_id, turns in entity.cooldowns.items():
            if turns > 1:
                entity.cooldowns[ability_id] = turns - 1
            else:
                expired.append(ability_id)

        for ability_id in expired:
            del entity.cooldowns[ability_id]

    def is_on_cooldown(self, entity, ability_id: str) -> bool:
        """
        Returns True if the ability is still cooling down.
        """
        return ability_id in entity.cooldowns

    # -------------------------------------------------------------------------
    # Optional: Utility for UI/AI
    # -------------------------------------------------------------------------

    def turns_remaining(self, entity, ability_id: str) -> int:
        """
        Returns the number of turns remaining for a cooldown, or 0 if ready.
        """
        return entity.cooldowns.get(ability_id, 0)
