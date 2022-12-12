import pygame as pg
from pygame import transform, image, sprite
from pygame import Vector2 as v2

import numpy as np

from config import GameConfig
from Assets.scripts.gameobject import GameObject, Ground, Player,Empty
from camera import Camera

class World():
    def __init__(self) -> None:
        self.background = transform.scale( image.load("Assets/Sprites/Background/background.png"), (GameConfig.WINDOW_SIZE.x, GameConfig.WINDOW_SIZE.y) )
        # remplacer par le chargement de la map
        self.blocks = np.array([
            [Ground(1, v2(j*GameConfig.BLOCK_SIZE, 0*GameConfig.BLOCK_SIZE), f"Assets/Sprites/Statics/ground.png") for j in range(10)],
            [Ground(1, v2(0*GameConfig.BLOCK_SIZE, 1*GameConfig.BLOCK_SIZE), f"Assets/Sprites/Statics/ground.png")]+[Empty(0, v2(j*GameConfig.BLOCK_SIZE, 1*GameConfig.BLOCK_SIZE)) for j in range(1,9)]+[Ground(1, v2(9*GameConfig.BLOCK_SIZE, 1*GameConfig.BLOCK_SIZE), f"Assets/Sprites/Statics/ground.png")],
            [Ground(1, v2(j*GameConfig.BLOCK_SIZE, 2*GameConfig.BLOCK_SIZE), f"Assets/Sprites/Statics/ground.png") for j in range(8)]+[Empty(0, v2(8*GameConfig.BLOCK_SIZE, 2*GameConfig.BLOCK_SIZE))]+[Ground(1, v2(9*GameConfig.BLOCK_SIZE, 2*GameConfig.BLOCK_SIZE), f"Assets/Sprites/Statics/ground.png")],
            [Ground(1, v2(0*GameConfig.BLOCK_SIZE, 3*GameConfig.BLOCK_SIZE), f"Assets/Sprites/Statics/ground.png")]+[Empty(0, v2(j*GameConfig.BLOCK_SIZE, 3*GameConfig.BLOCK_SIZE)) for j in range(1,9)]+[Ground(1, v2(9*GameConfig.BLOCK_SIZE, 3*GameConfig.BLOCK_SIZE), f"Assets/Sprites/Statics/ground.png")],
            [Ground(1, v2(j*GameConfig.BLOCK_SIZE, 4*GameConfig.BLOCK_SIZE), f"Assets/Sprites/Statics/ground.png") for j in range(10)],
        ])
        # self.blocks: np.ndarray[GameObject] = np.full((3, 3), None)
        # for i in range(3):
        #     for j in range(3):
        #         self.blocks[i, j] = Ground(0, v2(j*GameConfig.BLOCK_SIZE, i*GameConfig.BLOCK_SIZE), f"assets/sprites/statics/ground.png")
        self.player = Player(GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE, [f"assets/sprites/Dynamics/GreenSlime/Grn_Idle{i}.png" for i in range(1,11)])
        self.camera: Camera = Camera(self.player)

    def update(self) -> None:
        self.camera.update()
        self.player.update_frame()
        self.player.update()
        # self.gravite()

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

    def collision_mask(self, obj1: GameObject, others: np.ndarray[GameObject]) -> tuple[bool, int]:
        """
            le side est relative au deuxieme block
        """
        for obj2 in others:
            offset: v2 = obj2.position - obj1.position
            collide = obj1.mask.overlap(obj2.mask, offset)
            if collide != None:
                sprite.collide_mask
                return (True , obj2.rect.top)
        return (False, -1)

    def gravite(self) -> None:
        y_vect = 50 * GameConfig.BLOCK_SIZE

        gravite = v2(0, y_vect)
        # resistance = pygame.Vector2(0, 0)

        # self.player.acceleration.y = gravite[1] # + resistance[1]
        # self.player.vitesse.y += self.player.acceleration.y*GameState.dt
        # self.player.position.y += self.player.vitesse.y*GameState.dt

        # we get all 4 blocs (*) based on the position of the player (p)
        # | | | | |
        # | |p|*| |
        # | |*|*| |
        # | | | | |
        # for now there is a out of bound exception when we are not on the grid anymore
        collide, ny = self.collision_mask(self.player, [
            self.blocks[int(self.player.position.y)//int(GameConfig.BLOCK_SIZE), int(self.player.position.x)//int(GameConfig.BLOCK_SIZE)],
            self.blocks[int(self.player.position.y+self.player.taille.y)//int(GameConfig.BLOCK_SIZE), int(self.player.position.x)//int(GameConfig.BLOCK_SIZE)],
            self.blocks[int(self.player.position.y)//int(GameConfig.BLOCK_SIZE), int(self.player.position.x+self.player.taille.x)//int(GameConfig.BLOCK_SIZE)],
            self.blocks[int(self.player.position.y+self.player.taille.y)//int(GameConfig.BLOCK_SIZE), int(self.player.position.x+self.player.taille.x)//int(GameConfig.BLOCK_SIZE)]
        ])

        if collide:
            pass
            # resistance = pygame.Vector2(0, -y_vect)
            # h = 5 * GameConfig.BLOCK_SIZE
            # self.player.acceleration.y = -( 2 * gravite.y * h)**0.5/GameState.dt * int(pg.key.get_pressed()[pg.K_z])
            # obj.vitesse.y = obj.acceleration.y*dt
            # obj.position.y = ny + obj.vitesse.y*dt - self.player.rect.height
            # obj.rect.topleft = obj.position
