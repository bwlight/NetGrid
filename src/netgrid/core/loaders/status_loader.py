import json
import os
from jsonschema import validate, ValidationError

class StatusEffect:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.duration = data["duration"]
        self.tick_damage = data["tick_damage"]
        self.description = data["description"]

        # Optional fields
        self.stat_modifiers = data.get("stat_modifiers", {})
        self.control_type = data.get("control_type")
        self.flags = data.get("flags", {})

    def __repr__(self):
        return f"<StatusEffect {self.id}>"

class StatusLoader:
    def __init__(self, base_path="data"):
        self.base_path = base_path
        self.index_path = os.path.join(base_path, "status_index.json")
        self.schema_path = os.path.join(base_path, "status_schema.json")

        self.status_schema = self._load_schema()
        self.status_map = self._load_index()
        self.cache = {}

    def _load_schema(self):
        with open(self.schema_path, "r") as f:
            return json.load(f)

    def _load_index(self):
        with open(self.index_path, "r") as f:
            index_data = json.load(f)

        status_map = {}
        for entry in index_data["status_effects"]:
            status_map[entry["id"]] = os.path.join(self.base_path, entry["path"])
        return status_map

    def load(self, status_id):
        if status_id in self.cache:
            return self.cache[status_id]

        if status_id not in self.status_map:
            raise ValueError(f"Status '{status_id}' not found in index.")

        path = self.status_map[status_id]
        with open(path, "r") as f:
            data = json.load(f)

        # Validate against schema
        try:
            validate(instance=data, schema=self.status_schema)
        except ValidationError as e:
            raise ValueError(f"Status '{status_id}' failed schema validation: {e.message}")

        status_obj = StatusEffect(data["status"])
        self.cache[status_id] = status_obj
        return status_obj

    def load_all(self):
        return {sid: self.load(sid) for sid in self.status_map}
