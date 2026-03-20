import json
import os
from jsonschema import Draft7Validator

class AIBehaviorLoader:
    def __init__(self, schema_path):
        self.schema_path = schema_path
        self.schema = self._load_schema(schema_path)
        self.validator = Draft7Validator(self.schema)

    def _load_schema(self, path):
        with open(path, "r") as f:
            return json.load(f)

    def _log_flaw(self, cyberkin, message):
        print(f"[AIBehaviorLoader][Flaw] Cyberkin '{cyberkin.id}': {message}")
        cyberkin.ai_warnings.append(message)

    def apply(self, cyberkin_data, cyberkin):
        # Ensure warnings list exists
        cyberkin.ai_warnings = []

        # Detect missing ai_behavior block
        if "ai_behavior" not in cyberkin_data:
            self._log_flaw(cyberkin, "Missing ai_behavior block. Defaults applied.")
            ai_data = self._default_behavior()
        else:
            ai_data = cyberkin_data["ai_behavior"]

        # Validate and normalize
        ai_data = self.validate(ai_data, cyberkin)
        ai_data = self.normalize(ai_data, cyberkin)

        # Prepare phases
        ai_data["ai_phases"] = self.prepare_phases(ai_data.get("ai_phases", []), cyberkin)

        # Attach to Cyberkin object
        self._attach_behavior(cyberkin, ai_data)

    def validate(self, data, cyberkin):
        errors = sorted(self.validator.iter_errors(data), key=lambda e: e.path)

        for error in errors:
            path = ".".join(str(p) for p in error.path)
            message = f"{path}: {error.message}" if path else error.message
            self._log_flaw(cyberkin, message)

        # Return data even if flawed; normalization will fix it
        return data

    def normalize(self, data, cyberkin):
        normalized = {}

        # Role
        role = data.get("ai_role", "balanced")
        if role not in ["balanced", "aggressive", "defensive", "control", "purifier"]:
            self._log_flaw(cyberkin, f"Invalid ai_role '{role}', reset to 'balanced'.")
            role = "balanced"
        normalized["ai_role"] = role

        # Personality
        personality = data.get("ai_personality", "neutral")
        if personality not in ["neutral", "brave", "cautious", "chaotic"]:
            self._log_flaw(cyberkin, f"Invalid ai_personality '{personality}', reset to 'neutral'.")
            personality = "neutral"
        normalized["ai_personality"] = personality

        # Role tags
        valid_tags = ["tank", "support", "control", "glass_cannon"]
        tags = data.get("role_tags", [])
        cleaned_tags = []
        for t in tags:
            if t not in valid_tags:
                self._log_flaw(cyberkin, f"Unknown role_tag '{t}', ignored.")
            else:
                cleaned_tags.append(t)
        normalized["role_tags"] = cleaned_tags

        # Behavior modifiers
        normalized["ai_behavior_modifiers"] = self._normalize_modifiers(
            data.get("ai_behavior_modifiers", {}), cyberkin
        )

        # Phases (raw, will be prepared later)
        normalized["ai_phases"] = data.get("ai_phases", [])

        return normalized

    def _normalize_modifiers(self, mods, cyberkin):
        valid_mods = {
            "damage_mult",
            "dot_focus_mult",
            "control_focus_mult",
            "heal_priority_mult",
            "target_memory_mult"
        }

        cleaned = {}
        for key, value in mods.items():
            if key not in valid_mods:
                self._log_flaw(cyberkin, f"Unknown behavior modifier '{key}', ignored.")
                continue

            if not isinstance(value, (int, float)) or not (0.0 <= value <= 5.0):
                self._log_flaw(cyberkin, f"Modifier '{key}' must be 0.0–5.0, reset to 1.0.")
                cleaned[key] = 1.0
            else:
                cleaned[key] = value

        return cleaned

    def prepare_phases(self, phases, cyberkin):
        prepared = []

        for i, phase in enumerate(phases):
            name = phase.get("name", f"Phase {i+1}")
            trigger = phase.get("trigger", {})

            # Validate triggers
            if "hp_below" in trigger:
                val = trigger["hp_below"]
                if not isinstance(val, (int, float)) or not (0.0 <= val <= 1.0):
                    self._log_flaw(cyberkin, f"Phase '{name}' hp_below invalid, reset to 0.5.")
                    trigger["hp_below"] = 0.5

            # Normalize modifiers
            mods = self._normalize_modifiers(phase.get("behavior_modifiers", {}), cyberkin)

            prepared.append({
                "name": name,
                "trigger": trigger,
                "role": phase.get("role"),
                "personality": phase.get("personality"),
                "behavior_modifiers": mods
            })

        return prepared

    def _attach_behavior(self, cyberkin, data):
        # Namespace
        cyberkin.ai = {
            "role": data["ai_role"],
            "personality": data["ai_personality"],
            "role_tags": data["role_tags"],
            "modifiers": data["ai_behavior_modifiers"],
            "phases": data["ai_phases"]
        }

        # Direct attributes
        cyberkin.ai_role = data["ai_role"]
        cyberkin.ai_personality = data["ai_personality"]
        cyberkin.role_tags = data["role_tags"]
        cyberkin.ai_modifiers = data["ai_behavior_modifiers"]
        cyberkin.ai_phases = data["ai_phases"]

        # Active phase tracker
        cyberkin.active_ai_phase = None

    def _default_behavior(self):
        return {
            "ai_role": "balanced",
            "ai_personality": "neutral",
            "role_tags": [],
            "ai_behavior_modifiers": {},
            "ai_phases": []
        }
