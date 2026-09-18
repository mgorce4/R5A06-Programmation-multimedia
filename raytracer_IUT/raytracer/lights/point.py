
from __future__ import annotations
from math import pow
from ..vec3 import Vec3, Color, BLACK, EPSILON
from ..ray import Ray
from ..hit import Hit
from ..scene import Scene
from .base import Light


class PointLight(Light):
    def __init__(self, position: Vec3, color: Color):
        super().__init__(color)
        self.position = position

    def shade(self, ray: Ray, hit: Hit, scene: "Scene") -> Color:
        p = hit.point
        n = hit.normal.normalize()
        to_light = (self.position - p)
        dist_l = to_light.norm()
        l = (to_light / dist_l)
        shadow = Ray(p + n * EPSILON * 10.0, l, 1.0)
        shadow_hit = scene.closest_hit(shadow)
        if shadow_hit.valid() and shadow_hit.t < dist_l - EPSILON:
            return BLACK
        ndotl = max(0.0, n.dot(l))
        diff = hit.obj.Diffuse(hit) * ndotl
        v = (-ray.direction).normalize()
        r = (-l).reflect(n).normalize()
        spec_angle = max(0.0, r.dot(v))
        spec = hit.obj.Speculaire(hit) * pow(spec_angle, 32.0)
        return (diff + spec) * self.color.x
