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


def composer_image(fond: Image.Image, etoiles: Image.Image) -> Image.Image:
    """Assemble le fond et la couche transparente contenant les étoiles."""

    fond_rgba = fond.convert("RGBA")
    etoiles_a_la_taille_du_fond = etoiles.resize(fond_rgba.size)
    return Image.alpha_composite(fond_rgba, etoiles_a_la_taille_du_fond)


if __name__ == "__main__":
    fond = Image.open("__fondNoir.png").convert("RGBA")
    largeur, hauteur = fond.size
    etoiles = generer_etoiles(100, largeur, hauteur)
    couche_etoiles = dessiner_etoiles(etoiles, largeur, hauteur)
    image_finale = composer_image(fond, couche_etoiles)
    image_finale.show()



