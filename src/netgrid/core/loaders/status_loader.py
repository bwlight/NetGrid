import json
import os
from ..status import StatusCondition

STATUS_DIR = "src/netgrid/data/status"

def load_status_conditions():
    statuses = {}

    for filename in os.listdir(STATUS_DIR):
        if filename.endswith(".json"):
            path = os.path.join(STATUS_DIR, filename)
            with open(path, "r") as f:
                data = json.load(f)
                status = StatusCondition(data)
                statuses[status.id] = status

    return statuses
