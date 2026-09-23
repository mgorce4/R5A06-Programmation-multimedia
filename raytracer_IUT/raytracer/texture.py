from __future__ import annotations
import math
from typing import TYPE_CHECKING
from random import Random
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



class Rubiks(Texture):
    """Texture de Rubik's cube mélangé : une couleur aléatoire fixe par autocollant, basée sur (u, v)."""
    def __init__(self, taille: float = 1.0, bord: float = 0.08, color_bord: Color = Color(0.02, 0.02, 0.02), seed: int = 0):
        self.taille = taille
        self.bord = bord
        self.color_bord = color_bord
        self.rng = Random(seed)
        self.cases = {}
        
        self.colors = [
            Color(0.8, 0.0, 0.0),     # rouge
            Color(1.0, 0.4, 0.0),     # orange
            Color(1.0, 1.0, 1.0),     # blanc
            Color(1.0, 0.85, 0.0),    # jaune
            Color(0.0, 0.2, 0.8),     # bleu
            Color(0.0, 0.6, 0.1),     # vert
        ]

    def _sur_bord(self, hit: Hit) -> bool:
        fu = (hit.u / self.taille) % 1.0
        fv = (hit.v / self.taille) % 1.0
        return fu < self.bord or fu > 1.0 - self.bord or fv < self.bord or fv > 1.0 - self.bord

    def _face(self, hit: Hit) -> int:
        n = hit.normal
        if abs(n.x) >= abs(n.y) and abs(n.x) >= abs(n.z):
            return 0 if n.x > 0 else 1
        if abs(n.y) >= abs(n.z):
            return 2 if n.y > 0 else 3
        return 4 if n.z > 0 else 5

    def couleur(self, hit: Hit) -> Color:
        if self._sur_bord(hit):
            return self.color_bord

        face = self._face(hit)
        u_idx = math.floor(hit.u / self.taille)
        v_idx = math.floor(hit.v / self.taille)

        if u_idx == 1 and v_idx == 1:
            return self.colors[face]

        cle = (face, u_idx, v_idx)
        if cle not in self.cases:
            self.cases[cle] = self.rng.choice(self.colors)
        return self.cases[cle]


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