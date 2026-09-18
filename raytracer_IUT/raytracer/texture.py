from __future__ import annotations
import math
from typing import TYPE_CHECKING
from .vec3 import Color

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
