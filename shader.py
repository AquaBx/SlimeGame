import pygame
from PIL import Image, ImageDraw,ImageFilter
from config import GameConfig, GameState

def pilImageToSurface(pilImage):
    return pygame.image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()

def draw_a_light(center,color,radius,intensity=75):
    if not GameConfig.Graphics.EnableLights : return
    color_layer = Image.new('RGBA', GameConfig.GAME_SURFACE.get_size() , color)
    mask = Image.new("L", color_layer.size, (0))
    draw = ImageDraw.Draw(mask)

    p1 = (center[0]-radius,center[1]-radius)
    p2 = (center[0]+radius,center[1]+radius)
    shape = (p1,p2)
    
    draw.ellipse(shape, fill=intensity)
    GameState.shader = Image.composite(color_layer, GameState.shader, mask)
    
def reset():
    if not GameConfig.Graphics.EnableLights : return

    GameState.shader = Image.new('RGBA', GameConfig.GAME_SURFACE.get_size() , (0,0,15,GameConfig.opacity_world))

def draw():
    if not GameConfig.Graphics.EnableLights : return

    img = pilImageToSurface(GameState.shader.filter(ImageFilter.GaussianBlur(10)))
    GameConfig.GAME_SURFACE.blit(img,(0,0))
    