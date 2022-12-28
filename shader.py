import pygame as pg
from PIL import Image, ImageDraw,ImageFilter
from config import GameConfig, GameState

def pilImageToSurface(pilImage):
    return pg.image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()

def SurfaceTopilImage(surface):
    surf = pg.transform.rotate(surface,-90)
    surf = pg.transform.flip(surf,True,False)
    arr = pg.surfarray.array3d(surf)
    return Image.fromarray(arr)


def draw_a_light(center,color,radius,intensity=75):
    if not GameConfig.Graphics.EnableLights : return
    mask = Image.new("RGBA", GameState.GAME_SURFACE.get_size() , (intensity))
    draw = ImageDraw.Draw(mask)

    p1 = (center[0]-radius,center[1]-radius)
    p2 = (center[0]+radius,center[1]+radius)
    shape = (p1,p2)
    
    draw.ellipse(shape, fill=color)

    circle = pilImageToSurface( mask )
    GameState.shader.blit(circle,(0,0))
    
def reset():
    if not GameConfig.Graphics.EnableLights : return

    GameState.shader = pg.Surface(GameState.GAME_SURFACE.get_size())
    GameState.shader.fill((15,15,15,GameConfig.opacity_world))

def draw():
    if not GameConfig.Graphics.EnableLights : return
    img = SurfaceTopilImage(GameState.shader)
    img = img.filter( ImageFilter.GaussianBlur(10) )
    img = pilImageToSurface(img)
    GameState.GAME_SURFACE.blit(img,(0,0),special_flags=pg.BLEND_MULT)
    