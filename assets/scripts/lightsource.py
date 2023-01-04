import pygame as pg
from pygame import Surface, Color, Vector2 as v2
from PIL import Image as Img, ImageFilter, ImageDraw
from PIL.Image import Image
from abc import ABC, abstractclassmethod

from camera import Camera
from config import GameConfig, GameState

def surface_to_pil(surf: Surface) -> Image:
    arr = pg.surfarray.array3d(surf)
    return Img.fromarray(arr)

def pil_to_surface(pilImage) -> Surface:
    return pg.image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()

class LightSource(ABC):
    """Permet à un élément du jeu d'émettre une aura de lumière autour de lui\n
    
    Attributs:
    - glow: tuple[int, int, int] -> teinte en RGB de la lumière. `default: (230, 199, 119)`
    - radius: int -> taille du rayon d'émission. `default: 2*GameConfig.BLOCK_SIZE`
    - light_mask: pygame.Surface -> surface représentant le mask de lumière

    Propriété:
    - emit_position: pygame.Vector2 -> centre du cercle d'émission de lumière (à redéfinir par les classes héritières)
    """

    # list[LightSource]
    sources: list = list()
    filter: Surface = None

    def __init__(self, radius: int = 3*GameConfig.BLOCK_SIZE, glow: Color = Color(230, 199, 119), centered: bool = True) -> None:
        self.radius: int = radius
        self.glow: Color = glow
        self.centered: bool = centered

        surface = Img.new("RGBA", (3*self.radius, 3*self.radius), (0, 0, 0, 0))
        draw = ImageDraw.Draw(surface)


        w, h = surface.size
        p1 = (w/2 - (self.radius*0.90), h/2 - (self.radius*0.9))
        p2 = (w/2 + (self.radius*0.9), h/2 + (self.radius*0.9))
        shape = (p1,p2)

        draw.ellipse(shape, fill=(self.glow.r, self.glow.g, self.glow.b))

        surface_blured = surface .filter(ImageFilter.GaussianBlur(self.radius/5))

        self.light_mask: Surface = pg.transform.scale(pil_to_surface(surface_blured), (2*self.radius, 2*self.radius))
        LightSource.sources.append(self)

    # il faut la redéfinir pour chaque enfant
    @property
    @abstractclassmethod
    def emit_position(self) -> v2:
        """Cette fonction doit être redéfinie par chaque enfant.\n
        Elle donne la position (top, left) de la lumière.

        Returns:
            pg.Vector2: la position suppérieur gauche du filtre lumineux
        """
        ...

    def reset() -> None:
        LightSource.filter = Surface(GameState.GAME_SURFACE.get_size())
        LightSource.filter.fill(GameConfig.ambient_color_world)

    def draw(camera: Camera) -> None:
        for light in LightSource.sources:
            # on récupère la position dans l'espace de la caméra et on centre si indiqué
            dist: v2 = camera.transform_coord(light.emit_position-(v2(light.radius)*light.centered))
            LightSource.filter.blit(light.light_mask, dist)
        GameState.GAME_SURFACE.blit(LightSource.filter, (0, 0), special_flags=pg.BLEND_MULT)
