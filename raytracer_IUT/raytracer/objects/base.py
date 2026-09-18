
from __future__ import annotations
from ..material import Material
from ..vec3 import Color
from ..ray import Ray
from ..hit import Hit


class Object3D:
    def __init__(self): self.mat = Material()
    def Texture(self, tex): self.mat.texture = tex
    def Couleur(self, c: Color): self.mat.color = c
    def Ka(self, v: float): self.mat.ka = v
    def Kd(self, v: float): self.mat.kd = v
    def Ks(self, v: float): self.mat.ks = v
    def Reflexion(self, v: float): self.mat.kr = v
    def Transparence(self, v: float): self.mat.kt = v
    def Milieu_int(self, n: float): self.mat.ior_inside = n
    def Milieu_ext(self, n: float): self.mat.ior_outside = n
    def Ambiante(self, hit: Hit | None = None): return self.mat.couleurTex(hit) * self.mat.ka
    def Diffuse(self, hit: Hit | None = None): return self.mat.couleurTex(hit) * self.mat.kd
    def Speculaire(self, hit: Hit | None = None): return self.mat.color * self.mat.ks
    def couleurTex(self, hit: Hit | None = None): return self.mat.couleurTex(hit)
    def Kr(self) -> float: return self.mat.kr
    def Kt(self) -> float: return self.mat.kt
    def intersection(self, ray: Ray) -> Hit: raise NotImplementedError
