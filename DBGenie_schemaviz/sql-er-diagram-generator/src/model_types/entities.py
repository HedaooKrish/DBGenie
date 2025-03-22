from dataclasses import dataclass
from typing import List

@dataclass
class Entity:
    name: str
    columns: List[str]

@dataclass
class Relationship:
    source: str
    target: str
    label: str