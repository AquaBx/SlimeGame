from config import Config
from block import Block
from entity import Entity
import pygame
import debug
class World():
    def __init__(self):
        self.blocks = [Block(Config.BLOCK_SIZE * i, Config.WINDOW_H - Config.BLOCK_SIZE,
                                Config.BLOCK_SIZE, Config.BLOCK_SIZE, True,
                                f'Assets/Tileset/tileMain{2}.png') for i in range(1, 20)]
        self.blocks += [Block(Config.BLOCK_SIZE * (i-10), Config.WINDOW_H + 5*Config.BLOCK_SIZE,
                                Config.BLOCK_SIZE, Config.BLOCK_SIZE, True,
                                f'Assets/Tileset/tileMain{2}.png') for i in range(1, 20)]
        
        self.player = Entity(Config.BLOCK_SIZE,
                        Config.WINDOW_H - 2 * Config.BLOCK_SIZE,
                        Config.BLOCK_SIZE, Config.BLOCK_SIZE,
                        "Assets/GreenSlime/Grn_Idle1.png")

    def collision_mask(self, obj1, obj_arr):
        """
            le side est relative au deuxieme block
        """
        lis_out = []
        for obj2 in obj_arr:
            mask1 = obj1
            mask2 = obj2

            collide = pygame.sprite.collide_mask(mask1,mask2)
            if collide!=None:
                print(collide,obj2.rect.top)
                return True , obj2.rect.top
        return False,-1
    
    def gravite(self,obj,dt):
        debug.debug(obj.vitesse.y)

        y_vect = 10 * Config.BLOCK_SIZE

        gravite = pygame.Vector2(0, y_vect)
        # resistance = pygame.Vector2(0, 0)

        obj.acceleration.y = gravite[1] # + resistance[1]
        obj.vitesse.y += obj.acceleration.y*dt     
        obj.position.y += obj.vitesse.y * dt

        obj.rect.topleft = obj.position

        collide, ny = self.collision_mask(obj, self.blocks)
        print(collide)
        if collide :
            # resistance = pygame.Vector2(0, -y_vect)
            h = 2 * Config.BLOCK_SIZE
            obj.acceleration.y = -( 2 * gravite.y * h)**0.5/dt * int(pygame.key.get_pressed()[pygame.K_z])
            obj.vitesse.y = obj.acceleration.y*dt
            obj.position.y = ny + obj.vitesse.y*dt - obj.rect.height
            obj.rect.topleft = obj.position