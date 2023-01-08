# libraries
import pygame as pg
from pygame import Surface, Color, Vector2 as v2
from pygame.mask import Mask
from abc import ABC, abstractclassmethod
from config import GameConfig

# utils
from utils import coords_to_v2
from assets.palette import Palette

# entity
from assets.scripts.renderable import Renderable
from assets.scripts.gameobject_attributes import LightSource, Damager

class MapElement(Renderable, ABC):
    """Élément nécessaire pour construire le niveau du jeu\n
    Définie une méthode static `create` et un `mask` de collision pour chaque entité appartenant au décors.\n
    - Hérite de Renderable <- GameObject
    """

    @abstractclassmethod
    def create(coords: tuple[int, int], id: int, state: int, uuid: int) -> None: ...
        
    def __init__(self, coords: tuple[int, int], texture: Surface, collidable: bool = True) -> None:
        """MapElement(constructeur)

        Paramètres:
            coords (tuple[int, int]): la position dans la matrice du niveau.
            texture (pg.Surface): une référence vers la texture à afficher.
            collidable (bool, optional): Si Vrai alors le `mask` correspond à la texture, sinon le `mask` est vide. Défaut à True.
        """
        Renderable.__init__(self, coords_to_v2(coords), texture)
        self.mask: Mask = pg.mask.from_surface(self.texture) if collidable else Mask((0, 0))
    
    def compute_state(map, palette, edges, id, coords) -> int: 
        return 0

    
    def default_state() -> int:
        return 0

class Platform(MapElement):
    """Élément représentant une platforme dans le niveau 
    - Hérite de MapElement <- Renderable <- GameObject
    """
    def create(coords: tuple[int, int], id: int, state: int, uuid: int) -> None:
        return Platform(coords, Palette.get_texture(id, state))

    # on ajoutera sans doute ici les connected Textures

    __scoring_table = { # This table is only correct for Ground types
            28 : 0 , 124: 1 , 112: 2 , 16 : 3 , 247: 4 , 223: 5 ,
            31 : 6 , 255: 7 , 241: 8 , 17 : 9 , 253: 10, 127: 11,
            7  : 12, 199: 13, 193: 14, 1  : 15, 23 : 16, 209: 17,
            4  : 18, 68 : 19, 64 : 20, 0  : 21, 29 : 22, 113: 23,
            125: 24, 245: 25, 93 : 26, 117: 27, 20 : 28, 80 : 29,
            95 : 30, 215: 31, 87 : 32, 213: 33, 5  : 34, 65 : 35,
            116: 36, 92 : 37, 21 : 38, 84 : 39, 119: 40, 221: 41,
            197: 42, 71 : 43, 69 : 44, 81 : 45, 85 : 46
        }

    def compute_state(map, palette, edges, id, coords) -> int: 
        # has neighboor
        (t,  r,  b,  l )  = (False, False, False, False)
        (tr, rb, bl, lt)  = (False, False, False, False)
        i,j = coords
        # 4 neighboors
        # side is calculated if there is no OOB risk
        t = (not edges[0])   and (id == map[i-1, j].id)
        r = (not edges[1])   and (id == map[i, j+1].id)
        b = (not edges[2])   and (id == map[i+1, j].id)
        l = (not edges[3])   and (id == map[i, j-1].id)

        # 8 neighboors
        # corner is calculated if the 2 connected sides match with the current tile 
        tr = (t and r) and (id == map[i-1,j+1].id)
        rb = (r and b) and (id == map[i+1,j+1].id)
        bl = (b and l) and (id == map[i+1,j-1].id)
        lt = (l and t) and (id == map[i-1,j-1].id)

        # score calculation uses base2 to base10 system
        score = sum([((1<<i)*border) for i, border in enumerate([t, tr, r, rb, b, bl, l, lt])])
        
        return Platform.__scoring_table[score]
    
    def default_state() -> int:
        return 21

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

    def __init__(self, coords: tuple[int, int], texture: Surface) -> None:
        MapElement.__init__(self, coords, texture, False)
        LightSource.__init__(self)

    @property
    def emit_position(self) -> v2:
        return self.rect.center

class Spike(MapElement, Damager, LightSource):

    def create(coords: tuple[int, int], id: int, state: int, uuid: int) -> None:
        return Spike(coords, Palette.get_texture(id, state))

    def __init__(self, coords: tuple[int, int], texture: Surface):
        MapElement.__init__(self, coords, texture)
        LightSource.__init__(self, radius=int(0.9*GameConfig.BLOCK_SIZE), glow=Color(230, 230, 230, 128))
        
    @property
    def damage(self) -> int: return 50

    @property
    def hurt_time(self) -> int: return 2

    @property
    def bump_factor(self) -> int: return 3

    @property
    def emit_position(self) -> v2:
        return self.rect.center