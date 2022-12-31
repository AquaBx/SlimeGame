import pygame as pg
from PIL import Image, ImageDraw,ImageFilter
from config import GameConfig, GameState

def pilImageToSurface(pilImage:Image) -> pg.Surface:
    """
    Fonction qui transforme une Image en Surface Pygame
    """
    return pg.image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()

def SurfaceTopilImage(surface:pg.Surface) -> Image:
    """
    Fonction qui transforme une Surface Pygame en Matrice pour PIL (Image)
    """

    surf = pg.transform.rotate(surface,-90)
    surf = pg.transform.flip(surf,True,False) # pygame renvoie la transposé donc je rotate et je flippe
    arr = pg.surfarray.array3d(surf)
    return Image.fromarray(arr)


def draw_a_light(center:tuple,color:pg.Color,radius:int) -> None:
    """
    fonction qui va blit un halo lumineux sur notre Surface Shader
    """

    if not GameConfig.Graphics.EnableLights : return
    mask = Image.new("RGBA", GameState.GAME_SURFACE.get_size())
    draw = ImageDraw.Draw(mask)

    p1 = (center[0]-radius,center[1]-radius)
    p2 = (center[0]+radius,center[1]+radius)
    shape = (p1,p2)
    
    draw.ellipse(shape, fill=color)
    

    circle = pilImageToSurface( mask )
    GameState.shader.blit(circle,(0,0))
    
def reset() -> None:
    """
    fonction qui va reset notre Surface Shader
    """
    if not GameConfig.Graphics.EnableLights : return

    GameState.shader = pg.Surface(GameState.GAME_SURFACE.get_size())
    GameState.shader.fill(GameConfig.ambient_color_world)

def draw() -> None:
    """
    Fonction qui draw notre Surface Shader sur notre GameSurface
    """
    if not GameConfig.Graphics.EnableLights : return
    img = SurfaceTopilImage(GameState.shader) # convertion de l'image pour ensuite appliqué un gaussien
    img = img.filter( ImageFilter.GaussianBlur(10) )
    img = pilImageToSurface(img) # convertion en surface
    GameState.GAME_SURFACE.blit(img,(0,0),special_flags=pg.BLEND_MULT)
    