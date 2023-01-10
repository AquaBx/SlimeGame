# libraries
import pygame as pg
from pygame import Surface, Color, Vector2 as v2
from PIL import Image as Img, ImageFilter, ImageDraw
from PIL.Image import Image

# standard
from abc import ABC, abstractclassmethod

# utils
from camera import Camera
from config import GameConfig, GameState
from eventlistener import EventManager, Listener
from customevents import CustomEvent, ChangeStageEvent, PlayerActionEvent

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
        self.__glow: Color = glow
        self.centered: bool = centered

        self.light_mask: Surface = self.__generate_light_mask()
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

    def __generate_light_mask(self) -> Surface:
        surface = Img.new("RGBA", (3*self.radius, 3*self.radius), (0, 0, 0, 0))
        draw = ImageDraw.Draw(surface)

        w, h = surface.size
        p1 = (w/2 - (self.radius*0.90), h/2 - (self.radius*0.9))
        p2 = (w/2 + (self.radius*0.9), h/2 + (self.radius*0.9))
        shape = (p1,p2)

        draw.ellipse(shape, fill=(self.glow.r, self.glow.g, self.glow.b, self.glow.a))

        surface_blured = surface.filter(ImageFilter.GaussianBlur(self.radius/5))
        return pg.transform.scale(pil_to_surface(surface_blured), (2*self.radius, 2*self.radius))

    @property
    def glow(self) -> Color:
        return self.__glow
    
    @glow.setter
    def glow(self, color) -> None:
        if color == self.__glow: return
        
        self.__glow = color
        self.light_mask = self.__generate_light_mask()

class Damager(ABC):

    def __init__(self, damage, hurt_time, bump_factor):
        self.__damage = damage
        self.__hurt_time = hurt_time
        self.__bump_factor = bump_factor

    @property
    def damage(self) -> int: return self.__damage

    @property
    def hurt_time(self) -> int: return self.__hurt_time

    @property
    def bump_factor(self) -> int: return self.__bump_factor   

class Damagable(ABC): 
    def __init__(self, max_health: int, health: int = -1):
        """Instanciate Damaged objects

        Args:
            max_health (int): the maximum health of the entity
            health (int, optional): the current health of the entity. Default -1 means max_health
        """
        self.hurt_time: int = 0
        self.max_health = max_health
        if(health == -1): self._health = max_health
        else: self._health = health

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, v: int) -> None:
        if self._health == 0: return
        self._set_health(v)

    def _set_health(self, v: int) -> None:
        self._health = max(0, v)

class Dynamic(ABC):
    def __init__(self, mass: int, mask: Surface):
        self.mass: int = mass
        self.is_flying: bool = True
        self.velocity: v2 = v2(0.0)
        self.acceleration: v2 = v2(0.0)
        self.mask = pg.mask.from_surface(mask)

    @abstractclassmethod
    def update() -> None: ...

class Warp(Listener, ABC):

    def __init__(self, uuid: int, next_map: str, next_position: tuple[int, int]) -> None:
        Listener.__init__(self, ["player_action"], f"warp{uuid}")
        self.next_map: str = next_map
        self.next_position: tuple[int, int] = next_position

    @property
    @abstractclassmethod
    def warp_zone(self) -> pg.Rect:
        ...

    def notify(self, ce: CustomEvent) -> None:
        pae: PlayerActionEvent = ce
        if self.warp_zone.colliderect(pae.player.rect):
            EventManager.push_event(ChangeStageEvent(self.next_map, self.next_position))
