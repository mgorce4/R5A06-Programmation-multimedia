import os
import subprocess
from dataclasses import dataclass
from random import randint
from PIL import Image, ImageDraw


@dataclass
class Etoile:
    """Créer une étoile basé sur la base d'un cercle
     x est la position horizontale, y est la position verticale, 
     rayon est le rayon du cercle, couleur est un tuple RGBA et la vitesse de déplacement."""

    x: float
    y_init: float
    rayon: int
    couleur: tuple[int, int, int, int]
    vitesse: float


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
    aux bordures supérieures et inférieures.
    """
    image = Image.new("RGBA", (largeur, hauteur), (0, 0, 0, 0))
    dessin = ImageDraw.Draw(image)

    for etoile in etoiles:
        # Calcul de la position y actuelle avec modulo pour le bouclage parfait
        y_actuel = (etoile.y_init + frame_idx * etoile.vitesse) % hauteur
        r = etoile.rayon

        # Dessin principal et dessins secondaires aux bords (wrapping top/bottom)
        for offset_y in (0, -hauteur, hauteur):
            y_draw = y_actuel + offset_y
            # On ne dessine que si l'étoile dépasse sur la zone visible
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


def composer_image(fond_rgba: Image.Image, etoiles: Image.Image) -> Image.Image:
    """Assemble le fond et la couche transparente contenant les étoiles."""
    return Image.alpha_composite(fond_rgba, etoiles)


def generer_animation(nb_frames: int , nb_etoiles: int ,dossier_sortie: str = "frames",fichier_fond: str = "__fondNoir.png",
):
    """Génère la suite de PNGs constituant l'animation. et les placent dan le dossier frames"""
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    fond = Image.open(fichier_fond).convert("RGBA")
    largeur, hauteur = fond.size

    print(f"Génération de {nb_etoiles} étoiles pour une image de {largeur}x{hauteur}...")
    etoiles = generer_etoiles(nb_etoiles, largeur, hauteur, nb_frames=nb_frames)

    print(f"Génération des {nb_frames} images dans le dossier '")
    for frame_idx in range(nb_frames):
        couche_etoiles = dessiner_etoiles_frame(etoiles, frame_idx, largeur, hauteur)
        frame_complete = composer_image(fond, couche_etoiles)
        
        nom_fichier = os.path.join(dossier_sortie, f"frame_{frame_idx:04d}.png")
        frame_complete.save(nom_fichier)
        
        if (frame_idx + 1) % 50 == 0 or frame_idx == nb_frames - 1:
            print(f"  Images générées : {frame_idx + 1}/{nb_frames}", flush=True)

    print("Génération des images terminée.", flush=True)


def assembler_video_ffmpeg(dossier_sortie: str = "frames",nom_video: str = "out.avi",framerate: int = 25,
):
    """Assemble les images avec FFmpeg en appelant la commande ffmpeg"""
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
