import json

def load_travel_map(path):
    with open(path, "r") as f:
        data = json.load(f)

    return {
        "routes": data.get("routes", []),
        "travel_rules": data.get("travel_rules", {}),
        "connections": data.get("connections", {}),
        "path_types": data.get("path_types", {})
    }
