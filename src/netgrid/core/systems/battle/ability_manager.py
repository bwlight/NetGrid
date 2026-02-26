from __future__ import annotations

import random
from typing import Dict, Any, Optional, Tuple

from netgrid.core.loaders.ability_loader import Ability


class AbilityResult:
    """
    Represents the complete outcome of using an ability.
    Returned to the battle engine for UI + logic.
    """

    def __init__(self):
        self.hits = []
        self.missed = False
        self.crit = False
        self.status_inflicted = None
        self.stat_changes = {}
        self.heal_amount = 0
        self.cooldown_applied = 0
        self.log = []  # battle log messages

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hits": self.hits,
            "missed": self.missed,
            "crit": self.crit,
            "status_inflicted": self.status_inflicted,
            "stat_changes": self.stat_changes,
            "heal_amount": self.heal_amount,
            "cooldown_applied": self.cooldown_applied,
            "log": self.log,
        }


class AbilityManager:
    """
    Executes abilities in battle.
    Handles:
    - accuracy
    - damage
    - crits
    - elemental multipliers
    - multi-hit
    - healing
    - stat modifiers
    - status effects
    - cooldowns
    - passive triggers
    """

    def __init__(self, element_chart: Dict[str, Dict[str, float]]):
        """
        element_chart example:
        {
            "core": {"root": 1.2, "void": 0.8},
            "root": {"pulse": 1.2},
            ...
        }
        """
        self.element_chart = element_chart

    # ---------------------------------------------------------
    # MAIN ENTRY POINT
    # ---------------------------------------------------------
    def execute(
        self,
        ability: Ability,
        user: Any,
        target: Any
    ) -> AbilityResult:

        result = AbilityResult()

        # 1. Accuracy check
        if not self._passes_accuracy(ability):
            result.missed = True
            result.log.append(f"{user.name}'s {ability.name} missed!")
            return result

        # 2. Cooldown application
        result.cooldown_applied = ability.cooldown
        user.apply_cooldown(ability.id, ability.cooldown)

        # 3. Multi-hit loop
        hits = ability.effects.get("multi_hit", 1)

        for _ in range(hits):
            if ability.type == "attack":
                dmg, crit = self._calculate_damage(ability, user, target)
                result.crit = result.crit or crit
                target.current_hp = max(0, target.current_hp - dmg)
                result.hits.append(dmg)

        # 4. Healing
        heal_percent = ability.effects.get("heal_percent", 0)
        if heal_percent > 0:
            heal_amount = int(user.max_hp * heal_percent)
            user.current_hp = min(user.max_hp, user.current_hp + heal_amount)
            result.heal_amount = heal_amount
            result.log.append(f"{user.name} restored {heal_amount} HP!")

        # 5. Stat modifiers
        stat_mods = ability.effects.get("stat_modifiers", {})
        if stat_mods:
            for stat, amount in stat_mods.items():
                self._apply_stat_modifier(target, stat, amount)
                result.stat_changes[stat] = amount
                result.log.append(f"{target.name}'s {stat} changed by {amount * 100:.0f}%")

        # 6. Status infliction
        status = ability.effects.get("status_inflict")
        chance = ability.effects.get("status_chance", 0)

        if status and random.random() <= chance:
            target.apply_status(status)
            result.status_inflicted = status
            result.log.append(f"{target.name} is now afflicted with {status}!")

        return result

    # ---------------------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------------------

    def _passes_accuracy(self, ability: Ability) -> bool:
        return random.random() <= ability.accuracy

    def _calculate_damage(self, ability: Ability, user: Any, target: Any) -> Tuple[int, bool]:
        """
        Full damage formula including:
        - base power
        - ATK/DEF scaling
        - elemental multipliers
        - crit chance
        """

        base = ability.power
        atk = user.stats.get("ATK", 10)
        defense = target.stats.get("DEF", 10)

        # 1. Base damage
        dmg = (atk / defense) * base

        # 2. Elemental multiplier
        multiplier = self._element_multiplier(ability.element, target.element)
        dmg *= multiplier

        # 3. Crit chance (10% default)
        crit = random.random() <= 0.10
        if crit:
            dmg *= 1.5

        return max(1, int(dmg)), crit

    def _element_multiplier(self, atk_element: str, def_element: str) -> float:
        if atk_element in self.element_chart:
            return self.element_chart[atk_element].get(def_element, 1.0)
        return 1.0

    def _apply_stat_modifier(self, target: Any, stat: str, amount: float):
        if stat not in target.stats:
            return

        original = target.stats[stat]
        modified = int(original * (1 + amount))
        target.stats[stat] = max(1, modified)
