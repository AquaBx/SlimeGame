from pygame import Surface, Rect, Vector2 as v2
import pygame as pg

class SpritesheetManager:

    SlimeAnimations: dict[dict[str, list[Surface]]] = {}

    def load_frame(spritesheet: Surface, current_frame: int, animation_index: int, tile_size: int, size: v2, flip: bool) -> Surface:
        return pg.transform.flip(pg.transform.scale(spritesheet.subsurface(Rect(current_frame*tile_size,animation_index*tile_size,tile_size,tile_size)), size), flip, False)

    def generate_spritesheets(size: v2, spritesheets: dict[str,tuple[str,int]], animations: list[tuple[str, int]]) -> dict[dict[str, list[Surface]]]:
        sheets = {}
        for sheet_name, (path,tile_size) in spritesheets.items():
            spritesheet = pg.image.load(path)
            
            anims: dict[str, list[Surface]] = {}

            for animation_index, (anim_name, frame_count) in enumerate(animations):
                for direction in ["right", "left"]:
                    animation: list[Surface] = []
                    for frame_index in range(frame_count):
                        animation.append(SpritesheetManager.load_frame(spritesheet, frame_index, animation_index, tile_size, size, direction=="left"))
                    anims[f"{anim_name}-{direction}"] = animation

            sheets[sheet_name] = anims
        return sheets

    def initialize() -> None:
        SpritesheetManager.SlimeAnimations = SpritesheetManager.generate_spritesheets(
           size = v2(18),
           spritesheets={
            "green" :("assets/sprites/dynamics/green_slime_spritesheet.png",  18),
            "orange":("assets/sprites/dynamics/orange_slime_spritesheet.png", 18),
            "red"   :("assets/sprites/dynamics/red_slime_spritesheet.png",    18),
            "ghost" :("assets/sprites/dynamics/ghost_slime_spritesheet.png",  18),
           },
           animations=[
            ("idle",  10),
            ("jump",  10),
            ("walk",  5),
            ("hurt",  4),
            ("death", 3)
           ]
        )
