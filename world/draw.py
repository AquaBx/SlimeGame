import pygame as pg
from pygame import transform,Rect,Vector2 as v2

from config import GameConfig, GameState
from assets.scripts.lightsource import LightSource
from debug import debug
def draw(self) -> None:

    """ initialisation du draw """
    surface_size: v2 = v2(GameState.GAME_SURFACE.get_size())
    LightSource.reset() # initialisation des lights
    background_rect: pg.Rect = self.background.get_rect()

    """ affichage du monde """
    # itération de tout les blocks visibles
    
    croped_rect: pg.Rect = self.camera.rect.clip(background_rect)
    offset: v2 = v2((surface_size.x-croped_rect.size[0]) * (not bool(croped_rect.x)), (surface_size.y-croped_rect.size[1]) * (not bool(croped_rect.y)))
    GameState.GAME_SURFACE.blit(self.background.subsurface(croped_rect), offset)

    """ affichage des joueurs / mobs """
    self.player.update_frame()
    self.player.draw(self.camera)

    """ draw lights """
    LightSource.draw(self.camera)

    """ affichage UI """
    # recuperation de l'entité lié à la caméra
    link = self.camera.link

    # draw healthbar
    mr_bottom = surface_size[1]-2*surface_size[1]/20
    scale = 1/7*surface_size[1]/20
    health_percent = link.sante/link.santemax * 29 * scale
    pg.draw.rect( GameState.GAME_SURFACE, (255,7,3) , Rect(surface_size[1]/20+10*scale,mr_bottom+2*scale,health_percent,3*scale))
    GameState.GAME_SURFACE.blit( GameConfig.HealthBar,(surface_size[1]/20,mr_bottom) )
    
    """ blit fenetre """
    # upscale sur la taille de la fenetre
    GameState.WINDOW.blit(transform.scale(GameState.GAME_SURFACE, GameState.WINDOW.get_size()),(0,0))

    debug((int(1/GameState.dt),int(1/GameState.PhysicDT)))