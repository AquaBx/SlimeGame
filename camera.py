from pygame import Vector2, Rect
from config import GameState

class Camera:

    def __init__(self, link):
        self.link = link
        self.rect: Rect = Rect((1,1),(1,1))

    def update(self):
        """
        update le rect de la caméra en centrant le link par rapport à celle-ci
        """

        size: Vector2 = Vector2(GameState.GAME_SURFACE.get_size())

        xcam = (self.link.rect.right + self.link.rect.left  )/2 - size.x/2
        ycam = (self.link.rect.top   + self.link.rect.bottom)/2 - size.y/2
        
        self.rect: Rect = Rect(xcam , ycam , size.x , size.y)

    def transform_coord(self, position: Vector2) -> Vector2:
        """
        fonction qui va prendre en paramètre un Vector2 d'un objet (entité ou block)
        et qui va ré-envoyer un nouveau Vector2 de cet objet là ou il doit être dessiné à l'écran
        """
        fixed: bool = False
        # retire la position de la caméra si la position n'est pas fixe
        return position - Vector2(self.rect.topleft) * (not fixed)
