"""
Fusion de Perlin_galaxy.py et animated_stars.py :
- Une nébuleuse de fond qui bouge à chaque frame (bruit de Perlin 3D échantillonné
  le long d'un cercle fermé dans l'espace du bruit -> boucle parfaite sur nb_frames images).
- Des étoiles qui défilent verticalement et bouclent parfaitement sur nb_frames images.
- Assemblage final en vidéo avec FFmpeg.
"""

import os
import subprocess
from dataclasses import dataclass
from math import cos, pi, sin
from random import randint

from noise import pnoise3
from PIL import Image, ImageDraw


@dataclass
class Etoile:
    """Créer une étoile basée sur un cercle.
    x est la position horizontale, y_init la position verticale initiale,
    rayon le rayon du cercle, couleur un tuple RGBA et vitesse la vitesse
    de défilement vertical (pixels/frame)."""

    x: float
    y_init: float
    rayon: int
    couleur: tuple[int, int, int, int]
    vitesse: float


# ---------------------------------------------------------------------------
# Nébuleuse (bruit de Perlin) - animée, avec bouclage parfait
# ---------------------------------------------------------------------------
#
# Astuce pour faire "bouger" un bruit de Perlin tout en bouclant parfaitement :
# le bruit lui-même n'est pas périodique, donc on ne peut pas juste le faire
# défiler en ligne droite (ça ne boucle jamais proprement). La solution est de
# faire parcourir aux coordonnées d'échantillonnage un CERCLE FERMÉ dans
# l'espace du bruit : comme cos()/sin() sont périodiques, la position au
# frame 0 et au frame nb_frames est rigoureusement identique (position ET
# vitesse), donc l'animation boucle sans aucune coupure visible.
#
# On combine deux mouvements circulaires :
#   - une translation circulaire de (x, y) -> la nébuleuse "dérive" doucement
#   - une oscillation de la 3e dimension du bruit (pnoise3) -> la texture se
#     déforme/évolue en plus de dériver

