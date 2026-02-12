class StatusCondition:
    def __init__(self, data: dict):
        self.id = data["id"]
        self.name = data["name"]
        self.category = data["category"]
        self.duration = data["duration"]
        self.stacking = data.get("stacking", "none")

        self.stat_modifiers = data.get("stat_modifiers", [])
        self.damage_over_time = data.get("damage_over_time")
        self.healing_over_time = data.get("healing_over_time")

        self.control_effect = data.get("control_effect")
        self.trigger = data.get("trigger", "on_turn_start")

        self.cleanse_rules = data.get("cleanse_rules", {
            "can_be_cleansed": True,
            "requires_special_item": False
        })

        self.corruption_level = data.get("corruption_level", 0)

    def __repr__(self):
        return f"<Status {self.id}: {self.name}>"
