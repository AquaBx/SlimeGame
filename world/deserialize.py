import struct
from assets import ASSETS
from assets.palette import Palette
import numpy as np
from pygame import Vector2 as v2
import pygame as pg
from pygame import transform, image,Surface

from config import GameConfig

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
        environment: pg.Surface = pg.Surface(v2(grid_columns, grid_rows)*GameConfig.BLOCK_SIZE)
        self.blocks = np.full((grid_rows, grid_columns), None)
        for i in range(grid_rows):
            for j in range(grid_columns):
                (id, state, uuid) = struct.unpack("@bbh", f.read(4))

                if id == -1: continue
                self.blocks[i, j] = table[id].script.create((i, j), id, state, uuid)
                environment.blit(self.blocks[i, j].texture, self.blocks[i, j].position)

        # enfin on lit le background de la map
        background_id: int = struct.unpack("@h", f.read(2))[0]

        self.background: pg.Surface = transform.scale(image.load(ASSETS[background_id].path).convert(), environment.get_size())
        self.background.blit(environment, (0,0))
        f.close()