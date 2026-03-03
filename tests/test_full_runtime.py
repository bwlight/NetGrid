# tests/test_full_runtime.py

import random

from src.netgrid.core.systems.battle.ability_loader import AbilityLoader
from src.netgrid.core.systems.battle.ability_manager import AbilityManager
from src.netgrid.core.loaders.status_loader import StatusLoader
from src.netgrid.core.systems.battle.status_engine import StatusEngine
from src.netgrid.core.models.cyberkin.cyberkin_loader import CyberkinLoader
from src.netgrid.core.systems.battle.battle_entity import BattleEntity
from src.netgrid.core.systems.battle.battle_manager import BattleManager
from src.netgrid.core.systems.battle.turn_manager import TurnManager
from src.netgrid.core.systems.battle.ai_controller import AIController
from src.netgrid.core.systems.battle.ability_resolver import AbilityResolver
from src.netgrid.core.systems.battle.cooldown_manager import CooldownManager


def dev_log(msg: str):
    print(msg)


def test_full_runtime():
    rng = random.Random(42)

    # ---------------------------------------------------------
    # Load abilities
    # ---------------------------------------------------------
    ability_manager = AbilityManager()
    ability_loader = AbilityLoader("data/abilities/")
    loaded_abilities = ability_loader.load_all()

    # AbilityManager stores dicts, not Ability objects
    ability_manager.register_many([a.to_dict() for a in loaded_abilities])

    # ---------------------------------------------------------
    # Load statuses
    # ---------------------------------------------------------
    status_loader = StatusLoader("data/status/")
    status_library = status_loader.load_all()
    status_engine = StatusEngine(status_library)

    # ---------------------------------------------------------
    # Load Cyberkin
    # ---------------------------------------------------------
    cyberkin_loader = CyberkinLoader("data/cyberkin/", ability_manager)
    cyberkin_library = cyberkin_loader.load_all()

    ck_list = list(cyberkin_library.values())
    assert len(ck_list) >= 2, "Need at least two Cyberkin for runtime test."

    ck1 = ck_list[0]
    ck2 = ck_list[1]

    # ---------------------------------------------------------
    # Create BattleEntities
    # ---------------------------------------------------------
    e1 = BattleEntity(ck1)
    e2 = BattleEntity(ck2)
    entities = [e1, e2]

    # ---------------------------------------------------------
    # Create AI + Managers
    # ---------------------------------------------------------
    ai = AIController(rng=rng, dev_log=dev_log)
    cooldown_manager = CooldownManager()

    battle_manager = BattleManager(
        status_engine=status_engine,
        cooldown_manager=cooldown_manager,
        ai_controller=ai,
        rng=rng,
        dev_log=dev_log,
    )

    ability_resolver = AbilityResolver(
        battle_manager=battle_manager,
        status_engine=status_engine,
        cooldown_manager=cooldown_manager,
        rng=rng,
        dev_log=dev_log,
    )

    turn_manager = TurnManager(
        battle_manager=battle_manager,
        status_engine=status_engine,
        cooldown_manager=cooldown_manager,
        ability_resolver=ability_resolver,
        rng=rng,
        dev_log=dev_log,
    )

    # ---------------------------------------------------------
    # Run battle loop
    # ---------------------------------------------------------
    turn = 1
    max_turns = 50  # safety guard

    while turn <= max_turns:
        dev_log(f"\n===== TURN {turn} =====")
        turn_manager.run_full_turn(entities)

        if battle_manager.is_battle_over(entities):
            dev_log("Battle finished successfully.")
            return

        turn += 1

    assert False, "Battle did not end within 50 turns."
