from pygame import Rect, Vector2 as v2
from abc import ABC, abstractclassmethod

class WindowComponent(ABC):

    def __init__(self, rect : Rect):
        self.rect = rect

    @abstractclassmethod
    def draw(self) -> None:
        """Draws the element on the window
        """ 
        ...

    def is_clicked(self, mouse: v2) -> bool:
        """Checks if a mouse click hit the component hitbox

        Args:
            mouse (v2): mouse coordinates

        Returns:
            bool: True if the click was on the component
        """
        return self.rect.collidepoint(mouse.x, mouse.y)
