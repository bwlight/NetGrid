from __future__ import annotations

from typing import List, Dict, Any

from .battle_entity import BattleEntity
from .turn_manager import TurnManager
from .ability_manager import AbilityManager
from .status_engine import StatusEngine
from .cooldown_manager import CooldownManager
from .ai_controller import AIController

# PartyManager is imported from the public API
from netgrid.core.systems.party import PartyManager


class BattleManager:
    """
    High-level orchestrator for battles.
    Handles:
    - Entity creation
    - Synergy and relationship modifiers
    - Turn sequencing
    - Ability execution
    - Win/loss conditions
    - Battle logs
    """

class BattleManager:
    def __init__(
        self,
        ability_loader=None,
        cyber_loader=None,
        ai_config=None,
        status_engine=None,
        cooldown_manager=None,
        turn_manager=None,
        party_manager=None,
    ):
        self.ability_loader = ability_loader
        self.cyber_loader = cyber_loader
        self.ai_config = ai_config
        self.status_engine = status_engine
        self.cooldown_manager = cooldown_manager
        self.turn_manager = turn_manager
        self.party_manager = party_manager

        from .ai_controller import AIController
        self.ai_controller = AIController(ai_config)

        self.entities = []
        self.active = False


    # ---------------------------------------------------------
    # Battle Setup
    # ---------------------------------------------------------

    def load_combatants(self, cyberkins: List[Any]) -> None:
        """
        Accepts Cyberkin objects and wraps them in BattleEntity.
        Applies synergy and relationship modifiers before battle starts.
        """
        self.entities = [BattleEntity(c) for c in cyberkins]

        # Apply synergy modifiers to stats
        synergy_stats = self.party_manager.apply_synergy_to_stats(
            {stat: 1.0 for stat in self.entities[0].stats.keys()}
        )

        for entity in self.entities:
            for stat, multiplier in synergy_stats.items():
                if stat in entity.stats:
                    entity.stats[stat] *= multiplier

        # Relationship-based evolution modifiers (future hook)

    # ---------------------------------------------------------
    # Battle Loop
    # ---------------------------------------------------------

    def run_battle(self) -> Dict[str, Any]:
        """
        Main battle loop.
        Returns a result dictionary containing:
        - winner
        - final states
        - battle log
        """

        while True:
            # Sort by speed
            turn_order = self.turn_manager.sort_by_speed(self.entities)

            for entity in turn_order:
                if not entity.is_alive():
                    continue

                # Start of turn
                self.turn_manager.begin_turn(entity)

                # Check immobilize status
                if hasattr(entity, "metadata") and entity.metadata.get("immobilized"):
                    self._log_event(entity.id, "immobilized")
                    continue

                # Choose target via AI
                target = self.ai_controller.choose_target(entity, self.entities)
                if target is None:
                    continue

                # Choose ability via AI
                ability = self.ai_controller.choose_ability(entity)

                if self.ability_manager.can_use(entity, ability):
                    result = self.ability_manager.execute(entity, target, ability)
                    self._log_action(entity.id, target.id, result)

                # End-of-turn hook
                self.turn_manager.end_turn(entity)

                # Check win/loss
                if self._battle_over():
                    return self._finalize_battle()

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _choose_target(self, user: BattleEntity) -> BattleEntity | None:
        for entity in self.entities:
            if entity is not user and entity.is_alive():
                return entity
        return None

    def _get_entity_by_id(self, entity_id: str) -> BattleEntity:
        return next(e for e in self.entities if e.id == entity_id)

    def _battle_over(self) -> bool:
        alive = [e for e in self.entities if e.is_alive()]
        return len(alive) <= 1

    def _finalize_battle(self) -> Dict[str, Any]:
        winner = next((e for e in self.entities if e.is_alive()), None)
        return {
            "winner": winner.id if winner else None,
            "final_states": {e.id: e.current_hp for e in self.entities},
            "log": self.battle_log,
        }

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

    def _log_event(self, entity_id: str, event: str) -> None:
        self.battle_log.append({"entity": entity_id, "event": event})

    def _log_action(self, user_id: str, target_id: str, result: Dict[str, Any]) -> None:
        entry = {
            "user": user_id,
            "target": target_id,
            "ability": result["ability"],
            "events": result["events"],
        }
        self.battle_log.append(entry)

        # Threat system integration
        for event in result["events"]:
            if event["type"] == "damage":
                self.ai_controller.add_threat(
                    source=self._get_entity_by_id(user_id),
                    target=self._get_entity_by_id(target_id),
                    amount=event["amount"]
                )

    def start_battle(self, entity1, entity2):
        """
        Initialize a simple 1v1 battle for runtime testing.
        """
        # Accept raw BattleEntity objects
        self.entities = [entity1, entity2]
        self.active = True

        # Reset HP and statuses
        for e in self.entities:
            e.current_hp = e.stats.get("hp", 1)
            e.hp = e.current_hp
            e.status_effects = []
            e.cooldowns = {}

        # Register entities with the turn manager
        if hasattr(self.turn_manager, "set_entities"):
            self.turn_manager.set_entities(self.entities)


    def execute_turn(self):
        """
        Execute a single simulated turn for runtime testing.
        """
        if not self.active:
            raise RuntimeError("Battle has not been started.")

        attacker = self.turn_manager.get_current_entity()
        defender = self.turn_manager.get_opponent(attacker)

        # AI chooses an ability
        ability_id = self.ai_controller.choose_ability(attacker, defender, self.ability_loader)
        ability = self.ability_loader.get(ability_id)

        # Apply ability (very simplified)
        damage = ability.get("power", 0)
        defender.current_hp -= damage
        defender.hp = defender.current_hp

        # Advance turn
        self.turn_manager.advance_turn()

        # Check victory
        if defender.current_hp <= 0:
            self.active = False
            return f"{attacker.name} wins!"

        return f"{attacker.name} used {ability_id}!"
    
    def take_turn(self):
        if not self.active:
            raise RuntimeError("Battle has not been started.")

        attacker = self.turn_manager.get_current_entity()
        defender = self.turn_manager.get_opponent(attacker)

        # AI chooses an ability
        ability_id = self.ai_controller.choose_ability(attacker, defender, self.ability_loader)

        # If no valid ability exists, skip turn
        if not ability_id:
            self.turn_manager.advance_turn()
            return f"{attacker.name} hesitates..."

        ability = self.ability_loader.get(ability_id)

        # Apply ability (object-based)
        damage = getattr(ability, "power", 0)
        defender.current_hp -= damage
        defender.hp = defender.current_hp

        # Advance turn
        self.turn_manager.advance_turn()

        # Check victory
        if defender.current_hp <= 0:
            self.active = False
            return f"{attacker.name} wins!"

        return f"{attacker.name} used {ability_id}!"
