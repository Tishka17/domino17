from dataclasses import dataclass
from typing import List


@dataclass
class Environment:
    id: str
    name: str
    visibility: str


@dataclass
class EnvironmentList:
    object_type: str
    data: List[Environment]
