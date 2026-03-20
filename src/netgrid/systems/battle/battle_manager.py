# battle_manager.py

from typing import List, Tuple, Optional, Callable
import random
from .battle_entity import BattleEntity


class BattleManager:
    """
    Central orchestrator for battle logic.
    Handles:
    - action selection (AI or player)
    - damage calculation
    - shield reduction (via StatusEngine)
    - KO checks
    - battle end conditions
    """

    def __init__(
        self,
        status_engine,
        cooldown_manager,
        ai_controller,
        rng: Optional[random.Random] = None,
        dev_log: Optional[Callable[[str], None]] = None,
    ):
        self.status_engine = status_engine
        self.cooldown_manager = cooldown_manager
        self.ai_controller = ai_controller
        self.rng = rng or random.Random()
        self.dev_log = dev_log or (lambda msg: None)

    # -------------------------------------------------------------------------
    # Action Selection
    # -------------------------------------------------------------------------

    def choose_action(self, actor, entities: List["BattleEntity"]) -> Tuple[Optional[dict], List["BattleEntity"]]:
        """
        Returns (ability, targets).
        Delegates to AI for now, but can support player input later.
        """
        return self.ai_controller.choose_action(actor, entities, self)

    # -------------------------------------------------------------------------
    # Damage Calculation
    # -------------------------------------------------------------------------

    def calculate_damage(self, attacker, defender, ability: dict) -> int:
        """
        Canon damage formula:
            damage = power * (atk / def) * elemental_multiplier * variance
        """
        power = ability.get("power", 0)
        if power is None:
            return 0

        atk = attacker.get_effective_stat("atk")
        defense = max(1, defender.get_effective_stat("def"))

        base = power * (atk / defense)

        # Elemental multiplier (placeholder for now)
        multiplier = self._elemental_multiplier(attacker, defender, ability)

        # Random variance (±10%)
        variance = self.rng.uniform(0.9, 1.1)

        damage = int(base * multiplier * variance)
        return max(1, damage)

    def _elemental_multiplier(self, attacker, defender, ability):
        """
        Placeholder for your future elemental chart.
        Always returns 1.0 for now.
        """
        return 1.0

    # -------------------------------------------------------------------------
    # Damage Application
    # -------------------------------------------------------------------------

    def apply_damage(self, defender, amount: int) -> None:
        """
        Applies shield reduction first, then damage.
        """
        reduced = self.status_engine.apply_shield_reduction(defender, amount, self.dev_log)
        defender.apply_damage(reduced)

    # -------------------------------------------------------------------------
    # KO and Battle End Logic
    # -------------------------------------------------------------------------

    def is_battle_over(self, entities: List["BattleEntity"]) -> bool:
        """
        Returns True if one side has no living members.
        """
        teams = {}
        for e in entities:
            team = getattr(e.cyberkin, "team", "A")
            teams.setdefault(team, []).append(e)

        alive_by_team = {team: [e for e in members if e.is_alive()] for team, members in teams.items()}

        # If any team has 0 alive, battle ends
        for team, alive in alive_by_team.items():
            if len(alive) == 0:
                self.dev_log(f"Battle over: Team {team} has no remaining Cyberkin.")
                return True

        return False

    # -------------------------------------------------------------------------
    # Utility
    # -------------------------------------------------------------------------

    def get_living_entities(self, entities: List["BattleEntity"]) -> List["BattleEntity"]:
        return [e for e in entities if e.is_alive()]
