from pygame import Rect
from config import GameState

class Camera:

    def __init__(self, link):
        self.link = link

    def update(self):
        """
        update le rect de la caméra en centrant le link par rapport à celle-ci
        """

        size = GameState.GAME_SURFACE.get_size()

        xcam = (self.link.rect.right + self.link.rect.left  )/2 - size[0]/2
        ycam = (self.link.rect.top   + self.link.rect.bottom)/2 - size[1]/2
        
        self.rect: Rect = Rect(xcam , ycam , size[0] , size[1])

    def transform_coord(self, entity: Rect) -> Rect:
        """
        fonction qui va prendre en paramètre un rect d'un objet (entité ou block)
        et qui va ré-envoyer un nouveau rect de cet objet là ou il doit être dessiné à l'écran
        """

        fixed: bool = False

        newx: float = entity.left
        newy: float = entity.top

        if not fixed :  
            newx -= self.rect.left
            newy -= self.rect.top

        return Rect(newx , newy, entity.width, entity.height)
