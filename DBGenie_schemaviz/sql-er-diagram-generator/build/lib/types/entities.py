from dataclasses import dataclass

@dataclass
class Entity:
    name: str
    columns: list

@dataclass
class Relationship:
    source: str
    target: str
    label: str