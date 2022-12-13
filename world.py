import pygame as pg
from pygame import transform, image, sprite
from pygame import Vector2 as v2

from config import GameConfig

from pygame import Vector2 as v2
from pygame import transform, image
import numpy as np
import struct

import assets.gpalette as gpalette
from assets.gpalette import ASSETS, Palette
from assets.scripts.gameobject import GameObject, Player, Static

from camera import Camera

class World():
    palette: Palette
    Palette: list = []
    DEFAULT_SURFACE: pg.Surface = pg.Surface((0, 0))

    def __init__(self, map: str) -> None:
        self.background = transform.scale( image.load("assets/sprites/background/background.png"), (GameConfig.WINDOW_SIZE.x, GameConfig.WINDOW_SIZE.y) )
        self.current_map = map
        self.load()
        self.player = Player(15, v2(0, 0), [f"assets/sprites/Dynamics/GreenSlime/Grn_Idle{i}.png" for i in range(1,11)])
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
                    self.blocks[i, j] = Static(0, v2(j*GameConfig.BLOCK_SIZE, i*GameConfig.BLOCK_SIZE), World.DEFAULT_SURFACE)
                    continue
                script = gpalette.ASSETS[table[local_id].id].script
                texture = World.palette.get_texture(local_id, state)
                self.blocks[i, j] = script(state, v2(j*GameConfig.BLOCK_SIZE, i*GameConfig.BLOCK_SIZE), texture)

    def update(self) -> None:
        self.camera.update()
        self.player.update_frame()
        self.player.update()
        self.gravite()

    def draw(self) -> None:
        for j in range( max(0, int(self.camera.rect.left / GameConfig.BLOCK_SIZE) ) , min( len(self.blocks[0]) , int(self.camera.rect.right / GameConfig.BLOCK_SIZE ) + 1 ) ):
            for i in range( max(0, int(self.camera.rect.top / GameConfig.BLOCK_SIZE) ) , min( len(self.blocks) ,  int(self.camera.rect.bottom / GameConfig.BLOCK_SIZE) + 1 ) ):
                self.blocks[i, j].draw(self.camera)

        self.player.draw(self.camera)

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
