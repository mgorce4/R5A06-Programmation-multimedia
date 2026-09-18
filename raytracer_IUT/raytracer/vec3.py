
from __future__ import annotations
from dataclasses import dataclass
from math import sqrt

EPSILON = 1e-3


@dataclass(slots=True)
class Vec3:
    x: float
    y: float
    z: float

    def __add__(self, o: "Vec3") -> "Vec3": return Vec3(self.x +
                                                        o.x, self.y+o.y, self.z+o.z)
    def __sub__(self, o: "Vec3") -> "Vec3": return Vec3(self.x -
                                                        o.x, self.y-o.y, self.z-o.z)

    def __neg__(self) -> "Vec3": return Vec3(-self.x, -self.y, -self.z)

    def __mul__(self, k: float) -> "Vec3": return Vec3(self.x *
                                                       k, self.y*k, self.z*k)
    __rmul__ = __mul__

    def __truediv__(
        self, k: float) -> "Vec3": return Vec3(self.x/k, self.y/k, self.z/k)

    def dot(self, o: "Vec3") -> float: return self.x * \
        o.x + self.y*o.y + self.z*o.z

    def cross(self, o: "Vec3") -> "Vec3":
        return Vec3(self.y*o.z - self.z*o.y, self.z*o.x - self.x*o.z, self.x*o.y - self.y*o.x)

    def norm(self) -> float: return sqrt(self.dot(self))

    def normalize(self) -> "Vec3":
        n = self.norm()
        return self if n == 0 else self / n

    def near_zero(self) -> bool: return abs(self.x) < EPSILON and abs(
        self.y) < EPSILON and abs(self.z) < EPSILON

    def reflect(self, n: "Vec3") -> "Vec3": return self - \
        n * (2.0 * self.dot(n))

    def refract(self, n: "Vec3", n1: float, n2: float) -> "Vec3":
        v = self
        eta = n1/n2
        cos_i = -max(-1.0, min(1.0, v.dot(n)))
        sin2_t = eta*eta*(1.0 - cos_i*cos_i)
        if sin2_t > 1.0:
            return Vec3(0.0, 0.0, 0.0)
        from math import sqrt
        cos_t = sqrt(1.0 - sin2_t)
        return v*eta + n*(eta*cos_i - cos_t)


def clamp01(x: float) -> float: return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)


Color = Vec3
def mix(a: Color, b: Color, k: float) -> Color: return a*(1.0-k) + b*k


BLACK = Color(0.0, 0.0, 0.0)
WHITE = Color(1.0, 1.0, 1.0)
