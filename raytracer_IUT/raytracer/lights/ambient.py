
from __future__ import annotations
from ..vec3 import Color
from ..ray import Ray
from ..hit import Hit
from ..scene import Scene
from .base import Light


class AmbientLight(Light):
    def shade(self, ray: Ray, hit: Hit, scene: "Scene") -> Color:
        return hit.obj.Ambiante(hit) * self.color.x
