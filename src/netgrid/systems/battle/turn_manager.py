# turn_manager.py V3

from typing import List, Optional, Callable
import random
from .battle_entity import BattleEntity


class TurnPhase:
    START_OF_TURN = "start_of_turn"
    ACTION = "action"
    END_OF_TURN = "end_of_turn"


class TurnManager:
    """
    Orchestrates the full turn cycle:
    - start-of-turn status + cooldown ticks
    - speed-based ordering
    - ability execution via AbilityResolver
    - end-of-turn DOTs, buffs, debuffs, and expiration
    """

    def __init__(
        self,
        battle_manager,
        status_engine,
        cooldown_manager,
        ability_resolver,
        rng: Optional[random.Random] = None,
        dev_log: Optional[Callable[[str], None]] = None,
    ):
        self.battle_manager = battle_manager
        self.status_engine = status_engine
        self.cooldown_manager = cooldown_manager
        self.ability_resolver = ability_resolver
        self.rng = rng or random.Random()
        self.dev_log = dev_log or (lambda msg: None)
        self.turn_number = 1

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def run_full_turn(self, entities: List["BattleEntity"]) -> None:
        self.dev_log(f"=== TURN {self.turn_number} START ===")

        alive = [e for e in entities if e.is_alive()]
        if not alive:
            self.dev_log("No living entities. Battle already resolved.")
            return

        self._start_of_turn_phase(alive)
        self._action_phase(alive)
        self._end_of_turn_phase(alive)

        self.dev_log(f"=== TURN {self.turn_number} END ===\n")
        self.turn_number += 1

    # -------------------------------------------------------------------------
    # Start-of-turn phase
    # -------------------------------------------------------------------------

    def _start_of_turn_phase(self, entities: List["BattleEntity"]) -> None:
        self.dev_log(f"[Phase] {TurnPhase.START_OF_TURN}")

        for entity in entities:
            if not entity.is_alive():
                continue

            self.dev_log(f"  - Start-of-turn for {entity.debug_name}")

            # Cooldowns tick first
            self.cooldown_manager.tick_cooldowns(entity)
            self.dev_log(f"    Cooldowns ticked for {entity.debug_name}")

            # Status start-of-turn effects (shields, locks, regen, etc.)
            self.status_engine.apply_start_of_turn_effects(entity, self.dev_log)

            # Clear transient flags (skip turn, immobilize, etc.)
            entity.clear_turn_flags()

    # -------------------------------------------------------------------------
    # Action phase
    # -------------------------------------------------------------------------

    def _action_phase(self, entities: List["BattleEntity"]) -> None:
        self.dev_log(f"[Phase] {TurnPhase.ACTION}")

        # Speed ordering (after buffs/debuffs)
        ordered = sorted(
            [e for e in entities if e.is_alive()],
            key=lambda e: (e.get_effective_stat("spd"), e.initiative_tiebreaker),
            reverse=True,
        )

        for actor in ordered:
            if not actor.is_alive():
                continue

            if actor.should_skip_turn():
                self.dev_log(f"  - {actor.debug_name} skips turn (locked or incapacitated).")
                continue

            # AI or player chooses ability + targets
            ability, targets = self.battle_manager.choose_action(actor, entities)
            if ability is None or not targets:
                self.dev_log(f"  - {actor.debug_name} has no valid action.")
                continue

            # Execute via AbilityResolver
            self.ability_resolver.execute(actor, ability, targets)

            # Check if battle ended mid-turn
            if self.battle_manager.is_battle_over(entities):
                self.dev_log("  - Battle ended during action phase.")
                break

    # -------------------------------------------------------------------------
    # End-of-turn phase
    # -------------------------------------------------------------------------

    def _end_of_turn_phase(self, entities: List["BattleEntity"]) -> None:
        self.dev_log(f"[Phase] {TurnPhase.END_OF_TURN}")

        for entity in entities:
            if not entity.is_alive():
                continue

            self.dev_log(f"  - End-of-turn for {entity.debug_name}")

            # DOT ticks, buff/debuff duration, expiration
            self.status_engine.apply_end_of_turn_effects(entity, self.dev_log)

            # KO check after DOTs
            if not entity.is_alive():
                self.dev_log(f"    {entity.debug_name} was KO'd by end-of-turn effects.")
