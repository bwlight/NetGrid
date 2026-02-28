import json
import os


class AIConfigLoader:
    """
    Loads AI configuration data from ai_config.json.
    Provides access to role behaviors, personality modifiers,
    threat values, and ability scoring weights.
    """

    def __init__(self, path="data/ai/ai_config.json"):
        self.path = path

        if not os.path.isfile(self.path):
            raise FileNotFoundError(f"AI config file not found: {self.path}")

        with open(self.path, "r") as fp:
            raw = json.load(fp)

        # Core sections
        self.roles = raw.get("roles", {})
        self.personalities = raw.get("personalities", {})
        self.threat_values = raw.get("threat_values", {})
        self.ability_weights = raw.get("ability_weights", {})

        # Validation
        self._validate()

    # --------------------------------------------------------------
    # Validation ensures the config is complete and usable
    # --------------------------------------------------------------
    def _validate(self):
        if not self.roles:
            raise ValueError("AI config missing 'roles' section.")

        if not self.personalities:
            raise ValueError("AI config missing 'personalities' section.")

        if not self.threat_values:
            raise ValueError("AI config missing 'threat_values' section.")

        if not self.ability_weights:
            raise ValueError("AI config missing 'ability_weights' section.")

    # --------------------------------------------------------------
    # Public API
    # --------------------------------------------------------------
    def get_role_config(self, role: str) -> dict:
        """Return the configuration for a given AI role."""
        return self.roles.get(role, self.roles.get("aggressive"))

    def get_personality_config(self, personality: str) -> dict:
        """Return the configuration for a given AI personality."""
        return self.personalities.get(personality, self.personalities.get("neutral"))

    def get_threat_value(self, action_type: str) -> float:
        """Return the threat multiplier for a given action type."""
        return self.threat_values.get(action_type, 1.0)

    def get_ability_weight(self, weight_type: str) -> float:
        """Return the scoring weight for a given ability category."""
        return self.ability_weights.get(weight_type, 1.0)
