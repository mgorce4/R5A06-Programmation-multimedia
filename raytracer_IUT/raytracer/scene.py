
from __future__ import annotations
from typing import List
from .hit import Hit
from .ray import Ray


class Scene:
    def __init__(self):
        self.objects: List["Object3D"] = []
        self.lights: List["Light"] = []

    def add_object(self, o: "Object3D"): self.objects.append(o)

    def add_light(self, l: "Light"): self.lights.append(l)

    def closest_hit(self, ray: Ray) -> Hit:
        best = Hit()
        for o in self.objects:
            h = o.intersection(ray)
            if h.valid() and h.t < best.t:
                best = h
        return best
