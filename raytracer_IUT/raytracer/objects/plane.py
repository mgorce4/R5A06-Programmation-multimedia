
from __future__ import annotations
from ..vec3 import Vec3, EPSILON
from ..ray import Ray
from ..hit import Hit
from .base import Object3D


class Plane(Object3D):
    def __init__(self, normal: Vec3, d: float):
        super().__init__()
        self.n = normal.normalize()
        self.d = d
        self._init_axes()

    def _init_axes(self):
        if abs(self.n.y) > 0.9:
            self.u_axis = Vec3(1, 0, 0)
            self.v_axis = Vec3(0, 0, 1)
        else:
            self.u_axis = Vec3(0, 1, 0).cross(self.n).normalize()
            self.v_axis = self.n.cross(self.u_axis).normalize()

    def depuisVetP(self, v: Vec3, p: Vec3):
        self.n = v.normalize()
        self.d = -self.n.dot(p)
        self._init_axes()

    def Normale(self) -> Vec3: return self.n

    def Distance(self, p: Vec3) -> float: return self.n.dot(p) + self.d

    def intersection(self, ray: Ray) -> Hit:
        denom = self.n.dot(ray.direction)
        h = Hit()
        if abs(denom) < EPSILON:
            return h
        t = -(self.n.dot(ray.origin) + self.d) / denom
        if t <= EPSILON:
            return h
        p = ray.origin + ray.direction * t
        n = self.n if denom < 0 else -self.n
        h.t = t
        h.point = p
        h.normal = n
        h.obj = self
        h.next_medium_ior = self.mat.ior_inside if denom < 0 else self.mat.ior_outside
        h.u = p.dot(self.u_axis)
        h.v = p.dot(self.v_axis)
        return h
