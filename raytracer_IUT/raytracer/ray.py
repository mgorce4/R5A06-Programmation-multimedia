
from __future__ import annotations
from dataclasses import dataclass
from .vec3 import Vec3


@dataclass(slots=True)
class Ray:
    origin: Vec3
    direction: Vec3
    medium_ior: float = 1.0
    def __post_init__(self): self.direction = self.direction.normalize()
