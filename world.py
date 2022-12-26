import pygame as pg
from pygame import transform, image
from pygame import Rect, Vector2 as v2
from pygame.mask import Mask

from config import GameConfig, GameState

import numpy as np
import struct

from assets import ASSETS
import assets.saves
from assets.palette import Palette
from assets.scripts.gameobject import GameObject, Dynamic, Player, EmptyElement

from camera import Camera
from debug import debug
import shader

class World():

    def __init__(self, savestate: int) -> None:
        self.savestate: int = savestate
        self.save: dict = assets.saves.load(savestate)
        if self.save["occupied"]:
            self.deserialize(self.save["last_map"])
        else:
            self.save = {
                "occupied": True,
                "last_map": "stage1",
                "player": {
                    "position": (1, 1)
                }
            }
            self.deserialize("stage1")
        self.player = Player(v2(3, 2) * GameConfig.BLOCK_SIZE, 1*GameConfig.BLOCK_SIZE*v2(1, 1), [f"assets/sprites/Dynamics/GreenSlime/Grn_Idle{i}.png" for i in range(1,11)])
        self.camera: Camera = Camera(self.player)

    def deserialize(self, file: str) -> None:
        # on ouvre le fichier dans le dossier .../slime_game/assets/maps/
        f = open(f"assets/maps/{file}.map", "rb")

        # on récupère en premier les informations de la palette
        
        # on lit la taille de la palette
        table_length: int  = struct.unpack("@b", f.read(1))[0]
        
        # construit la liste des assets
        table = [ ASSETS[global_id] for global_id in list(struct.unpack("@" + "h"*table_length, f.read(2*table_length)))]
        Palette.load(table)

        # on lit ensuite les dimensions de la grille
        (grid_rows, grid_columns) = struct.unpack("@bb", f.read(2))
        self.blocks = np.full((grid_rows, grid_columns), EmptyElement)

        for i in range(grid_rows):
            for j in range(grid_columns):
                (id, state, uuid) = struct.unpack("@bbh", f.read(4))

                shine = True if id == 3 else False
 
                if id == -1: continue
                self.blocks[i, j] = table[id].script.create((i, j), id, state, uuid,shine)
                # StateElement(id, state, uuid, v2(j*Grid.tile_size, i*Grid.tile_size), palette.elements[id].spritesheet[state])

        # enfin on lit le background de la map
        background_id: int = struct.unpack("@h", f.read(2))[0]
        
        self.background: pg.Surface = transform.scale(image.load(ASSETS[background_id].path), GameConfig.WINDOW_SIZE)
        f.close()

    def update(self) -> None:
        self.camera.update()
        self.player.update_frame()
        self.update_pos(self.player)

    def draw(self) -> None:
        shader.reset()
        
        for j in range( max(0, int(self.camera.rect.left / GameConfig.BLOCK_SIZE) ) , min( len(self.blocks[0]) , int(self.camera.rect.right / GameConfig.BLOCK_SIZE ) + 1 ) ):
            for i in range( max(0, int(self.camera.rect.top / GameConfig.BLOCK_SIZE) ) , min( len(self.blocks) ,  int(self.camera.rect.bottom / GameConfig.BLOCK_SIZE) + 1 ) ):
                self.blocks[i, j].draw(self.camera)
        
                
        link = self.camera.link
        link.draw(self.camera)
        shader.draw()


        link.sante -= 0.0001

        scale = 1/7*GameConfig.WINDOW_SIZE.y/20
        mr_left = GameConfig.WINDOW_SIZE.y/20
        mr_bottom = GameConfig.WINDOW_SIZE.y-2*GameConfig.WINDOW_SIZE.y/20
        

        health_percent = link.sante/link.santemax * 29 * scale
        pg.draw.rect(GameConfig.WINDOW,(255,7,3),pg.Rect(GameConfig.WINDOW_SIZE.y/20+10*scale,mr_bottom+2*scale+1,health_percent,3*scale-1))
        GameConfig.WINDOW.blit(transform.scale(image.load("assets/UI/healthbar.png"), (41*scale, GameConfig.WINDOW_SIZE.y/20)),(GameConfig.WINDOW_SIZE.y/20,mr_bottom))
        

    def gravite(self,obj):
        y_vect = 5 * GameConfig.BLOCK_SIZE
        gravite = v2(0, y_vect)
        obj.acceleration.y = gravite[1] # + resistance[1]
        obj.vitesse.y += self.player.acceleration.y*GameState.dt
        obj.position.y += self.player.vitesse.y*GameState.dt

    def collide(self,obj: Dynamic):
        # we get all 9 blocs based on the centered position of the player (0)
        # | | | | | |
        # | |0|1|2| |
        # | |3|4|5| |
        # | |6|7|8| |
        # | | | | | |
        # for now there is a out of bound exception when we are not on the grid anymore
        jc = int( obj.position_matrix_center.x )
        ic = int( obj.position_matrix_center.y )
        blocks_arround = [
            {"ref":self.blocks[i,j] } for i in range(ic-1,ic+2) for j in range(jc-1,jc+2)
        ]

        for key in range(len(blocks_arround)):
            if blocks_arround[key]["ref"] == EmptyElement:
                blocks_arround[key]["collide"] = False
                blocks_arround[key]["overlap_rect"] = None
            else:
                obj2 = blocks_arround[key]["ref"]
                offset: v2 = obj2.position - obj.position
                collide_mask: Mask = obj.mask.overlap_mask(obj2.mask, offset)
                collide_rect: list[Rect] = collide_mask.connected_component().get_bounding_rects()
                if collide_rect:
                    blocks_arround[key]["collide"] = True
                    blocks_arround[key]["overlap_rect"] = collide_rect[0]
                else:
                    blocks_arround[key]["collide"] = False
                    blocks_arround[key]["overlap_rect"] = None
                
        return blocks_arround

    def is_flying(self,obj:GameObject) -> None:
        BL = obj.position_matrix_bottom_left
        BR = obj.position_matrix_bottom_right

        i1, j1 = int(BL.y), int(BL.x)
        i2, j2 = int(BR.y), int(BR.x)

        if BL.x == float(j1):
            #j1 += 1
            pass
        if BR.x == float(j2):
            j2 -= 1
            pass

        if self.blocks[i1,j1] == EmptyElement and self.blocks[i2,j2] == EmptyElement:
            return True,None
        elif self.blocks[i1,j1] == EmptyElement :
            return False,self.blocks[i2,j2].position.y
        return False,self.blocks[i1,j1].position.y

    def update_pos(self, obj : Dynamic) -> None:
        
        pos_avant = v2(obj.position.x,obj.position.y)

        obj.acceleration.x = 0
        obj.acceleration.y = 0

        # keyboard inputs
        obj.update()

        obj.acceleration.x -= obj.vitesse.x / ( GameState.dt * 12 )
        obj.vitesse.x += obj.acceleration.x * GameState.dt
        obj.position.x += obj.vitesse.x * GameState.dt

        dir = obj.position - pos_avant

        blocks_collide = self.collide(obj) # on actualise les collisions pour avoir une meilleur gestion de l'axe x

        if dir.x < 0 and ( blocks_collide[0]["collide"] or blocks_collide[3]["collide"] or blocks_collide[6]["collide"] ):

            correction = 0

            if blocks_collide[0]["collide"]:
                correction = max(correction,blocks_collide[0]["overlap_rect"].width)
            if blocks_collide[3]["collide"]:
                correction = max(correction,blocks_collide[3]["overlap_rect"].width)
            if blocks_collide[6]["collide"]:
                correction = max(correction,blocks_collide[6]["overlap_rect"].width)

            obj.position.x += 1 * correction
            obj.vitesse.x = 0

        elif dir.x > 0 and ( blocks_collide[2]["collide"] or blocks_collide[5]["collide"] or blocks_collide[8]["collide"] ):

            correction = 0

            if blocks_collide[2]["collide"]:
                correction = max(correction,blocks_collide[2]["overlap_rect"].width)
            if blocks_collide[5]["collide"]:
                correction = max(correction,blocks_collide[5]["overlap_rect"].width)
            if blocks_collide[8]["collide"]:
                correction = max(correction,blocks_collide[8]["overlap_rect"].width)

            obj.position.x += -1 * correction
            obj.vitesse.x = 0
        
        obj.acceleration.x = 0

        # Gravity
        obj.acceleration.y += 15 * 9.81 * GameConfig.BLOCK_SIZE

        obj.vitesse.y += obj.acceleration.y * GameState.dt
        obj.position.y += obj.vitesse.y * GameState.dt

        dir = obj.position - pos_avant

        # /!\ EDGE CASE TO PREVENT CRASHING 
        if not 0 <= obj.position_matrix_center.y <= 63:
            obj.position.y = pos_avant.y
            obj.vitesse.y = 0

        blocks_collide = self.collide(obj)


        if dir.y < 0 and ( blocks_collide[0]["collide"] or blocks_collide[1]["collide"] or blocks_collide[2]["collide"] ):

            correction = 0

            if blocks_collide[0]["collide"]:
                correction = max(correction,blocks_collide[0]["overlap_rect"].height)
            if blocks_collide[1]["collide"]:
                correction = max(correction,blocks_collide[1]["overlap_rect"].height)
            if blocks_collide[2]["collide"]:
                correction = max(correction,blocks_collide[2]["overlap_rect"].height)
            
            obj.position.y += 1 * correction
            obj.vitesse.y = 0

        if dir.y > 0 and ( blocks_collide[6]["collide"] or blocks_collide[7]["collide"] or blocks_collide[8]["collide"] ):
            
            obj.is_flying = False
            
            correction = 0

            if blocks_collide[6]["collide"]:
                correction = max(correction,blocks_collide[6]["overlap_rect"].height)
            if blocks_collide[7]["collide"]:
                correction = max(correction,blocks_collide[7]["overlap_rect"].height)
            if blocks_collide[8]["collide"]:
                correction = max(correction,blocks_collide[8]["overlap_rect"].height)
            
            obj.position.y += -1 * correction
            obj.vitesse.y = 0

        obj.acceleration.y = 0