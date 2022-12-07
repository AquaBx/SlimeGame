from config import GameConfig
from gameobject import Ground,Player
import pygame
import numpy as np

class World():
    def __init__(self):
        self.background = pygame.transform.scale( pygame.image.load("Assets/Sprites/Background/background.png"), (GameConfig.WINDOW_SIZE.x, GameConfig.WINDOW_SIZE.y) )

        self.blocks = np.array( [ [ Ground(True,pygame.Vector2(i*GameConfig.BLOCK_SIZE,j*GameConfig.BLOCK_SIZE), 'Assets/Sprites/Statics/ground.png') for i in range(3) ] for j in range(3) ]  )
        
        self.player = Player(0, 0, GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE, [f'Assets/Sprites/Dynamics/GreenSlime/Grn_Idle{i}.png' for i in range(1,11)])

    def update(self,camera):

        self.player.update_frame()
        self.player.update()
        # World.gravite(player,dt)
        self.player.draw(camera)
        
        for j in range( max(0, int(camera.rect.left / GameConfig.BLOCK_SIZE) ) , min( len(self.blocks[0]) , int(camera.rect.right / GameConfig.BLOCK_SIZE ) + 1 ) ):
            for i in range( max(0, int(camera.rect.top / GameConfig.BLOCK_SIZE) ) , min( len(self.blocks) ,  int(camera.rect.bottom / GameConfig.BLOCK_SIZE) + 1 ) ):
                self.blocks[i][j].draw( camera )

    def collision_mask(self, obj1, obj_arr):
        """
            le side est relative au deuxieme block
        """
        for obj2 in obj_arr:
            mask1 = obj1
            mask2 = obj2

            collide = pygame.sprite.collide_mask(mask1,mask2)
            if collide!=None:
                return True , obj2.rect.top
        return False,-1
    
    def gravite(self,obj,dt):
        y_vect = 50 * GameConfig.BLOCK_SIZE

        gravite = pygame.Vector2(0, y_vect)
        # resistance = pygame.Vector2(0, 0)

        obj.acceleration.y = gravite[1] # + resistance[1]
        obj.vitesse.y += obj.acceleration.y*dt     
        obj.position.y += obj.vitesse.y * dt

        obj.rect.topleft = obj.position

        collide, ny = self.collision_mask(obj, self.blocks)

        if collide :
            # resistance = pygame.Vector2(0, -y_vect)
            h = 5 * GameConfig.BLOCK_SIZE
            obj.acceleration.y = -( 2 * gravite.y * h)**0.5/dt * int(pygame.key.get_pressed()[pygame.K_z])
            obj.vitesse.y = obj.acceleration.y*dt
            obj.position.y = ny + obj.vitesse.y*dt - obj.rect.height
            obj.rect.topleft = obj.position