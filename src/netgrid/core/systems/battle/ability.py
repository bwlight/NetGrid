#Version 2.0 - 3/2/26
class Ability:
    def __init__(
        self,
        id: str,
        name: str,
        type: str,
        element: str = None,
        power: int = 0,
        cost: int = 0,
        cooldown: int = 0,
        accuracy: float = 1.0,
        target: str = "single",
        effects: dict = None,
        status_effects: list = None,
        description: str = ""
    ):
        self.id = id
        self.name = name
        self.type = type  # attack | support | passive
        self.element = element
        self.power = power
        self.cost = cost
        self.cooldown = cooldown
        self.accuracy = accuracy
        self.target = target
        self.effects = effects or {}
        self.status_effects = status_effects or []
        self.description = description

        # Auto-generated tags for AI scoring
        self.tags = self._generate_tags()

    # ---------------------------------------------------------
    # Tag generation based on schema fields
    # ---------------------------------------------------------
    def _generate_tags(self):
        tags = set()

        # Type-based tags
        if self.type == "attack":
            tags.add("attack")
        elif self.type == "support":
            tags.add("support")
        elif self.type == "passive":
            tags.add("passive")

        # Power-based tags
        if self.power > 0:
            tags.add("damage")
        if self.power >= 50:
            tags.add("high_damage")
        if self.power >= 80:
            tags.add("finisher")

        # Effects-based tags
        if "stat_modifiers" in self.effects:
            mods = self.effects["stat_modifiers"]
            # Buffs vs debuffs
            for stat, value in mods.items():
                if value > 0:
                    tags.add("buff")
                elif value < 0:
                    tags.add("debuff")

        if "heal_percent" in self.effects or "heal_flat" in self.effects:
            tags.add("heal")

        if "status_inflict" in self.effects:
            tags.add("status")
            # Control tags
            status = self.effects["status_inflict"]
            if status in ("stun", "root", "sleep", "freeze"):
                tags.add("control")

        # Multi-hit
        if "multi_hit" in self.effects and self.effects["multi_hit"] > 1:
            tags.add("multi_hit")

        return list(tags)

    # ---------------------------------------------------------
    # Convenience helpers for AI logic
    # ---------------------------------------------------------
    @property
    def is_attack(self):
        return self.type == "attack"

    @property
    def is_support(self):
        return self.type == "support"

    @property
    def is_passive(self):
        return self.type == "passive"

    def __repr__(self):
        return f"<Ability {self.id}: {self.name}>"
    
    @property
    def is_multi_target(self):
        return self.target in ("multi_enemy", "multi_ally", "multi_all")
