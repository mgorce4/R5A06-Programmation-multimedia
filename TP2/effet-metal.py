from dataclasses import dataclass
from random import randint
from math import sin, pi

from PIL import Image, ImageDraw


def generer_image_sinus(
    largeur: int,
    hauteur: int,
    periode: float = 100.0
) -> Image.Image:
    """
    Génère une image dont la couleur de chaque pixel
    dépend d'un sinus de x + y (effet métal sans perturbation).
    """

    image = Image.new("RGB", (largeur, hauteur))
    pixels = image.load()

    for y in range(hauteur):
        for x in range(largeur):

            # Position sans perturbation
            position = x + y

            # On applique le sinus sur la position
            valeur = sin(2 * pi * position / periode)

            # On change l'intensité de la couleur en fonction de la valeur du sinus
            intensite = (valeur + 1) / 2

            # Couleur bleu  -> rose
            r = int(intensite * 80 + (intensite ** 2) * 175)
            g = int(intensite * 180 + (intensite ** 2) * 30)
            b = int(220 + intensite * 35)

            pixels[x, y] = (r, g, b)

    return image


if __name__ == "__main__":

    largeur = 500
    hauteur = 500

    print("Génération de l'image avec sinus...")

    image = generer_image_sinus(
        largeur,
        hauteur,
        periode=100
    )

    image.show()