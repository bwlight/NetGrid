# status_engine.py

from typing import Callable, Dict
from .status_effect import StatusEffect


class StatusEngine:
    """
    Applies and manages all status effects in battle.
    Uses:
      - StatusEffect (immutable definition)
      - Runtime instances stored on BattleEntity:
            entity.statuses[status_id] = {
                "effect": StatusEffect,
                "duration": int,
                "shield_value": int (optional),
                ...
            }
    """

    def __init__(self, status_library: Dict[str, StatusEffect]):
        """
        status_library: dict of status_id -> StatusEffect object
        """
        self.status_library = status_library

    # -------------------------------------------------------------------------
    # Status Application
    # -------------------------------------------------------------------------

    def apply_status(self, source, target, status_id: str, log: Callable[[str], None]):
        """Applies a status to a target, respecting uniqueness and schema rules."""
        if status_id not in self.status_library:
            log(f"      ERROR: Status '{status_id}' not found.")
            return

        effect: StatusEffect = self.status_library[status_id]

        # Unique statuses cannot stack
        if effect.unique and status_id in target.statuses:
            log(f"      {target.debug_name} already has unique status {status_id}. Refreshing duration.")
            target.statuses[status_id]["duration"] = effect.duration
            return

        # Create runtime instance
        instance = {
            "effect": effect,
            "duration": effect.duration,
        }

        # Shields get runtime HP
        if effect.is_shield():
            instance["shield_value"] = effect.shield_value or 0

        target.statuses[status_id] = instance
        log(f"      {target.debug_name} gains status {status_id} ({effect.type}).")

    def apply_instant_stat_modifiers(self, source, target, modifiers: dict, log):
        """Applies immediate stat changes from abilities (not persistent statuses)."""
        for stat, value in modifiers.items():
            target.modify_stat(stat, value)
            log(f"      {target.debug_name}'s {stat} modified by {value:+.2f}")

    # -------------------------------------------------------------------------
    # Start-of-turn Phase
    # -------------------------------------------------------------------------

    def apply_start_of_turn_effects(self, entity, log):
        """Handles shield decay, lock behavior, regen, and other start-phase logic."""
        for status_id, inst in entity.statuses.items():
            effect: StatusEffect = inst["effect"]

            # Shield decay
            if effect.is_shield() and effect.shield_decay:
                inst["shield_value"] -= effect.shield_decay
                log(f"      Shield {status_id} decays by {effect.shield_decay}.")

                if inst["shield_value"] <= 0:
                    log(f"      Shield {status_id} on {entity.debug_name} breaks.")
                    entity.remove_status(status_id)
                    continue

            # Lock behavior
            if effect.is_lock():
                entity.set_skip_turn(True)
                log(f"      {entity.debug_name} is locked by {status_id} and cannot act this turn.")

    # -------------------------------------------------------------------------
    # End-of-turn Phase
    # -------------------------------------------------------------------------

    def apply_end_of_turn_effects(self, entity, log):
        """Handles DOT ticks, buff/debuff duration, and expiration."""
        expired = []

        for status_id, inst in entity.statuses.items():
            effect: StatusEffect = inst["effect"]

            # DOT damage
            if effect.is_dot() and effect.tick_damage:
                log(f"      DOT: {entity.debug_name} takes {effect.tick_damage} from {status_id}.")
                entity.apply_damage(effect.tick_damage)

            # Duration countdown
            inst["duration"] -= 1
            if inst["duration"] <= 0:
                expired.append(status_id)

        # Remove expired statuses
        for status_id in expired:
            self._expire_status(entity, status_id, log)

    # -------------------------------------------------------------------------
    # Shield Logic
    # -------------------------------------------------------------------------

    def apply_shield_reduction(self, entity, incoming_damage: int, log) -> int:
        """
        Called by BattleManager before applying damage.
        Returns reduced damage after shield effects.
        """
        for status_id, inst in entity.statuses.items():
            effect: StatusEffect = inst["effect"]

            if not effect.is_shield():
                continue

            shield_hp = inst.get("shield_value", 0)
            if shield_hp <= 0:
                continue

            reduced = max(0, incoming_damage - shield_hp)
            log(f"      Shield {status_id} reduces damage from {incoming_damage} to {reduced}.")
            return reduced

        return incoming_damage

    # -------------------------------------------------------------------------
    # Expiration
    # -------------------------------------------------------------------------

    def _expire_status(self, entity, status_id: str, log):
        """Removes a status and reverses persistent effects."""
        inst = entity.statuses.get(status_id)
        if not inst:
            return

        effect: StatusEffect = inst["effect"]

        # Reverse stat modifiers
        if effect.stat_modifiers:
            for stat, value in effect.stat_modifiers.items():
                entity.modify_stat(stat, -value)
                log(f"      {entity.debug_name}'s {stat} returns to normal (expired {status_id}).")

        entity.remove_status(status_id)
        log(f"      {entity.debug_name}'s status {status_id} has expired.")
