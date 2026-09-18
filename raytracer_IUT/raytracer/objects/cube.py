
from __future__ import annotations
from dataclasses import dataclass
from ..vec3 import Vec3, EPSILON
from ..ray import Ray
from ..hit import Hit
from .base import Object3D


def _min3(a: float, b: float, c: float) -> float:
    return a if a <= b and a <= c else (b if b <= c else c)


class Cube(Object3D):
    mn: Vec3
    mx: Vec3

    def __init__(self, mn: Vec3, mx: Vec3):
        super().__init__()
        self.mn = Vec3(min(mn.x, mx.x), min(mn.y, mx.y), min(mn.z, mx.z))
        self.mx = Vec3(max(mn.x, mx.x), max(mn.y, mx.y), max(mn.z, mx.z))

    def CoinMin(self, p: Vec3): self.mn = p
    def CoinMax(self, p: Vec3): self.mx = p

    def DepuisCentreEtTaille(self, c: Vec3, sx: float, sy: float, sz: float):
        hx, hy, hz = sx*0.5, sy*0.5, sz*0.5
        self.mn = Vec3(c.x - hx, c.y - hy, c.z - hz)
        self.mx = Vec3(c.x + hx, c.y + hy, c.z + hz)

    def intersection(self, ray: Ray) -> Hit:
        o = ray.origin
        d = ray.direction
        # méthode des Slabs
        invx = 1.0 / d.x if abs(d.x) > EPSILON else float('inf')
        invy = 1.0 / d.y if abs(d.y) > EPSILON else float('inf')
        invz = 1.0 / d.z if abs(d.z) > EPSILON else float('inf')

        tx1 = (self.mn.x - o.x) * invx
        tx2 = (self.mx.x - o.x) * invx
        tmin = min(tx1, tx2)
        tmax = max(tx1, tx2)
        side_min = 0 if tx1 < tx2 else 1  # 0:xmin,1:xmax

        ty1 = (self.mn.y - o.y) * invy
        ty2 = (self.mx.y - o.y) * invy
        tmin_y = min(ty1, ty2)
        tmax_y = max(ty1, ty2)
        side_min_y = 2 if ty1 < ty2 else 3  # 2:ymin,3:ymax

        if tmin_y > tmin:
            tmin = tmin_y
            side_min = side_min_y
        if tmax_y < tmax:
            tmax = tmax_y

        tz1 = (self.mn.z - o.z) * invz
        tz2 = (self.mx.z - o.z) * invz
        tmin_z = min(tz1, tz2)
        tmax_z = max(tz1, tz2)
        side_min_z = 4 if tz1 < tz2 else 5  # 4:zmin,5:zmax

        if tmin_z > tmin:
            tmin = tmin_z
            side_min = side_min_z
        if tmax_z < tmax:
            tmax = tmax_z

        h = Hit()
        if tmax < EPSILON or tmin > tmax:  # no hit or behind
            return h

        t = tmin if tmin > EPSILON else (tmax if tmax > EPSILON else None)
        if t is None:
            return h

        p = o + d * t

        # Determine geometric normal from side_min (the entering face if t==tmin; else exiting face for inside rays)
        if side_min == 0:
            n = Vec3(-1, 0, 0)
        elif side_min == 1:
            n = Vec3(1, 0, 0)
        elif side_min == 2:
            n = Vec3(0, -1, 0)
        elif side_min == 3:
            n = Vec3(0, 1, 0)
        elif side_min == 4:
            n = Vec3(0, 0, -1)
        else:
            n = Vec3(0, 0, 1)

        h.t = t
        h.point = p
        h.normal = n
        h.obj = self
        # Orient normal to oppose the ray (for correct shading)
        if d.dot(n) > 0.0:
            n = Vec3(-n.x, -n.y, -n.z)
            h.normal = n
            h.next_medium_ior = self.mat.ior_outside
        else:
            h.next_medium_ior = self.mat.ior_inside
        return h
