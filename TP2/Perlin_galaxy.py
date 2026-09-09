#import de la librairie noise pour le bruit de Perlin
from noise import pnoise2, pnoise3
from dataclasses import dataclass
from random import randint

from PIL import Image, ImageDraw


@dataclass
class Etoile:
    """Créer une étoile basé sur la base d'un cercle
     x est la position horizontale, y est la position verticale, rayon est le rayon du cercle et couleur est un tuple RGBA."""

    x: int 
    y: int
    rayon: int
    couleur: tuple[int, int, int, int]


def generer_etoiles(nombre: int, largeur: int, hauteur: int) -> list[Etoile]:
    """Génère 100 étoiles de tailles et de couleurs variées.
    Les étoiles sont générées aléatoirement dans l'image de largeur et hauteur données.
    """

    etoiles = []
    for _ in range(nombre):
        rayon = randint(1, 30)
        etoiles.append(
            Etoile(
                x=randint(rayon, largeur - rayon - 1),
                y=randint(rayon, hauteur - rayon - 1),
                rayon=rayon,
                couleur=(
                    randint(180, 255),
                    randint(180, 255),
                    randint(180, 255),
                    randint(120, 255),
                ),
            )
        )
    return etoiles


def dessiner_etoiles(etoiles: list[Etoile], largeur: int, hauteur: int) -> Image.Image:
    """Dessine les étoiles sur une image RGBA au fond transparent."""

    
    image = Image.new("RGBA", (largeur, hauteur), (0, 0, 0, 0))
    dessin = ImageDraw.Draw(image)

    for etoile in etoiles:
        dessin.ellipse(
            (
                etoile.x - etoile.rayon,
                etoile.y - etoile.rayon,
                etoile.x + etoile.rayon,
                etoile.y + etoile.rayon,
            ),
            fill=etoile.couleur,
        )
    return image


def generer_bruit_perlin(largeur: int, hauteur: int, echelle: float = 200.0, octaves: int = 6, persistence: float = 0.55, lacunarity: float = 2.0) -> Image.Image:
    """Génère une couche de nébuleuse basée sur le bruit de Perlin 2D."""

    image_bruit = Image.new("RGBA", (largeur, hauteur))
    pixels = image_bruit.load()

    for y in range(hauteur):
        for x in range(largeur):
            #on calcule la valeur du bruit de Perlin pour chaque pixel
            valeur = pnoise2(
                x / echelle,
                y / echelle,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
            )
            # on fait varier l'intensité de la couleur en fonction de la valeur du bruit de Perlin
            intensite = (valeur + 0.6) / 1.2
            intensite = max(0.0, min(1.0, intensite))

            # Nuances bleutées / cyan / violettes pour un effet galaxie trop classe
            r = int(intensite * 70 + (intensite ** 3) * 120)
            g = int(intensite * 100 + (intensite ** 2) * 120)
            b = int(intensite * 240)
            alpha = int(intensite * 200)

            pixels[x, y] = (r, g, b, alpha)

    return image_bruit


def composer_image(fond: Image.Image, etoiles: Image.Image) -> Image.Image:
    """Assemble le fond et la couche transparente contenant les étoiles."""

    fond_rgba = fond.convert("RGBA")
    etoiles_a_la_taille_du_fond = etoiles.resize(fond_rgba.size)
    return Image.alpha_composite(fond_rgba, etoiles_a_la_taille_du_fond)


if __name__ == "__main__":
    # Ajout d'un fond noir
    fond = Image.open("__fondNoir.png").convert("RGBA")
    largeur, hauteur = fond.size

    print(f"Génération de la nébuleuse avec le bruit de Perlin ({largeur}x{hauteur})...")
    # Génération de la couche de bruit de Perlin
    couche_bruit = generer_bruit_perlin(largeur, hauteur, echelle=250.0, octaves=6)

    # Fusion du bruit sur le fond noir
    fond_avec_bruit = Image.alpha_composite(fond, couche_bruit)

    print("Génération et dessin des étoiles...")
    # Génération et dessin des étoiles
    etoiles = generer_etoiles(100, largeur, hauteur)
    couche_etoiles = dessiner_etoiles(etoiles, largeur, hauteur)

    # Composition finale
    image_finale = composer_image(fond_avec_bruit, couche_etoiles)
    image_finale.show()



