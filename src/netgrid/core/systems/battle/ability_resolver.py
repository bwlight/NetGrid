# ability_resolver.py

from typing import List, Callable
import random
from .battle_entity import BattleEntity


class AbilityResolver:
    """
    Executes abilities according to the canonical ability schema.
    Handles:
    - accuracy
    - multi-hit
    - damage
    - stat modifiers
    - status application
    - shield reduction (delegated to BattleManager)
    """

    def __init__(self, battle_manager, status_engine, cooldown_manager,
                 rng: random.Random = None, dev_log: Callable[[str], None] = None):
        self.battle_manager = battle_manager
        self.status_engine = status_engine
        self.cooldown_manager = cooldown_manager
        self.rng = rng or random.Random()
        self.dev_log = dev_log or (lambda msg: None)

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def execute(self, actor, ability: dict, targets: List["BattleEntity"]) -> None:
        """
        Executes a single ability on one or more targets.
        """
        name = ability["name"]
        self.dev_log(f"  - {actor.debug_name} uses {name}")

        # Start cooldown immediately
        self.cooldown_manager.start_cooldown(actor, ability)

        # Determine hit count
        hits = self._determine_hit_count(ability)

        for hit_index in range(1, hits + 1):
            is_support = ability["type"] == "support" or ability["power"] is None

            for target in targets:
                if not target.is_alive():
                    continue

                # Accuracy roll for attack abilities
                if not is_support:
                    if not self._roll_accuracy(actor, target, ability):
                        self.dev_log(
                            f"    Hit {hit_index}: {actor.debug_name}'s {name} missed {target.debug_name}"
                        )
                        continue

                    # Damage calculation + shield reduction
                    damage = self.battle_manager.calculate_damage(actor, target, ability)
                    self.dev_log(
                        f"    Hit {hit_index}: {actor.debug_name}'s {name} deals {damage} to {target.debug_name}"
                    )
                    self.battle_manager.apply_damage(target, damage)

                    if not target.is_alive():
                        self.dev_log(f"      {target.debug_name} is KO'd.")
                        continue

                # Stat modifiers (buffs/debuffs)
                stat_mods = ability.get("stat_modifiers") or {}
                if stat_mods:
                    self.dev_log(
                        f"    Hit {hit_index}: applying stat modifiers from {name} to {target.debug_name}: {stat_mods}"
                    )
                    self.status_engine.apply_instant_stat_modifiers(actor, target, stat_mods, self.dev_log)

                # Status application
                status_id = ability.get("status_inflict")
                status_chance = ability.get("status_chance")
                if status_id and status_chance is not None:
                    if self._roll_status(status_chance):
                        self.dev_log(
                            f"    Hit {hit_index}: {name} inflicts status {status_id} on {target.debug_name}"
                        )
                        self.status_engine.apply_status(actor, target, status_id, self.dev_log)
                    else:
                        self.dev_log(
                            f"    Hit {hit_index}: {name} failed to inflict status {status_id} on {target.debug_name}"
                        )

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _determine_hit_count(self, ability: dict) -> int:
        multi = ability.get("multi_hit")
        if not multi:
            return 1
        min_hits = multi.get("min", 1)
        max_hits = multi.get("max", min_hits)
        if min_hits == max_hits:
            return min_hits
        return self.rng.randint(min_hits, max_hits)

    def _roll_accuracy(self, actor, target, ability: dict) -> bool:
        base_acc = ability.get("accuracy", 1.0)
        roll = self.rng.random()
        self.dev_log(
            f"      Accuracy roll: {roll:.3f} vs {base_acc:.3f} "
            f"({actor.debug_name} -> {target.debug_name})"
        )
        return roll <= base_acc

    def _roll_status(self, chance: float) -> bool:
        roll = self.rng.random()
        self.dev_log(f"      Status roll: {roll:.3f} vs {chance:.3f}")
        return roll <= chance
