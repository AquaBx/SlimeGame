import pygame
from PIL import Image, ImageDraw,ImageFilter
from config import GameConfig, GameState

def pilImageToSurface(pilImage):
    return pygame.image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode)

def draw_a_ligth(center,color,radius):
    color_layer = Image.new('RGBA', GameConfig.GAME_SURFACE.get_size() , color)
    mask = Image.new("L", color_layer.size, (0))
    draw = ImageDraw.Draw(mask)

    p1 = (center[0]-radius,center[1]-radius)
    p2 = (center[0]+radius,center[1]+radius)
    shape = (p1,p2)

    draw.ellipse(shape, fill=75)

    mask_blur = mask.filter(ImageFilter.GaussianBlur(radius/2))
    GameState.shader = Image.composite(color_layer, GameState.shader, mask_blur)

def reset():
    GameState.shader = Image.new('RGBA', GameConfig.GAME_SURFACE.get_size() , (0,0,15,GameConfig.opacity_world))

def draw():
    img = pilImageToSurface(GameState.shader)
    GameConfig.GAME_SURFACE.blit(img,(0,0))