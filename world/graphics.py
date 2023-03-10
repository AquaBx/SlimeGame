import pygame as pg
from pygame import Vector2 as v2

from config import GameConfig, GameState
from assets.scripts.gameobject_attributes import LightSource

def draw(world) -> None:

    """ initialisation du draw """
    surface_size: v2 = v2(GameState.GAME_SURFACE.get_size())
    LightSource.reset() # initialisation des lights
    background_rect: pg.Rect = world.background.get_rect()

    """ affichage du monde """
    # itération de tout les blocks visibles
    
    croped_rect: pg.Rect = GameState.camera.rect.clip(background_rect)
    offset: v2 = v2((surface_size.x-croped_rect.size[0]) * (not bool(croped_rect.x)), (surface_size.y-croped_rect.size[1]) * (not bool(croped_rect.y)))
    GameState.GAME_SURFACE.blit(world.background.subsurface(croped_rect), offset)

    """ affichage des joueurs / mobs """
    world.player.update_frame()
    world.player.draw(GameState.camera)

    for enemy in world.enemies:
        enemy.update_frame()
        enemy.draw(GameState.camera)

    """ draw lights """
    if GameConfig.gameGraphics.EnableLights:
        LightSource.draw(GameState.camera)
