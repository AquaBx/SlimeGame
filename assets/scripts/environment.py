# libraries
import pygame as pg

# utils
from config import GameConfig
from assets.palette import Palette

# entity
from assets.scripts.renderable import Renderable
from assets.scripts.lightsource import LightSource

class MapElement(Renderable):
    """Élément nécessaire pour construire le niveau du jeu\n
    Définie une méthode static `create` et un `mask` de collision pour chaque entité appartenant au décors.\n
    - Hérite de Renderable <- GameObject
    """
    def create(coords: tuple[int, int], id: int, state: int, uuid: int):
        return MapElement(coords, Palette.get_texture(id, state))

    def __init__(self, coords: tuple[int, int], texture: pg.Surface, collidable: bool = True) -> None:
        """MapElement(constructeur)

        Paramètres:
            coords (tuple[int, int]): la position dans la matrice du niveau.
            texture (pg.Surface): une référence vers la texture à afficher.
            collidable (bool, optional): Si Vrai alors le `mask` correspond à la texture, sinon le `mask` est vide. Défaut à True.
        """
        Renderable.__init__(self, pg.Vector2(coords[1], coords[0]) * GameConfig.BLOCK_SIZE, texture)
        self.mask: pg.Mask = pg.mask.from_surface(self.texture) if collidable else pg.Mask((0, 0))

class Platform(MapElement):
    """Élément représentant une platforme dans le niveau 
    - Hérite de MapElement <- Renderable <- GameObject
    """
    # on ajoutera sans doute ici les connected Textures

# placeholder pour Assets
class Background:
    ...

class Lamp(MapElement, LightSource):
    """Élément de décors emettant de la lumière\n
    Redéfinie la méthode static `create` pour générer une `Lamp`
    
    - Hérite de (MapElement, LightSource) <- (Renderable, ) <- (GameObject, )
    """

    def create(coords: tuple[int, int], id: int, state: int, uuid: int):
        return Lamp(coords, Palette.get_texture(id, state))

    def __init__(self, coords: tuple[int, int], texture: pg.Surface) -> None:
        MapElement.__init__(self, coords, texture, False)
        LightSource.__init__(self)

    @property
    def emit_position(self) -> pg.Vector2:
        return self.rect.center
