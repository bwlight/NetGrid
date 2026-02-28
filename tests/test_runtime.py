import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)




"""
NetGrid Runtime Initialization Test
Run with: python tests/test_runtime.py
"""

def test_runtime_initialization():
    print("=== NetGrid Runtime Test ===")

    # -----------------------------
    # Load Ability Data
    # -----------------------------
    print("Loading abilities...")
    from netgrid.core.systems.battle import AbilityLoader
    ability_loader = AbilityLoader(base_path="data/abilities")
    print(f"Loaded {len(ability_loader.abilities)} abilities.")

    # -----------------------------
    # Load Cyberkin Data
    # -----------------------------
    print("Loading cyberkin...")
    from netgrid.core.models.cyberkin import CyberkinLoader
    cyber_loader = CyberkinLoader(ability_loader, index_path="data/cyberkin_index.json")
    print(f"Loaded {len(cyber_loader.cyberkin)} cyberkin.")

    ids = list(cyber_loader.cyberkin.keys())
    c1 = cyber_loader.get(ids[0])
    c2 = cyber_loader.get(ids[1])

    print(f"Selected Cyberkin: {c1.name} vs {c2.name}")

    # -----------------------------
    # Wrap Cyberkin in BattleEntities
    # -----------------------------
    print("Creating battle entities...")
    from netgrid.core.systems.battle import BattleEntity
    e1 = BattleEntity(c1)
    e2 = BattleEntity(c2)

    print(f"{e1.name}: HP={e1.hp}, ATK={e1.stats['attack']}")
    print(f"{e2.name}: HP={e2.hp}, ATK={e2.stats['attack']}")

    # -----------------------------
    # Load AI Config
    # -----------------------------
    print("Loading AI config...")
    from netgrid.core.systems.battle import AIConfigLoader
    ai_config = AIConfigLoader(path="data/ai/ai_config.json")
    print("AI config loaded.")

    # -----------------------------
    # Initialize Battle Subsystems
    # -----------------------------
    print("Initializing battle subsystems...")
    from netgrid.core.systems.battle import (
        StatusEngine,
        CooldownManager,
        TurnManager,
        BattleManager,
    )

    status_engine = StatusEngine()
    cooldowns = CooldownManager()
    turn_manager = TurnManager(status_engine, cooldowns)

    battle = BattleManager(
        ability_loader=ability_loader,
        ai_config=ai_config,
        status_engine=status_engine,
        cooldown_manager=cooldowns,
        turn_manager=turn_manager,
    )

    print("BattleManager initialized.")

    # -----------------------------
    # Run a Simulated Turn
    # -----------------------------
    print("Running a simulated turn...")
    battle.start_battle(e1, e2)
    battle.take_turn()

    print("Turn executed successfully.")
    print("=== Runtime Test Complete ===")


# Make the test run when executed directly
if __name__ == "__main__":
    test_runtime_initialization()
