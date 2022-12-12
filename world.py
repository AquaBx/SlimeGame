import pygame as pg
from pygame import transform, image, sprite
from pygame import Vector2 as v2

import numpy as np

from config import GameConfig,GameState
from Assets.scripts.gameobject import GameObject, Ground, Player,Empty
from camera import Camera

from debug import debug

class World():
    def __init__(self) -> None:
        self.background = transform.scale( image.load("Assets/Sprites/Background/background.png"), (GameConfig.WINDOW_SIZE.x, GameConfig.WINDOW_SIZE.y) )
        # remplacer par le chargement de la map
        self.blocks = np.array([
            [Ground(1, v2(j, 0), f"Assets/Sprites/Statics/ground.png") for j in range(10)],
            [Ground(1, v2(0, 1), f"Assets/Sprites/Statics/ground.png")]+[Empty(0, v2(j, 1)) for j in range(1,9)]+[Ground(1, v2(9, 1), f"Assets/Sprites/Statics/ground.png")],
            [Ground(1, v2(j, 2), f"Assets/Sprites/Statics/ground.png") for j in range(8)]+[Empty(0, v2(8, 2))]+[Ground(1, v2(9, 2), f"Assets/Sprites/Statics/ground.png")],
            [Ground(1, v2(0, 3), f"Assets/Sprites/Statics/ground.png")]+[Empty(0, v2(j, 3)) for j in range(1,9)]+[Ground(1, v2(9, 3), f"Assets/Sprites/Statics/ground.png")],
            [Ground(1, v2(j, 4), f"Assets/Sprites/Statics/ground.png") for j in range(10)],
        ])
        # self.blocks: np.ndarray[GameObject] = np.full((3, 3), None)
        # for i in range(3):
        #     for j in range(3):
        #         self.blocks[i, j] = Ground(0, v2(j, i, f"assets/sprites/statics/ground.png")
        self.player = Player(v2(1,1), GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE, [f"assets/sprites/Dynamics/GreenSlime/Grn_Idle{i}.png" for i in range(1,11)])
        self.camera: Camera = Camera(self.player)

    def update(self) -> None:
        self.camera.update()
        self.player.update_frame()
        self.update_pos(self.player)

    def draw(self) -> None:
        link = self.camera.link
        link.draw(self.camera)
        link.sante -= 0.0001
        health_percent = link.sante/link.santemax * GameConfig.BLOCK_SIZE*5
        pg.draw.rect(GameConfig.WINDOW,"red",pg.Rect(GameConfig.BLOCK_SIZE/2,GameConfig.WINDOW_SIZE.y-GameConfig.BLOCK_SIZE,GameConfig.BLOCK_SIZE*5,GameConfig.BLOCK_SIZE/2))
        pg.draw.rect(GameConfig.WINDOW,"green",pg.Rect(GameConfig.BLOCK_SIZE/2,GameConfig.WINDOW_SIZE.y-GameConfig.BLOCK_SIZE,health_percent,GameConfig.BLOCK_SIZE/2))

        for j in range( max(0, int(self.camera.rect.left / GameConfig.BLOCK_SIZE) ) , min( len(self.blocks[0]) , int(self.camera.rect.right / GameConfig.BLOCK_SIZE ) + 1 ) ):
            for i in range( max(0, int(self.camera.rect.top / GameConfig.BLOCK_SIZE) ) , min( len(self.blocks) ,  int(self.camera.rect.bottom / GameConfig.BLOCK_SIZE) + 1 ) ):
                self.blocks[i, j].draw(self.camera)

    def gravite(self,obj):
        y_vect = 5 * GameConfig.BLOCK_SIZE
        gravite = v2(0, y_vect)
        obj.acceleration.y = gravite[1] # + resistance[1]
        obj.vitesse.y += self.player.acceleration.y*GameState.dt
        obj.position.y += self.player.vitesse.y*GameState.dt

    def update_pos(self,obj:GameObject) -> None:
        
        pos_avant = v2(obj.position.x,obj.position.y)

        obj.update()
        self.gravite(obj)

        # we get all 4 blocs (*) based on the position of the player (p)
        # | | | | |
        # | |p|*| |
        # | |*|*| |
        # | | | | |
        # for now there is a out of bound exception when we are not on the grid anymore

        x1 = int( obj.position_matrix.x )
        y1 = int( obj.position_matrix.y )

        blocks_arround = {
            "top-left" : { "ref":self.blocks[y1, x1] },
            "bottom-left" : { "ref":self.blocks[y1+1, x1] },
            "top-right" : { "ref":self.blocks[y1, x1+1] },
            "bottom-right" : { "ref":self.blocks[y1+1, x1+1] }
        }
        
        for key in blocks_arround:
            obj2 = blocks_arround[key]["ref"]
            offset: v2 = obj2.position - obj.position
            collide = obj.mask.overlap(obj2.mask, offset)
            blocks_arround[key]["collide"] = True if collide else False
        
        dir = obj.position - pos_avant

        if dir.y < 0 and ( blocks_arround["top-left"]["collide"] or blocks_arround["top-right"]["collide"] ):
            obj.position.y = blocks_arround["top-left"]["ref"].rect.bottom
            obj.vitesse.y = 0
            obj.acceleration.y = 0
        if dir.y > 0 and ( blocks_arround["bottom-right"]["collide"] or blocks_arround["bottom-left"]["collide"] ):
            obj.position.y = blocks_arround["bottom-left"]["ref"].rect.top - blocks_arround["bottom-left"]["ref"].taille.x
            obj.vitesse.y = 0
            obj.acceleration.y = 0

        for key in blocks_arround:
            obj2 = blocks_arround[key]["ref"]
            offset: v2 = obj2.position - obj.position
            collide = obj.mask.overlap(obj2.mask, offset)
            blocks_arround[key]["collide"] = True if collide else False

        if dir.x < 0 and ( blocks_arround["top-left"]["collide"] or blocks_arround["bottom-left"]["collide"] ):
            obj.position.x = blocks_arround["top-left"]["ref"].rect.right
            obj.vitesse.x = 0
            obj.acceleration.x = 0
        if dir.x > 0 and ( blocks_arround["top-right"]["collide"] or blocks_arround["bottom-right"]["collide"] ):
            obj.position.x = blocks_arround["top-right"]["ref"].rect.left - blocks_arround["top-right"]["ref"].taille.x
            obj.vitesse.x = 0
            obj.acceleration.x = 0