import json
import os

class AbilityManager:
    def __init__(self):
        # Correct project root (FIVE levels up from this file)
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../../../../")
        )
        self.project_root = project_root

        # Build correct paths
        self.base_path = os.path.join(project_root, "data", "abilities")
        self.master_index_path = os.path.join(self.base_path, "ability_master_index.json")

        self.abilities = {}
        self.family_abilities = {}
        self.universal_abilities = {}
        self.cross_family_abilities = {}
        self.status_abilities = {}
        self.boss_only = {}

        self.load_master_index()
        self.load_all_abilities()

    def load_master_index(self):
        with open(self.master_index_path, "r") as f:
            self.master_index = json.load(f)

    def load_all_abilities(self):
        self.load_family_abilities()
        self.load_universal_abilities()
        self.load_cross_family_abilities()
        self.load_status_abilities()
        self.load_boss_only()

    def load_family_abilities(self):
        families = self.master_index.get("families", {})
        for family, path in families.items():
            full_path = os.path.normpath(os.path.join(self.project_root, path))
            data = self._load_json(full_path)
            self.family_abilities[family] = data
            self.abilities.update(data)

    def load_universal_abilities(self):
        entry = self.master_index.get("universal", {})
        path = entry.get("path")
        if path:
            full_path = os.path.normpath(os.path.join(self.project_root, path))
            data = self._load_json(full_path)
            self.universal_abilities = data
            self.abilities.update(data)

    def load_cross_family_abilities(self):
        entry = self.master_index.get("cross_family", {})
        path = entry.get("path")
        if path:
            full_path = os.path.normpath(os.path.join(self.project_root, path))
            data = self._load_json(full_path)
            self.cross_family_abilities = data
            self.abilities.update(data)

    def load_status_abilities(self):
        entry = self.master_index.get("status", {})
        path = entry.get("path")
        if path:
            full_path = os.path.normpath(os.path.join(self.project_root, path))
            data = self._load_json(full_path)
            self.status_abilities = data
            self.abilities.update(data)

    def load_boss_only(self):
        boss_entries = self.master_index.get("boss_only", {})
        for key, entry in boss_entries.items():
            path = entry.get("path")
            if path:
                full_path = os.path.normpath(os.path.join(self.project_root, path))
                data = self._load_json(full_path)
                if "special" in data:
                    self.boss_only[key] = data["special"]
                    self.abilities[key] = data["special"]

    def _load_json(self, path):
        with open(path, "r") as f:
            return json.load(f)
