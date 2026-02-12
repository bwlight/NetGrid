class Ability:
    def __init__(self, data: dict):
        self.id = data["id"]
        self.name = data["name"]
        self.type = data["type"]
        self.category = data["category"]
        self.energy_cost = data["energy_cost"]

        self.cooldown = data.get("cooldown", 0)
        self.power = data.get("power")
        self.accuracy = data.get("accuracy")
        self.scaling = data.get("scaling")
        self.target = data.get("target", "enemy")

        self.multi_hit = data.get("multi_hit")
        self.healing = data.get("healing")
        self.shield = data.get("shield")
        self.status_inflict = data.get("status_inflict")

        self.buffs = data.get("buffs", [])
        self.debuffs = data.get("debuffs", [])

        self.damage_over_time = data.get("damage_over_time")
        self.conditional_effects = data.get("conditional_effects", [])

        self.on_hit = data.get("on_hit", [])
        self.on_miss = data.get("on_miss", [])

    def __repr__(self):
        return f"<Ability {self.id}: {self.name}>"
