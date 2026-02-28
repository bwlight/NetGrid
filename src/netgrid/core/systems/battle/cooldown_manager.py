from __future__ import annotations

from typing import Dict
from .battle_entity import BattleEntity


class CooldownManager:
    """
    Tracks ability cooldowns for each BattleEntity.
    Cooldowns are stored on the entity itself:
        entity.cooldowns = { ability_name: turns_remaining }
    """

    def set_cooldown(self, entity: BattleEntity, ability_name: str, turns: int) -> None:
        """
        Starts a cooldown for an ability.
        """
        entity.cooldowns[ability_name] = turns

    def tick(self, entity: BattleEntity) -> None:
        """
        Decrements all cooldowns by 1.
        Removes abilities whose cooldown has expired.
        """
        expired: list[str] = []

        for ability, turns in entity.cooldowns.items():
            if turns > 1:
                entity.cooldowns[ability] = turns - 1
            else:
                expired.append(ability)

        for ability in expired:
            del entity.cooldowns[ability]

    def is_on_cooldown(self, entity: BattleEntity, ability_name: str) -> bool:
        """
        Returns True if the ability is still cooling down.
        """
        return ability_name in entity.cooldowns
