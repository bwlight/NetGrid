from __future__ import annotations

from typing import List, Any, Optional


class TurnManager:
    """
    Controls turn order, SPD priority, cooldown ticking,
    status ticking, and determining whose turn it is.
    """

    def __init__(self, combatants: List[Any]):
        """
        combatants: list of Cyberkin or battlers
        Each must have:
        - name
        - stats["SPD"]
        - current_hp
        - is_alive()
        - cooldowns (dict)
        - statuses (list)
        """
        self.combatants = combatants
        self.turn_index = 0

        # Sort by SPD descending
        self.combatants.sort(key=lambda c: c.stats.get("SPD", 10), reverse=True)

    # ---------------------------------------------------------
    # MAIN LOOP
    # ---------------------------------------------------------
    def next_turn(self) -> Optional[Any]:
        """
        Returns the next combatant whose turn it is.
        Handles:
        - skipping dead units
        - skipping immobilized units
        - ticking cooldowns
        - ticking statuses
        """

        if not any(c.is_alive() for c in self.combatants):
            return None  # battle is over

        while True:
            actor = self.combatants[self.turn_index]

            # Advance turn index for next call
            self.turn_index = (self.turn_index + 1) % len(self.combatants)

            # Skip dead units
            if not actor.is_alive():
                continue

            # Tick cooldowns + statuses
            self._tick_cooldowns(actor)
            self._tick_statuses(actor)

            # Skip immobilized units
            if actor.has_status("immobilized"):
                actor.consume_status("immobilized")
                continue

            return actor

    # ---------------------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------------------

    def _tick_cooldowns(self, actor: Any):
        """
        Reduces all cooldowns by 1.
        Removes abilities whose cooldown reaches 0.
        """
        to_remove = []
        for ability_id, turns in actor.cooldowns.items():
            new_value = turns - 1
            if new_value <= 0:
                to_remove.append(ability_id)
            else:
                actor.cooldowns[ability_id] = new_value

        for ability_id in to_remove:
            del actor.cooldowns[ability_id]

    def _tick_statuses(self, actor: Any):
        """
        Ticks down status durations.
        Applies DOT/HOT effects if present.
        """
        expired = []

        for status in actor.statuses:
            status.duration -= 1

            # DOT
            if status.type == "dot":
                dmg = status.value
                actor.current_hp = max(0, actor.current_hp - dmg)

            # HOT
            if status.type == "hot":
                heal = status.value
                actor.current_hp = min(actor.max_hp, actor.current_hp + heal)

            if status.duration <= 0:
                expired.append(status)

        for s in expired:
            actor.statuses.remove(s)
