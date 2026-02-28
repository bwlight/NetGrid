from __future__ import annotations

from typing import List
from .battle_entity import BattleEntity
from .status_engine import StatusEngine
from .cooldown_manager import CooldownManager


class TurnManager:
    """
    Handles turn sequencing, speed ordering, and per-turn updates.
    Designed to work with BattleEntity objects and future systems
    like synergy, corruption, resonance, and evolution triggers.
    """

    def __init__(self, status_engine: StatusEngine, cooldown_manager: CooldownManager):
        self.status_engine = status_engine
        self.cooldown_manager = cooldown_manager
        self.entities = []
        self.current_index = 0
    
    def set_entities(self, entities): 
        """ Register the two battle entities. """ 
        self.entities = entities
        self.current_index = 0
    
    def get_current_entity(self): 
            """ Return the entity whose turn it is. """ 
            if not self.entities: 
                raise RuntimeError("TurnManager has no entities registered.") 
            return self.entities[self.current_index]

    def get_opponent(self, entity): 
        """ Return the opposing entity. """ 
        if len(self.entities) != 2: 
            raise RuntimeError("TurnManager only supports 1v1 battles.") 
        return self.entities[1] if self.entities[0] == entity else self.entities[0]
 
    def advance_turn(self): 
        """ Move to the next entity. """ 
        if not self.entities: 
            raise RuntimeError("TurnManager has no entities registered.") 
        self.current_index = (self.current_index + 1) % len(self.entities)

    # ---------------------------------------------------------
    # Turn Order
    # ---------------------------------------------------------

    def sort_by_speed(self, entities: List[BattleEntity]) -> List[BattleEntity]:
        """
        Returns entities sorted by speed descending.
        Future-proof: speed may be modified by synergy, buffs, debuffs, or corruption.
        """
        return sorted(entities, key=lambda e: e.stats.get("speed", 1), reverse=True)

    # ---------------------------------------------------------
    # Turn Start
    # ---------------------------------------------------------

    def begin_turn(self, entity: BattleEntity) -> None:
        """
        Called at the start of a creature's turn.
        Applies status effects, ticks cooldowns, and handles energy gain.
        """

        # Clear immobilize flag each turn (StatusEffect will reapply if needed)
        if "immobilized" in entity.metadata:
            del entity.metadata["immobilized"]

        # Status effects (DOT, HOT, buffs, debuffs, immobilize, etc.)
        logs = self.status_engine.update_statuses(entity)
        # (Optional) You can forward logs to BattleManager later

        # Cooldowns
        self.cooldown_manager.tick(entity)

        # Energy gain (placeholder — BattleManager may override this later)
        entity.energy += 1

    # ---------------------------------------------------------
    # Turn End (optional future hook)
    # ---------------------------------------------------------

    def end_turn(self, entity: BattleEntity) -> None:
        """
        Optional hook for end-of-turn effects.
        Useful for corruption decay, resonance charge, or lingering effects.
        """
        pass

    # ---------------------------------------------------------
    # Battle End Checks
    # ---------------------------------------------------------

    def all_dead(self, entities: List[BattleEntity]) -> bool:
        return all(not e.is_alive() for e in entities)

    def any_dead(self, entities: List[BattleEntity]) -> bool:
        return any(not e.is_alive() for e in entities)

