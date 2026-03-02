class CooldownManager:
    def __init__(self):
        self.cooldowns = {}  # entity_id -> { ability_id: turns_remaining }

    def start_cooldown(self, entity, ability):
        if ability.cooldown <= 0:
            return

        eid = entity.id
        if eid not in self.cooldowns:
            self.cooldowns[eid] = {}

        self.cooldowns[eid][ability.id] = ability.cooldown

    def is_on_cooldown(self, entity, ability):
        eid = entity.id
        if eid not in self.cooldowns:
            return False

        return self.cooldowns[eid].get(ability.id, 0) > 0

    def tick(self):
        for eid in list(self.cooldowns.keys()):
            for ability_id in list(self.cooldowns[eid].keys()):
                self.cooldowns[eid][ability_id] -= 1
                if self.cooldowns[eid][ability_id] <= 0:
                    del self.cooldowns[eid][ability_id]
