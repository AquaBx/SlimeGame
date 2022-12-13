import pygame as pg
from pygame import transform, image
from pygame import Vector2 as v2

from config import GameConfig,GameState

import numpy as np
import struct

import assets.gpalette as gpalette
from assets.gpalette import ASSETS, Palette
from assets.scripts.gameobject import GameObject, Player,Empty,Ground

from camera import Camera

from debug import debug

class World():
    palette: Palette
    Palette: list = []
    DEFAULT_SURFACE: pg.Surface = pg.Surface((0, 0))

    def __init__(self, map: str) -> None:
        self.background = transform.scale( image.load("assets/sprites/background/background.png"), (GameConfig.WINDOW_SIZE.x, GameConfig.WINDOW_SIZE.y) )
        self.current_map = map
        self.load()

        self.player = Player(v2(1,1), v2(GameConfig.BLOCK_SIZE,GameConfig.BLOCK_SIZE), [f"assets/sprites/Dynamics/GreenSlime/Grn_Idle{i}.png" for i in range(1,11)])
        self.camera: Camera = Camera(self.player)

    def load(self):
        f = open(f"assets/maps/{self.current_map}.map", "rb")
        map_dim: tuple[int, int] = struct.unpack("@bb", f.read(2))

        data: np.ndarray = np.full(map_dim, None)
        self.blocks: np.ndarray[GameObject] = np.full(map_dim, None)
        for i in range(map_dim[0]):
            for j in range(map_dim[1]):
                data[i, j] = struct.unpack("@bbh", f.read(4))

        table_size: int = struct.unpack("@b", f.read(1))[0]
        table: dict[int, int] = {}
        for _ in range(table_size):
            local_id, global_id = struct.unpack("@bh", f.read(4))
            table[local_id] = ASSETS[global_id]
        World.palette = Palette(table)

        for i in range(map_dim[0]):
            for j in range(map_dim[1]):
                local_id, state, uuid = data[i, j]
                if local_id == -1:
                    self.blocks[i, j] = Empty(0,v2(j, i),v2(GameConfig.BLOCK_SIZE,GameConfig.BLOCK_SIZE))
                    continue
                script = gpalette.ASSETS[table[local_id].id].script
                texture = World.palette.get_texture(local_id, state)
                self.blocks[i, j] = script(state, v2(j, i),v2(GameConfig.BLOCK_SIZE, GameConfig.BLOCK_SIZE), texture)

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

    def collide(self,obj):
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
            if blocks_arround[key]["ref"].state != 0:
                obj2 = blocks_arround[key]["ref"]
                offset: v2 = obj2.position - obj.position
                collide = obj.mask.overlap(obj2.mask, offset)
                blocks_arround[key]["collide"] = True if collide else False
            else:
                blocks_arround[key]["collide"] = False
        
        return blocks_arround

    def update_pos(self,obj:GameObject) -> None:
        
        pos_avant = v2(obj.position.x,obj.position.y)

        obj.acceleration.x = -obj.vitesse.x * 1000 / GameConfig.BLOCK_SIZE

        obj.update()

        obj.vitesse.x += obj.acceleration.x * GameState.dt
        obj.position.x += obj.vitesse.x * GameState.dt

        obj.vitesse.y += obj.acceleration.y * GameState.dt
        obj.position.y += obj.vitesse.y * GameState.dt

        self.gravite(obj)
       
        blocks_collide = self.collide(obj)
        debug((blocks_collide["top-left"],blocks_collide["top-left"]["ref"].mask))
        dir = obj.position - pos_avant

        if dir.y < 0 and ( blocks_collide["top-left"]["collide"] or blocks_collide["top-right"]["collide"] ):
            obj.position.y = blocks_collide["top-left"]["ref"].rect.bottom
            obj.vitesse.y = 0
            obj.acceleration.y = 0
        elif dir.y > 0 and ( blocks_collide["bottom-right"]["collide"] or blocks_collide["bottom-left"]["collide"] ):
            obj.position.y = blocks_collide["bottom-left"]["ref"].rect.top - obj.taille.y
            obj.vitesse.y = 0
            obj.acceleration.y = 0

        blocks_collide = self.collide(obj) # on actualise les collisions pour avoir une meilleur gestion de l'axe x

        if dir.x < 0 and ( blocks_collide["top-left"]["collide"] or blocks_collide["bottom-left"]["collide"] ):
            obj.position.x = blocks_collide["top-left"]["ref"].rect.right
            obj.vitesse.x = 0
            obj.acceleration.x = 0
        elif dir.x > 0 and ( blocks_collide["top-right"]["collide"] or blocks_collide["bottom-right"]["collide"] ):
            obj.position.x = blocks_collide["top-right"]["ref"].rect.left - obj.taille.x
            obj.vitesse.x = 0
            obj.acceleration.x = 0
