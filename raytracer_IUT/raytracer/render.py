
from __future__ import annotations
from .vec3 import Color, BLACK
from .ray import Ray
from .scene import Scene
__render_version__ = "energy_blend_v6"


def trace_ray(scene: Scene, ray: Ray, depth: int) -> Color:
    if depth <= 0:
        return BLACK
    hit = scene.closest_hit(ray)
    if not hit.valid():
        return BLACK
    local = BLACK
    for light in scene.lights:
        local = local + light.shade(ray, hit, scene)
    kr = max(0.0, min(1.0, hit.obj.Kr()))
    kt = max(0.0, min(1.0, hit.obj.Kt()))
    base = max(0.0, 1.0 - kr - kt)
    refl_col = BLACK
    if kr > 0.0:
        refl_dir = ray.direction.reflect(hit.normal).normalize()
        refl_ray = Ray(hit.point + hit.normal * 1e-2, refl_dir, ray.medium_ior)
        refl_col = trace_ray(scene, refl_ray, depth - 1)
    refr_col = BLACK
    if kt > 0.0:
        refr_dir = ray.direction.refract(
            hit.normal, ray.medium_ior, hit.next_medium_ior)
        if not refr_dir.near_zero():
            refr_ray = Ray(hit.point - hit.normal * 1e-2,
                           refr_dir.normalize(), hit.next_medium_ior)
            refr_col = trace_ray(scene, refr_ray, depth - 1)
    return local * base + refl_col * kr + refr_col * kt
