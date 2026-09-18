
from raytracer import (
    Vec3, Color, AmbientLight, PointLight,
    Plane, Sphere, Cube, Camera, Scene, write_png,
    Damier
)
from time import time

if __name__ == "__main__":
    NX, NY = 400, 300
    scene = Scene()
    scene.add_light(AmbientLight(Color(1, 1, 1)))
    scene.add_light(PointLight(Vec3(10, 15, 10), Color(1, 1, 1)))
    floor = Plane(Vec3(0, 1, 0), 0.0)
    floor.Couleur(Color(0.65, 0.75, 0.65))
    floor.Texture(Damier(Color(1.0, 1.0, 1.0), Color(0.1, 0.3, 0.9), taille=2.0))
    floor.Kd(0.8)
    floor.Ka(0.3)
    floor.Ks(0.2)
    floor.Reflexion(0.5)
    scene.add_object(floor)
    back = Plane(Vec3(0, 0, 1), 10.0)
    back.Couleur(Color(0.9, 0.7, 0.7))
    back.Kd(0.7)
    back.Ka(0.3)
    back.Ks(0.1)
    scene.add_object(back)
    s1 = Sphere(Vec3(2.5, 4.0, 0.0), 2.0)
    s1.Couleur(Color(0.75, 0.75, 1.0))
    s1.Ks(0.6)
    s1.Kd(0.8)
    s1.Ka(0.3)
    scene.add_object(s1)
    s2 = Sphere(Vec3(-3.5, 3.0, 0.5), 3.0)
    s2.Couleur(Color(1.0, 0.5, 0.5))
    s2.Reflexion(0.75)
    scene.add_object(s2)

    c3 = Cube(Vec3(3.5-1.0, 4.0-1.0, 5.0-1.0), Vec3(3.5+1.0, 4.0+1.0, 5.0+1.0))
    c3.Couleur(Color(1.0, 1.0, 1.0))
    c3.Transparence(0.85)
    c3.Reflexion(0.15)
    c3.Milieu_int(1.5)
    scene.add_object(c3)

    cam = Camera()
    cam.Centre(Vec3(0.0, 5.0, 12.0))
    cam.Haut(Vec3(0.0, 1.0, 0.0))
    cam.Dist(5.0)
    FOV_W = 8
    cam.Largeur(FOV_W)
    cam.Hauteur(FOV_W * NY / NX)  # aspect garanti
    cam.Direct(Vec3(0.0, 3.5, 0.0))
    tic = time()
    pixels = cam.render(scene, NX, NY, max_depth=5)
    tac = time()
    print(round((tac-tic)/2, 3))
    write_png("image.png", NX, NY, pixels, gamma=1.0, normalize=False)
    print("image.png OK")
