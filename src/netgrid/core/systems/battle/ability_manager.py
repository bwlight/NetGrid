from __future__ import annotations

from typing import Any, Dict
from .battle_entity import BattleEntity
from .status_engine import StatusEngine
from .cooldown_manager import CooldownManager


class AbilityManager:
    """
    Executes abilities on BattleEntity objects.
    Handles:
    - Damage
    - Healing
    - Status effects
    - Cooldowns
    - Energy costs
    """

    def __init__(self, status_engine: StatusEngine, cooldown_manager: CooldownManager):
        self.status_engine = status_engine
        self.cooldown_manager = cooldown_manager

    # ---------------------------------------------------------
    # Ability Checks
    # ---------------------------------------------------------

    def can_use(self, user: BattleEntity, ability: Dict[str, Any]) -> bool:
        name = ability["name"]

        # Cooldown check
        if self.cooldown_manager.is_on_cooldown(user, name):
            return False

        # Energy check
        cost = ability.get("energy_cost", 0)
        if user.energy < cost:
            return False

        return True

    # ---------------------------------------------------------
    # Ability Execution
    # ---------------------------------------------------------

    def execute(self, user: BattleEntity, target: BattleEntity, ability: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes an ability and returns a result dictionary for logging.
        """

        name = ability["name"]
        result = {"ability": name, "events": []}

        # Pay energy cost
        cost = ability.get("energy_cost", 0)
        user.energy = max(0, user.energy - cost)

        # Damage
        if "damage" in ability:
            dmg = self._calculate_damage(user, target, ability)
            target.apply_damage(dmg)
            result["events"].append({"type": "damage", "amount": dmg})

        # Healing
        if "heal" in ability:
            heal_amount = ability["heal"]
            target.heal(heal_amount)
            result["events"].append({"type": "heal", "amount": heal_amount})

        # Status effects
        if "status" in ability:
            status = ability["status"]
            self.status_engine.apply_status(target, status)
            result["events"].append({"type": "status", "status": status.name})

        # Apply cooldown
        cooldown = ability.get("cooldown", 0)
        if cooldown > 0:
            self.cooldown_manager.set_cooldown(user, name, cooldown)

        return result

    # ---------------------------------------------------------
    # Damage Calculation
    # ---------------------------------------------------------

    def _calculate_damage(self, user: BattleEntity, target: BattleEntity, ability: Dict[str, Any]) -> float:
        """
        Simple placeholder formula:
        damage = (attack * power) - defense
        """

        power = ability["damage"]
        atk = user.stats.get("attack", 1)
        defense = target.stats.get("defense", 1)

        dmg = max(1, (atk * power) - defense)
        return float(dmg)
