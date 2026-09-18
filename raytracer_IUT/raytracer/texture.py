from __future__ import annotations
import math
from typing import TYPE_CHECKING
from .vec3 import Color
import noise

if TYPE_CHECKING:
    from .hit import Hit


class Texture:
    """Classe de base pour toutes les textures."""
    def couleur(self, hit: Hit) -> Color:
        raise NotImplementedError


class Damier(Texture):
    """Texture de damier 2D basée sur les coordonnées (u, v) du Hit."""
    def __init__(self, color1: Color = Color(1, 1, 1), color2: Color = Color(0.1, 0.3, 0.9), taille: float = 1.0):
        self.color1 = color1
        self.color2 = color2
        self.taille = taille

    def couleur(self, hit: Hit) -> Color:
        u_idx = math.floor(hit.u / self.taille)
        v_idx = math.floor(hit.v / self.taille)
        if (int(u_idx) + int(v_idx)) % 2 == 0:
            return self.color1
        return self.color2



class Bruit(Texture):
    """Texture de bruit de Perlin grace à la librairie noise."""
    def __init__(self, scale: float = 0.5, octaves: int = 4):
        self.scale = scale
        self.octaves = octaves

    def couleur(self, hit: Hit) -> Color:
        noise_value = self.perlin_noise(hit.point.x * self.scale, hit.point.y * self.scale, hit.point.z * self.scale)
        val = max(0.0, min(1.0, noise_value))
        return Color(val, val, val)

    def perlin_noise(self, x: float, y: float, z: float) -> float:
        if noise is not None:
            return (noise.pnoise3(x, y, z, octaves=self.octaves) + 1.0) * 0.5
        return (math.sin(x) + math.sin(y) + math.sin(z) + 3.0) / 6.0