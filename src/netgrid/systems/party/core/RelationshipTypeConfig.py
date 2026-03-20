from dataclasses import dataclass


@dataclass
class RelationshipTypeConfig:
    name: str
    min_value: int
    max_value: int
