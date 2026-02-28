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
        self.type = type
        self.element = element
        self.power = power
        self.cost = cost
        self.cooldown = cooldown
        self.accuracy = accuracy
        self.target = target
        self.effects = effects or {}
        self.status_effects = status_effects or []
        self.description = description

    def __repr__(self):
        return f"<Ability {self.id}: {self.name}>"
