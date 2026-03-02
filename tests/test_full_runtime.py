import json
from src.netgrid.core.models.cyberkin.cyberkin_loader import CyberkinLoader
from src.netgrid.core.systems.battle.ability_loader import AbilityLoader
from src.netgrid.core.loaders.ai_behavior_loader import AIBehaviorLoader
from src.netgrid.core.systems.battle.battle_manager import BattleManager
from src.netgrid.core.systems.battle.battle_entity import BattleEntity
from src.netgrid.core.systems.battle.ai_controller import AIController

def test_full_runtime():
    # Load Cyberkin JSON
    with open("data/cyberkin/EMBERBIT.json", "r") as f:
        raw_data = json.load(f)

    # Loaders
    cyberkin_loader = CyberkinLoader("schemas/cyberkin.schema.json")
    ability_loader = AbilityLoader("schemas/ability.schema.json")
    ai_loader = AIBehaviorLoader("schemas/ai_behavior.schema.json")

    # Load Cyberkin object
    cyberkin = cyberkin_loader.apply(raw_data)

    # Load abilities
    ability_loader.apply(cyberkin)

    # Load AI behavior
    ai_loader.apply(raw_data, cyberkin)

    # Wrap Cyberkin into a BattleEntity
    entity = BattleEntity(cyberkin)

    # Create a dummy opponent
    dummy_data = {
        "id": "DUMMY",
        "name": "Dummy",
        "stats": {"hp": 100, "attack": 1, "defense": 1, "speed": 1},
        "abilities": [],
        "evolution": None,
        "personality": "neutral"
    }
    dummy = cyberkin_loader.apply(dummy_data)
    dummy_entity = BattleEntity(dummy)

    # Create battle manager
    battle = BattleManager([entity], [dummy_entity])

    # AI Controller
    ai = AIController()

    # Simulate one turn
    chosen_ability, target = ai.choose_action(entity, battle)

    print("\n=== Integration Test Output ===")
    print("Chosen Ability:", chosen_ability)
    print("Target:", target.cyberkin.id if target else None)
    print("Active AI Phase:", entity.cyberkin.active_ai_phase)
    print("AI Warnings:", entity.cyberkin.ai_warnings)

    # Assertions
    assert chosen_ability is not None
    assert target is not None
    assert isinstance(entity.cyberkin.ai, dict)
    assert entity.cyberkin.active_ai_phase is None or isinstance(entity.cyberkin.active_ai_phase, str)
    assert isinstance(entity.cyberkin.ai_warnings, list)