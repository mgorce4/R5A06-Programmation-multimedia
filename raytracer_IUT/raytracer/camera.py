
from __future__ import annotations
from typing import List
from .vec3 import Vec3, Color, clamp01, BLACK
from .ray import Ray
from .scene import Scene
from .render import trace_ray


class Camera:
    def __init__(self):
        self.centre = Vec3(0, 0, 0)
        self.dir = Vec3(0, 0, -1).normalize()
        self.up = Vec3(0, 1, 0)
        self.width = 4.0
        self.height = 3.0
        self.dist = 5.0

    def Centre(self, p: Vec3): self.centre = p
    def Direct(self, cible: Vec3): self.dir = (cible - self.centre).normalize()
    def Haut(self, v: Vec3): self.up = v.normalize()
    def Largeur(self, w: float): self.width = w
    def Hauteur(self, h: float): self.height = h
    def Dist(self, d: float): self.dist = d

    def render(self, scene: Scene, nx: int, ny: int, max_depth: int = 5) -> List[Color]:
        w = self.dir
        u = w.cross(self.up).normalize()    # RIGHT
        v = u.cross(w).normalize()          # TRUE UP
        screen_center = self.centre + w * self.dist
        pixels: List[Color] = [BLACK for _ in range(nx * ny)]
        for j in range(ny):
            for i in range(nx):
                x = ((i + 0.5) / nx - 0.5) * self.width
                y = (0.5 - (j + 0.5) / ny) * self.height
                p = screen_center + u * x + v * y
                r = Ray(self.centre, (p - self.centre).normalize(), 1.0)
                c = trace_ray(scene, r, max_depth)
                pixels[j*nx + i] = Color(clamp01(c.x),
                                         clamp01(c.y), clamp01(c.z))
        return pixels
