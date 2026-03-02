class StatusEngine:
    def __init__(self):
        pass

    def apply(self, entity, status_effect):
        # Prevent duplicates unless stacking is allowed later
        if status_effect.id in entity.status_effects:
            return

        # Clone the status so each entity has its own instance
        status_instance = {
            "effect": status_effect,
            "remaining": status_effect.duration,
            "applied_modifiers": {}
        }

        # Apply stat modifiers immediately
        for stat, value in status_effect.stat_modifiers.items():
            entity.modify_stat(stat, value)
            status_instance["applied_modifiers"][stat] = value

        entity.status_effects[status_effect.id] = status_instance

    def update(self, entity):
        expired = []

        for status_id, instance in entity.status_effects.items():
            effect = instance["effect"]

            # DOT tick
            if effect.tick_damage > 0:
                entity.take_damage(effect.tick_damage)

            # Decrement duration
            instance["remaining"] -= 1

            # Mark for expiration
            if instance["remaining"] <= 0:
                expired.append(status_id)

        # Expire statuses after iteration
        for status_id in expired:
            self.expire(entity, status_id)

    def expire(self, entity, status_id):
        instance = entity.status_effects.pop(status_id)
        effect = instance["effect"]

        # Revert stat modifiers
        for stat, value in instance["applied_modifiers"].items():
            entity.modify_stat(stat, -value)

    def is_action_locked(self, entity):
        for instance in entity.status_effects.values():
            if instance["effect"].control_type == "lock":
                return True
        return False

    def has_evasion_boost(self, entity):
        for instance in entity.status_effects.values():
            if instance["effect"].flags.get("evasion_boost"):
                return True
        return False

    def has_damage_reduction(self, entity):
        for instance in entity.status_effects.values():
            if instance["effect"].flags.get("reduces_damage"):
                return True
        return False

    def blocks_corruption(self, entity):
        for instance in entity.status_effects.values():
            if instance["effect"].flags.get("blocks_corruption"):
                return True
        return False
