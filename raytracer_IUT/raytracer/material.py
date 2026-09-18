
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
from .vec3 import Color

if TYPE_CHECKING:
    from .texture import Texture
    from .hit import Hit


@dataclass(slots=True)
class Material:
    color: Color = field(default_factory=lambda: Color(1, 1, 1))
    ka: float = 0.3
    kd: float = 0.8
    ks: float = 0.6
    kr: float = 0.0
    kt: float = 0.0
    ior_inside: float = 1.0
    ior_outside: float = 1.0
    texture: Optional[Texture] = None

    def couleurTex(self, hit: Optional[Hit] = None) -> Color:
        if self.texture is not None and hit is not None:
            return self.texture.couleur(hit)
        return self.color

