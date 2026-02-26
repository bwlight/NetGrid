from __future__ import annotations

from typing import List, Any, Dict

from turn_manager import TurnManager
from ability_manager import AbilityManager
from status_engine import StatusEngine
from cooldown_manager import CooldownManager


class BattleManager:
    """
    The orchestrator of the entire battle.
    Handles:
    - turn flow
    - ability execution
    - win/loss checks
    - logging
    """

    def __init__(
        self,
        combatants: List[Any],
        element_chart: Dict[str, Dict[str, float]]
    ):
        self.combatants = combatants
        self.turn_manager = TurnManager(combatants)
        self.status_engine = StatusEngine()
        self.cooldown_manager = CooldownManager()
        self.ability_manager = AbilityManager(element_chart)

        self.battle_log = []

    # ---------------------------------------------------------
    # MAIN BATTLE LOOP
    # ---------------------------------------------------------
    def run_turn(self, player_action_callback) -> Dict:
        """
        Runs a single turn of combat.
        player_action_callback(actor) -> (ability, target)
        """

        # 1. Determine whose turn it is
        actor = self.turn_manager.next_turn()
        if actor is None:
            return {"battle_over": True, "log": ["Battle ended."]}

        turn_log = [f"It is {actor.name}'s turn."]

        # 2. If actor is player, ask for input
        if actor.is_player:
            ability, target = player_action_callback(actor)
        else:
            ability, target = actor.choose_ai_action(self.combatants)

        # 3. Check cooldowns
        if not self.cooldown_manager.is_usable(actor, ability.id):
            turn_log.append(f"{ability.name} is on cooldown!")
            return {"battle_over": False, "log": turn_log}

        # 4. Execute ability
        result = self.ability_manager.execute(ability, actor, target)
        turn_log.extend(result.log)

        # 5. Apply cooldown
        self.cooldown_manager.apply_cooldown(actor, ability.id, ability.cooldown)

        # 6. Tick statuses (DOT/HOT)
        for c in self.combatants:
            status_logs = self.status_engine.tick_statuses(c)
            turn_log.extend(status_logs)

        # 7. Check win/loss
        if self._check_battle_end():
            turn_log.append("Battle finished!")
            return {"battle_over": True, "log": turn_log}

        return {"battle_over": False, "log": turn_log}

    # ---------------------------------------------------------
    # HELPERS
    # ---------------------------------------------------------
    def _check_battle_end(self) -> bool:
        alive = [c for c in self.combatants if c.is_alive()]
        return len(alive) <= 1
