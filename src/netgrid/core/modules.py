from __future__ import annotations

from netgrid.core.systems.battle.battle_manager import BattleManager
from netgrid.core.systems.battle.ability_manager import AbilityManager
from netgrid.core.systems.battle.turn_manager import TurnManager
from netgrid.core.systems.battle.status_engine import StatusEngine
from netgrid.core.systems.battle.cooldown_manager import CooldownManager

from netgrid.core.systems.party.core.party_manager import PartyManager
from netgrid.core.systems.party.core.relationship_system import RelationshipSystem
from netgrid.core.systems.party.core.synergy_calculator import SynergyCalculator


class EngineModules:
    """
    Central registry for all major engine subsystems.
    """

    def __init__(self, element_chart):
        self.battle = BattleManager
        self.ability = AbilityManager(element_chart)
        self.turns = TurnManager
        self.status = StatusEngine()
        self.cooldowns = CooldownManager()

        self.party = PartyManager
        self.relationships = RelationshipSystem
        self.synergy = SynergyCalculator
