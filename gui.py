from pygame import Rect,Surface, Vector2 as v2
from abc import ABC,abstractclassmethod
import pygame as pg
from config import GameState

class GUIComponent(ABC):
    def __init__(self, position: v2, size: v2, id: str) -> None:
        self.position: v2 = position
        self.size: v2 = size
        self.id = id

    @property
    @abstractclassmethod
    def surface(self) -> Surface : ...

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, GUIComponent) and self.id == __o.id

    def __hash__(self) -> int:
        return hash(self.id)
    
class HealthBar(GUIComponent):
    def __init__(self, link: object, id: str):
        self.texture = pg.image.load("assets/UI/healthbar.png").convert_alpha()
        GUIComponent.__init__(self, v2(10,GameState.GAME_SURFACE.get_size()[1]-self.texture.get_size()[1]-10), self.texture.get_size(), id)
        self.link = link

    @property
    def surface(self) -> Surface:
        surface = Surface(self.size, pg.SRCALPHA).convert_alpha()

        health_percent = self.link.health/self.link.max_health * 29
        pg.draw.rect( surface, (255,7,3) , Rect(10,2,health_percent,3))
        surface.blit(self.texture, (0,0))

        return surface
    
class GUI:
    components: set[GUIComponent] = set()
    
    def add_component(component: GUIComponent) -> None:
        GUI.components.add(component)

    def remove_component(component: GUIComponent) -> None:
        GUI.components.remove(component)

    def has_component(component: GUIComponent) -> bool:
        return component in GUI.components

    def upsert_component(component: GUIComponent) -> None:
        """add or update a component

        Args:
            component (GUIComponent): the component to upsert
        """
        if GUI.has_component(component):
            GUI.remove_component(component)
        GUI.add_component(component)


    def draw(window : Surface) -> None:
        
        for gc in GUI.components:
            window.blit(gc.surface,gc.position)

