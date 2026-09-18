
from __future__ import annotations
from ..vec3 import Color, WHITE
from ..ray import Ray
from ..hit import Hit


class Light:
    def __init__(self, color: Color = WHITE): self.color = color

    def shade(self, ray: Ray, hit: Hit,
              scene: "Scene") -> Color: raise NotImplementedError
