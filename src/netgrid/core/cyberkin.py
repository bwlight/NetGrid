class EvolutionStage:
    """
    Represents a single evolution stage (baby, rookie, champion, final).
    Holds name and stats.
    """
    def __init__(self, name: str, stats: dict):
        self.name = name
        self.stats = stats  # dict with hp, attack, defense, etc.

    def __repr__(self):
        return f"<EvolutionStage {self.name}>"


class Cyberkin:
    """
    Represents an entire Cyberkin family:
    - family_id
    - name
    - sector
    - type
    - evolution stages
    - abilities (names only for now)
    - habitat
    - evolution requirements
    - quest hooks
    """
    def __init__(self, data: dict):
        # Basic identity
        self.family_id = data["family_id"]
        self.name = data["name"]
        self.sector = data["sector"]
        self.type = data["type"]

        # Evolution line (baby, rookie, champion, final)
        evo = data["evolution_line"]
        self.evolution_line = {
            stage: EvolutionStage(
                evo[stage]["name"],
                evo[stage]["stats"]
            )
            for stage in evo
        }

        # Ability names (actual Ability objects linked later)
        self.ability_names = data.get("abilities", [])
        self.abilities = []  # populated after ability loader runs

        # World/lore info
        self.habitat = data.get("habitat", "")
        self.evolution_requirements = data.get("evolution_requirements", [])
        self.quest_hooks = data.get("quest_hooks", [])

    def link_abilities(self, ability_registry):
        """
        After abilities are loaded, link actual Ability objects
        to this Cyberkin.
        """
        self.abilities = [
            ability_registry[name]
            for name in self.ability_names
            if name in ability_registry
        ]

    def get_stage(self, stage_name: str):
        """Return a specific evolution stage object."""
        return self.evolution_line.get(stage_name)

    def __repr__(self):
        return f"<Cyberkin {self.family_id}: {self.name}>"
