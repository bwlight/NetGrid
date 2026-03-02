import random

class AbilityManager:
    def __init__(self, ability_loader):
        self.ability_loader = ability_loader

    def get(self, ability_id):
        return self.ability_loader.load(ability_id)

    def can_use(self, entity, ability):
        # Cost system is simple for now
        return True

    def get_targets(self, user, ability, allies, enemies):
        t = ability.target

        if t == "self":
            return [user]
        if t == "ally":
            return allies
        if t == "enemy":
            return enemies
        if t == "single":
            return [enemies[0]] if enemies else []
        if t == "multi":
            return enemies
        if t == "random":
            return [random.choice(enemies)] if enemies else []

        return []

    def check_accuracy(self, user, target, ability, status_engine):
        acc = ability.accuracy

        # Evasion boost from statuses
        if status_engine.has_evasion_boost(target):
            acc *= 0.8

        return random.random() <= acc

    def apply_status_if_any(self, target, ability, status_loader, status_engine):
        eff = ability.effects
        if "status_inflict" not in eff:
            return

        status_id = eff["status_inflict"]
        chance = eff.get("status_chance", 1.0)

        if random.random() <= chance:
            status_obj = status_loader.load(status_id)
            status_engine.apply(target, status_obj)
