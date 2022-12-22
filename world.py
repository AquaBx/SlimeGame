import pygame as pg
from pygame import transform, image
from pygame import Vector2 as v2

from config import GameConfig, GameState

import numpy as np
import struct

from assets import ASSETS
import assets.saves
from assets.palette import Palette
from assets.scripts.gameobject import GameObject, Player, EmptyElement

from camera import Camera

class World():

    def __init__(self, savestate: int) -> None:
        self.savestate: int = savestate
        self.save: dict = assets.saves.load(savestate)
        if self.save["occupied"]:
            self.deserialize(self.save["last_map"])
            self.player = Player(v2(1, 1), 0.95*GameConfig.BLOCK_SIZE*v2(1, 1), [f"assets/sprites/Dynamics/GreenSlime/Grn_Idle{i}.png" for i in range(1,11)])
            self.camera: Camera = Camera(self.player)
        else:
            self.save = {
                "occupied": True,
                "last_map": "stage1",
                "player": {
                    "position": (1, 1)
                }
            }
            self.deserialize("stage1")
            self.player = Player(v2(5, 60), 0.95*GameConfig.BLOCK_SIZE*v2(1, 1), [f"assets/sprites/Dynamics/GreenSlime/Grn_Idle{i}.png" for i in range(1,11)])
            self.camera = Camera(self.player)

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
                if id == -1: continue
                self.blocks[i, j] = table[id].script.create((i, j), id, state, uuid)
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
        for j in range( max(0, int(self.camera.rect.left / GameConfig.BLOCK_SIZE) ) , min( len(self.blocks[0]) , int(self.camera.rect.right / GameConfig.BLOCK_SIZE ) + 1 ) ):
            for i in range( max(0, int(self.camera.rect.top / GameConfig.BLOCK_SIZE) ) , min( len(self.blocks) ,  int(self.camera.rect.bottom / GameConfig.BLOCK_SIZE) + 1 ) ):
                self.blocks[i, j].draw(self.camera)
                
        link = self.camera.link
        link.draw(self.camera)
        link.sante -= 0.0001
        health_percent = link.sante/link.santemax * GameConfig.BLOCK_SIZE*5
        pg.draw.rect(GameConfig.WINDOW,"red",pg.Rect(GameConfig.BLOCK_SIZE/2,GameConfig.WINDOW_SIZE.y-GameConfig.BLOCK_SIZE,GameConfig.BLOCK_SIZE*5,GameConfig.BLOCK_SIZE/2))
        pg.draw.rect(GameConfig.WINDOW,"green",pg.Rect(GameConfig.BLOCK_SIZE/2,GameConfig.WINDOW_SIZE.y-GameConfig.BLOCK_SIZE,health_percent,GameConfig.BLOCK_SIZE/2))

    def gravite(self,obj):
        y_vect = 5 * GameConfig.BLOCK_SIZE
        gravite = v2(0, y_vect)
        obj.acceleration.y = gravite[1] # + resistance[1]
        obj.vitesse.y += self.player.acceleration.y*GameState.dt
        obj.position.y += self.player.vitesse.y*GameState.dt

    def collide(self,obj):
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
            if blocks_arround[key]["ref"] != EmptyElement:
                obj2 = blocks_arround[key]["ref"]
                offset: v2 = obj2.position - obj.position
                collide = obj.mask.overlap(obj2.mask, offset)
                blocks_arround[key]["collide"] = True if collide else False
            else:
                blocks_arround[key]["collide"] = False
        
        return blocks_arround

    def is_flying(self,obj:GameObject) -> None:
        BL = obj.position_matrix_bottom_left
        BR = obj.position_matrix_bottom_right

        i1, j1 = int(BL.y), int(BL.x)
        i2, j2 = int(BR.y), int(BR.x)

        if BL.x == float(j1):
            # j1 += 1
            pass

        if BR.x == float(j2):
            j2 -= 1

        if self.blocks[i1,j1] == EmptyElement and self.blocks[i2,j2] == EmptyElement:
            return True,None
        return False,self.blocks[i2,j2].position.y

    def update_pos(self,obj:GameObject) -> None:
        
        pos_avant = v2(obj.position.x,obj.position.y)

        obj.acceleration.x = -obj.vitesse.x * 1000 / GameConfig.BLOCK_SIZE

        obj.update()

        blocks_collide = self.collide(obj)

        obj.vitesse.x += obj.acceleration.x * GameState.dt
        obj.position.x += obj.vitesse.x * GameState.dt
 
        blocks_collide = self.collide(obj) # on actualise les collisions pour avoir une meilleur gestion de l'axe x
        
        dir = obj.position - pos_avant

        if dir.x < 0 and ( blocks_collide[0]["collide"] or blocks_collide[3]["collide"] or blocks_collide[6]["collide"] ):
            obj.position.x = blocks_collide[0]["ref"].rect.right
            obj.vitesse.x = 0
            obj.acceleration.x = 0
        elif dir.x > 0 and ( blocks_collide[2]["collide"] or blocks_collide[5]["collide"] or blocks_collide[8]["collide"] ):
            obj.position.x = blocks_collide[2]["ref"].rect.left - obj.taille.x
            obj.vitesse.x = 0
            obj.acceleration.x = 0

        is_flying,max_y = self.is_flying(obj)
        if is_flying:
            obj.acceleration.y = max(0, 0.3 * GameConfig.BLOCK_SIZE / GameState.dt)
            obj.vitesse.y += obj.acceleration.y * GameState.dt
            obj.position.y += obj.vitesse.y * GameState.dt
        else:
            obj.acceleration.y = min(0, 0.3 * GameConfig.BLOCK_SIZE * obj.acceleration.y)
            obj.vitesse.y = obj.acceleration.y * GameState.dt
            obj.position.y = min(max_y-obj.taille.y, obj.position.y + obj.vitesse.y * GameState.dt )

        dir = obj.position - pos_avant

        blocks_collide = self.collide(obj)

        if dir.y < 0 and ( blocks_collide[0]["collide"] or blocks_collide[1]["collide"] or blocks_collide[2]["collide"] ):
            obj.position.y = blocks_collide[0]["ref"].rect.bottom
            obj.vitesse.y = 0
            obj.acceleration.y = 0
        elif dir.y > 0 and ( blocks_collide[6]["collide"] or blocks_collide[7]["collide"] or blocks_collide[8]["collide"] ):
            obj.position.y = blocks_collide[6]["ref"].rect.top - obj.taille.y
            obj.vitesse.y = 0
            obj.acceleration.y = 0