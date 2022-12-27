from pygame import draw
from config import GameConfig

def debug(info: object, y: float = 10, x: float = 10) -> None:
    debug_surf = GameConfig.FONTS["PressStart2P"].render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft = (x, y))
    draw.rect(GameConfig.WINDOW, 'Black', debug_rect)

    GameConfig.WINDOW.blit(debug_surf, debug_rect)
