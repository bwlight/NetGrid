import json
import os
from ..cyberkin import Cyberkin

CYBERKIN_DIR = "src/netgrid/data/cyberkin"

def load_cyberkin():
    cyberkin = {}

    for filename in os.listdir(CYBERKIN_DIR):
        if filename.endswith(".json"):
            path = os.path.join(CYBERKIN_DIR, filename)
            with open(path, "r") as f:
                data = json.load(f)

                # unwrap the "cyberkin" key
                family_data = data["cyberkin"]

                # instantiate Cyberkin object
                ck = Cyberkin(family_data)

                cyberkin[ck.family_id] = ck

    return cyberkin
