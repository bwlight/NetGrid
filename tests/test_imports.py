"""
NetGrid Engine Import Test
Run with:  python -m tests.test_imports
"""

def test_core_imports():
    import netgrid.core
    import netgrid.core.models
    import netgrid.core.systems
    import netgrid.core.loaders

def test_cyberkin_model():
    from netgrid.core.models.cyberkin import Cyberkin, CyberkinLoader

def test_battle_system_imports():
    from netgrid.core.systems.battle import (
        BattleManager,
        BattleEntity,
        AbilityManager,
        AbilityLoader,
        AIController,
        AIConfigLoader,
        StatusEngine,
        StatusEffect,
        CooldownManager,
        TurnManager,
    )

def test_party_system():
    from netgrid.core.systems.party import PartyManager

def test_ability_loader():
    from netgrid.core.systems.battle import AbilityLoader
    loader = AbilityLoader(base_path="data/abilities")
    assert isinstance(loader.abilities, dict)

def test_cyberkin_loader():
    from netgrid.core.models.cyberkin import CyberkinLoader
    from netgrid.core.systems.battle import AbilityLoader

    ability_loader = AbilityLoader(base_path="data/abilities")
    cyber_loader = CyberkinLoader(ability_loader, base_path="data/cyberkin")

    assert len(cyber_loader.cyberkins) > 0

def test_battle_entity_creation():
    from netgrid.core.systems.battle import BattleEntity
    from netgrid.core.models.cyberkin import Cyberkin

    c = Cyberkin(
        id="test",
        name="Testmon",
        stats={"hp": 10, "attack": 5, "defense": 3, "speed": 2},
        abilities=[],
    )

    entity = BattleEntity(c)
    assert entity.hp == 10
    assert entity.stats["attack"] == 5

def test_battle_manager_instantiation():
    from netgrid.core.systems.battle import (
        BattleManager,
        AbilityLoader,
        AIConfigLoader,
        StatusEngine,
        CooldownManager,
        TurnManager,
    )

    ability_loader = AbilityLoader(base_path="data/abilities")
    ai_config = AIConfigLoader(base_path="data/ai/ai_config.json")
    status_engine = StatusEngine()
    cooldowns = CooldownManager()
    turn_manager = TurnManager(status_engine, cooldowns)

    manager = BattleManager(
        ability_loader=ability_loader,
        ai_config=ai_config,
        status_engine=status_engine,
        cooldown_manager=cooldowns,
        turn_manager=turn_manager,
    )

    assert manager is not None

print("All import tests passed!")