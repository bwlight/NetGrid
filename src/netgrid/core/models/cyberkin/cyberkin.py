class Cyberkin:
    def __init__(
        self,
        id: str,
        name: str,
        family: str,
        stage: str,
        stats: dict,
        abilities: list,
        evolution: dict,
        personality: dict,
        role: str = None,
        description: str = ""
    ):
        self.id = id
        self.name = name
        self.family = family
        self.stage = stage
        self.stats = stats
        self.abilities = abilities
        self.evolution = evolution
        self.personality = personality
        self.role = role
        self.description = description

    def __repr__(self):
        return f"<Cyberkin {self.id}: {self.name} ({self.stage})>"