def generer_bruit_perlin(
    largeur: int,
    hauteur: int,
    frame_idx: int,
    nb_frames: int,
    echelle: float = 250.0,
    octaves: int = 6,
    persistence: float = 0.55,
    lacunarity: float = 2.0,
    rayon_derive: float = 1.2,
    rayon_evolution: float = 0.8,
    facteur_reduction: int = 4,
) -> Image.Image:
    """Génère une couche de nébuleuse pour le frame `frame_idx` (sur `nb_frames` au total).

    `facteur_reduction` calcule le bruit sur une grille plus petite (divisée par
    ce facteur) puis la redimensionne en douceur : comme la nébuleuse est une
    texture basse fréquence, c'est invisible à l'oeil et ça accélère énormément
    le calcul, ce qui compte vu qu'on doit refaire le bruit à chaque frame.
    Mettre facteur_reduction=1 pour calculer à pleine résolution.
    """

    angle = 2 * pi * frame_idx / nb_frames
    decalage_x = rayon_derive * cos(angle)
    decalage_y = rayon_derive * sin(angle)
    decalage_z = rayon_evolution * sin(angle)

    largeur_calc = max(1, largeur // facteur_reduction)
    hauteur_calc = max(1, hauteur // facteur_reduction)

    image_bruit = Image.new("RGBA", (largeur_calc, hauteur_calc))
    pixels = image_bruit.load()

    for y in range(hauteur_calc):
        for x in range(largeur_calc):
            # On multiplie par facteur_reduction pour garder la même échelle
            # visuelle que si on calculait à pleine résolution.
            valeur = pnoise3(
                (x * facteur_reduction) / echelle + decalage_x,
                (y * facteur_reduction) / echelle + decalage_y,
                decalage_z,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
            )
            intensite = (valeur + 0.6) / 1.2
            intensite = max(0.0, min(1.0, intensite))

            # Nuances bleutées / cyan / violettes pour un effet galaxie trop classe
            r = int(intensite * 70 + (intensite ** 3) * 120)
            g = int(intensite * 100 + (intensite ** 2) * 120)
            b = int(intensite * 240)
            alpha = int(intensite * 200)

            pixels[x, y] = (r, g, b, alpha)

    if facteur_reduction > 1:
        image_bruit = image_bruit.resize((largeur, hauteur), resample=Image.BICUBIC)

    return image_bruit


# ---------------------------------------------------------------------------
# Étoiles animées - repris d'animated_stars.py
# ---------------------------------------------------------------------------

def generer_etoiles(nombre: int, largeur: int, hauteur: int, nb_frames: int = 400) -> list[Etoile]:
    """Génère des étoiles avec une vitesse calculée pour boucler parfaitement sur nb_frames images."""
    etoiles = []
    for _ in range(nombre):
        rayon = randint(1, 30)

        # k est un nombre entier aléatoire de traversées d'écran complètes sur la durée de l'animation
        k = randint(1, 5)
        vitesse = (k * hauteur) / nb_frames

        etoiles.append(
            Etoile(
                x=randint(rayon, largeur - rayon - 1),
                y_init=randint(0, hauteur - 1),
                rayon=rayon,
                couleur=(
                    randint(180, 255),
                    randint(180, 255),
                    randint(180, 255),
                    randint(120, 255),
                ),
                vitesse=vitesse,
            )
        )
    return etoiles


def dessiner_etoiles_frame(etoiles: list[Etoile], frame_idx: int, largeur: int, hauteur: int) -> Image.Image:
    """Dessine une image (frame) de la couche d'étoiles pour l'index de frame donné.
    Gère le défilement vertical (haut en bas) et le wrapping pour éviter tout saut visible
    aux bordures supérieures et inférieures."""
    image = Image.new("RGBA", (largeur, hauteur), (0, 0, 0, 0))
    dessin = ImageDraw.Draw(image)

    for etoile in etoiles:
        y_actuel = (etoile.y_init + frame_idx * etoile.vitesse) % hauteur
        r = etoile.rayon

        for offset_y in (0, -hauteur, hauteur):
            y_draw = y_actuel + offset_y
            if -r <= y_draw <= hauteur + r:
                dessin.ellipse(
                    (
                        etoile.x - r,
                        y_draw - r,
                        etoile.x + r,
                        y_draw + r,
                    ),
                    fill=etoile.couleur,
                )

    return image


# ---------------------------------------------------------------------------
# Composition et animation
# ---------------------------------------------------------------------------

def composer_image(fond_rgba: Image.Image, etoiles: Image.Image) -> Image.Image:
    """Assemble le fond (nébuleuse déjà fusionnée sur le fond noir) et la couche d'étoiles."""
    return Image.alpha_composite(fond_rgba, etoiles)


def generer_animation(
    nb_frames: int = 400,
    nb_etoiles: int = 300,
    dossier_sortie: str = "frames",
    fichier_fond: str = "__fondNoir.png",
    echelle_bruit: float = 250.0,
    octaves_bruit: int = 6,
    rayon_derive_bruit: float = 1.2,
    rayon_evolution_bruit: float = 0.8,
    facteur_reduction_bruit: int = 4,
):
    """Génère la suite de PNGs constituant l'animation (nébuleuse qui bouge en boucle
    parfaite + étoiles qui défilent) et les place dans le dossier de sortie."""
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    fond = Image.open(fichier_fond).convert("RGBA")
    largeur, hauteur = fond.size

    print(f"Génération de {nb_etoiles} étoiles pour une image de {largeur}x{hauteur}...")
    etoiles = generer_etoiles(nb_etoiles, largeur, hauteur, nb_frames=nb_frames)

    print(f"Génération des {nb_frames} images (nébuleuse animée + étoiles) dans '{dossier_sortie}'...")
    for frame_idx in range(nb_frames):
        couche_bruit = generer_bruit_perlin(
            largeur,
            hauteur,
            frame_idx,
            nb_frames,
            echelle=echelle_bruit,
            octaves=octaves_bruit,
            rayon_derive=rayon_derive_bruit,
            rayon_evolution=rayon_evolution_bruit,
            facteur_reduction=facteur_reduction_bruit,
        )
        fond_avec_bruit = Image.alpha_composite(fond, couche_bruit)

        couche_etoiles = dessiner_etoiles_frame(etoiles, frame_idx, largeur, hauteur)
        frame_complete = composer_image(fond_avec_bruit, couche_etoiles)

        nom_fichier = os.path.join(dossier_sortie, f"frame_{frame_idx:04d}.png")
        frame_complete.save(nom_fichier)

        if (frame_idx + 1) % 50 == 0 or frame_idx == nb_frames - 1:
            print(f"  Images générées : {frame_idx + 1}/{nb_frames}", flush=True)

    print("Génération des images terminée.", flush=True)


def assembler_video_ffmpeg(dossier_sortie: str = "frames", nom_video: str = "out.avi", framerate: int = 25):
    """Assemble les images avec FFmpeg en appelant la commande ffmpeg."""
    print(f"Assemblage de la vidéo avec FFmpeg ({nom_video})...")

    pattern_input = os.path.join(dossier_sortie, "frame_%04d.png")

    cmd = [
        "ffmpeg",
        "-y",  # Écrase le fichier de sortie s'il existe déjà
        "-framerate", str(framerate),
        "-i", pattern_input,
        "-c:v", "ffv1",
        nom_video,
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Vidéo '{nom_video}' créée avec succès !")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'assemblage FFmpeg : {e}")
    except FileNotFoundError:
        print("FFmpeg n'a pas été trouvé dans le PATH système.")


if __name__ == "__main__":
    generer_animation(nb_frames=400, nb_etoiles=300)
    assembler_video_ffmpeg()