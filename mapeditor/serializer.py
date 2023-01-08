import struct
import numpy as np
from pygame import Vector2 as v2

from mapeditor import config
import assets
from grid import Grid
from assets import MAP_DIR
from palette import Palette, Rect
from elements import EmptyElement, StateElement

class Serializer:
    def serialize(grid: Grid, palette: Palette, file: str = "default_0000.map") -> None:
        """serialize(grid: Grid, palette: Palette, file: str)\n
        Cette fonction sauvegarde dans le fichier `file` le contenu de `grid` lié à `palette`

        Paramètres:
            `grid` (Grid): grille qui représente le contenu du niveau qu'on édite
            `palette` (Palette): tableau de correspondance entre les assets et les ids
            `file` (str, optional): nom du fichier à écrire. Valeur par défaut -> "default_0000.map".
        
        Retourne:
            `None`
        """
        # on ouvre le fichier dans le dossier .../slime_game/assets/maps/
        f = open(f"{MAP_DIR}/{file}", 'wb')

        # on écrit le tableau de concordance en premier

        # d'abord le nommbre d'éléments dans la palette
        f.write(struct.pack("@b", len(palette.elements)))
        
        # ensuite les identifiants des assets
        f.write(struct.pack("@" + "h"*len(palette.elements), *[palette.table[j].id for j in palette.elements.keys()]))

        # écrit la taille en tuile du niveau
        f.write(struct.pack('@bb', grid.rows, grid.columns))

        # écrit la matrice de niveau
        # sous la forme <8b:id><8b:state><16b:uuid>
        elements: list[int] = [props for element in grid.map.flatten() for props in (element.id, element.state, element.uuid)]
        f.write(struct.pack('@' + 'bbh'*grid.rows*grid.columns, *elements))
        
        # ajouter le background
        f.write(struct.pack("@h", grid.background.id))

        f.close()

    def deserialize(file: str = "default_0000.map") -> tuple[Palette, Grid]:
        """deserialize(file: str)\n
        Cette fonction charge dans `grid` et `palette` les éléments dans le `file`

        Paramètres:
            file (str, optional): fichier depuis lequel on lit. Valeur par défaut -> "default_0000.map".

        Retourne:
            tuple[Palette, Grid]: la palette et la grid une fois chargées
        """
        # on ouvre le fichier dans le dossier .../slime_game/assets/maps/
        f = open(f"{MAP_DIR}/{file}", "rb")

        # on récupère en premier les informations de la palette

        # on lit la taille de la palette
        table_length: int  = struct.unpack("@b", f.read(1))[0]

        # construit la liste des assets
        table: list[assets.Asset] = [ assets.ASSETS[global_id] for global_id in list(struct.unpack("@" + "h"*table_length, f.read(2*table_length)))]

        Palette.tile_size: int = config.compute_palette_tile_size(config.WINDOW_W, config.DEFAULT_PALETTE_COLUMNS)
        palette: Palette = Palette(
            Rect(
                config.compute_palette_offset(config.WINDOW_W, config.DEFAULT_PALETTE_COLUMNS*Palette.tile_size),
                0,
                config.DEFAULT_PALETTE_COLUMNS*Palette.tile_size,
                config.DEFAULT_PALETTE_ROWS*Palette.tile_size
            ),
            table
        )

        # on lit ensuite les dimensions de la grille
        (grid_rows, grid_columns) = struct.unpack("@bb", f.read(2))
        data_grid = np.full((grid_rows, grid_columns), EmptyElement)

        for i in range(grid_rows):
            for j in range(grid_columns):
                (id, state, uuid) = struct.unpack("@bbh", f.read(4))
                if id == -1: continue
                data_grid[i, j] = StateElement(id, state, uuid, v2(j*Grid.tile_size, i*Grid.tile_size), palette.elements[id].spritesheet[state])

        # enfin on lit le background de la map
        background_id: int = struct.unpack("@h", f.read(2))[0]

        Grid.tile_size = config.compute_grid_tile_size((config.WINDOW_W, config.WINDOW_H), (grid_rows, grid_columns), palette.rect.width)
        grid: Grid = Grid(Rect(0, 0, grid_columns*Grid.tile_size, grid_rows*Grid.tile_size), assets.ASSETS[background_id], data_grid)

        f.close()

        return (palette, grid)
