from pygame import Rect,Surface, Vector2 as v2
from abc import ABC,abstractclassmethod
import pygame as pg
from config import GameState

class GUIComponent(ABC):
    def __init__(self, position: v2, size: v2) -> None:
        self.position: v2 = position
        self.size: v2 = size

    @property
    @abstractclassmethod
    def surface(self) -> Surface : ...
    
class HealthBar(GUIComponent):
    def __init__(self, link):
        self.texture = pg.image.load("assets/UI/healthbar.png").convert_alpha()
        GUIComponent.__init__(self, v2(10,GameState.GAME_SURFACE.get_size()[1]-self.texture.get_size()[1]-10), self.texture.get_size())
        self.link = link

    @property
    def surface(self) -> Surface:
        surface = Surface(self.size, pg.SRCALPHA).convert_alpha()

        health_percent = self.link.health/self.link.max_health * 29
        pg.draw.rect( surface, (255,7,3) , Rect(10,2,health_percent,3))
        surface.blit(self.texture, (0,0))

        return surface
    
class GUI:
    components: set = set()
    
    def add_component(Component: GUIComponent) -> None:
        GUI.components.add(Component)

    def draw(window : Surface) -> None:
        for gc in GUI.components:
            window.blit(gc.surface,gc.position)

