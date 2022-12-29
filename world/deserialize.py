import struct
import assets.saves
from assets import ASSETS
from assets.palette import Palette
from assets.scripts.gameobject import GameObject, Dynamic, Player, EmptyElement
import numpy as np

from pygame import transform, image

from config import GameState

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

    # enfin on lit le background de la map
    background_id: int = struct.unpack("@h", f.read(2))[0]

    self.background: pg.Surface = transform.scale(image.load(ASSETS[background_id].path).convert(), GameState.WINDOW.get_size())
    f.close()