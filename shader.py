import pygame
from PIL import Image, ImageDraw,ImageFilter
from config import GameConfig, GameState

res_reduc = GameConfig.WINDOW_SIZE.y/96


import time

def pilImageToSurface(pilImage):
    new_size = (int(GameConfig.WINDOW_SIZE.x) , int(GameConfig.WINDOW_SIZE.y))
    img = pygame.transform.scale( pygame.image.frombytes(pilImage.tobytes(), pilImage.size, pilImage.mode), new_size ).convert_alpha()
    img.set_alpha(GameConfig.opacity_world)
    return img

def draw_a_ligth(center,color,radius):
    
    imBlack = Image.new('RGB', [ int(GameConfig.WINDOW_SIZE.x/res_reduc) , int(GameConfig.WINDOW_SIZE.y/res_reduc) ], color)
    mask = Image.new("L", imBlack.size, (0))
    draw = ImageDraw.Draw(mask)

    p1 = (center[0]/res_reduc-radius/res_reduc,center[1]/res_reduc-radius/res_reduc)
    p2 = (center[0]/res_reduc+radius/res_reduc,center[1]/res_reduc+radius/res_reduc)
    shape = (p1,p2)

    draw.ellipse(shape, fill=radius)

    mask_blur = mask.filter(ImageFilter.GaussianBlur(radius/2/res_reduc))
    GameState.shader = Image.composite(imBlack, GameState.shader, mask_blur)

def reset():
    GameState.shader = Image.new('RGB', [ int(GameConfig.WINDOW_SIZE.x/res_reduc) , int(GameConfig.WINDOW_SIZE.y/res_reduc) ], (0,0,0))

def draw():
    img = pilImageToSurface(GameState.shader)
    GameConfig.WINDOW.blit(img,(0,0))