import struct
from assets import ASSETS
from assets.palette import Palette
import numpy as np

import pygame as pg
from pygame import transform, image,Vector2 as v2

from config import GameConfig
from assets.scripts.environment import MapElement

def deserialize(world, file: str) -> tuple[np.ndarray[(None, MapElement)], pg.Surface]:
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
        environment: pg.Surface = pg.Surface(v2(grid_columns, grid_rows)*GameConfig.BLOCK_SIZE, flags=pg.SRCALPHA).convert_alpha()
        blocks = np.full((grid_rows, grid_columns), None)
        for i in range(grid_rows):
            for j in range(grid_columns):
                (id, state, uuid) = struct.unpack("@bbh", f.read(4))

                if id == -1: continue
                blocks[i, j] = table[id].script.create((i, j), id, state, uuid)
                environment.blit(blocks[i, j].texture, blocks[i, j].position)

        # enfin on lit le background de la map
        background_id: int = struct.unpack("@h", f.read(2))[0]

        background: pg.Surface = transform.scale(image.load(ASSETS[background_id].path).convert(), environment.get_size())
        background.blit(environment, (0,0))
        f.close()
        return (blocks, background)