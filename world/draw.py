import pygame as pg
from pygame import transform
from pygame import Rect
from config import GameConfig, GameState
import shader

def draw(self) -> None:

    """ initialisation du draw """
    surface_size = GameState.GAME_SURFACE.get_size()
    shader.reset() # initialisation des lights
    GameState.GAME_SURFACE.fill('Black')

    """ affichage du monde """
    # itération de tout les blocks visibles
    for j in range( max(0, int(self.camera.rect.left / GameConfig.BLOCK_SIZE ) ) , min( len(self.blocks[0]) , int(self.camera.rect.right / GameConfig.BLOCK_SIZE ) + 1 ) ):
        for i in range( max(0, int(self.camera.rect.top / GameConfig.BLOCK_SIZE ) ) , min( len(self.blocks) ,  int(self.camera.rect.bottom / GameConfig.BLOCK_SIZE) + 1 ) ):
            self.blocks[i, j].draw(self.camera)

    """ affichage des joueurs / mobs """
    self.player.draw(self.camera)

    """ draw lights """
    shader.draw()

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
