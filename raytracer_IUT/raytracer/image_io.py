
from __future__ import annotations
from typing import List
from math import pow
from .vec3 import Color, clamp01


def _gamma_to_byte(x: float, inv_g: float) -> int:
    return max(0, min(255, int(pow(clamp01(x), inv_g) * 255 + 0.5)))


def write_ppm(path: str, nx: int, ny: int, pixels: List[Color], gamma: float = 2.2, normalize: bool = False) -> None:
    if normalize:
        m = max(max(p.x, p.y, p.z) for p in pixels)
        if m > 0:
            pixels = [Color(p.x/m, p.y/m, p.z/m) for p in pixels]
    inv_g = 1.0 / gamma if gamma > 0 else 1.0
    with open(path, "wb") as f:
        f.write(f"P6\n{nx} {ny}\n255\n".encode("ascii"))
        buf = bytearray()
        for p in pixels:
            buf.extend(bytes([_gamma_to_byte(p.x, inv_g), _gamma_to_byte(
                p.y, inv_g), _gamma_to_byte(p.z, inv_g)]))
        f.write(buf)


def write_png(path: str, nx: int, ny: int, pixels: List[Color], gamma: float = 2.2, normalize: bool = False) -> None:
    try:
        from PIL import Image  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "Pillow n'est pas installé. pip install pillow") from e
    if normalize:
        m = max(max(p.x, p.y, p.z) for p in pixels)
        if m > 0:
            pixels = [Color(p.x/m, p.y/m, p.z/m) for p in pixels]
    inv_g = 1.0 / gamma if gamma > 0 else 1.0
    data = bytearray(nx * ny * 3)
    k = 0
    for j in range(ny):
        base = j * nx
        for i in range(nx):
            p = pixels[base + i]
            data[k] = _gamma_to_byte(p.x, inv_g)
            data[k+1] = _gamma_to_byte(p.y, inv_g)
            data[k+2] = _gamma_to_byte(p.z, inv_g)
            k += 3
    from PIL import Image
    Image.frombytes("RGB", (nx, ny), bytes(data)).save(path, format="PNG")
