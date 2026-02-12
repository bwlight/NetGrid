import json
import os
from ..abilities import Ability

ABILITY_DIR = "src/netgrid/data/abilities"

def load_abilities():
    abilities = {}

    for filename in os.listdir(ABILITY_DIR):
        if filename.endswith(".json"):
            path = os.path.join(ABILITY_DIR, filename)
            with open(path, "r") as f:
                data = json.load(f)
                ability = Ability(data)
                abilities[ability.id] = ability

    return abilities
