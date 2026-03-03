# tests/conftest.py

import random
import pytest

from src.netgrid.core.systems.battle.ability_loader import AbilityLoader
from src.netgrid.core.systems.battle.ability_manager import AbilityManager
from src.netgrid.core.loaders.status_loader import StatusLoader
from src.netgrid.core.systems.battle.status_engine import StatusEngine
from src.netgrid.core.models.cyberkin.cyberkin_loader import CyberkinLoader


@pytest.fixture(scope="session")
def rng():
    return random.Random(42)


@pytest.fixture(scope="session")
def ability_manager():
    manager = AbilityManager()
    loader = AbilityLoader("data/abilities/")
    abilities = loader.load_all()
    manager.register_many([a.to_dict() for a in abilities])
    return manager


@pytest.fixture(scope="session")
def status_engine():
    loader = StatusLoader("data/status/")
    status_library = loader.load_all()
    return StatusEngine(status_library)


@pytest.fixture(scope="session")
def cyberkin_library(ability_manager):
    loader = CyberkinLoader("data/cyberkin/", ability_manager)
    return loader.load_all()


@pytest.fixture
def two_cyberkin(cyberkin_library):
    ck_list = list(cyberkin_library.values())
    assert len(ck_list) >= 2, "Need at least two Cyberkin for runtime tests."
    return ck_list[0], ck_list[1]
