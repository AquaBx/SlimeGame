from pygame import draw
from config import GameState,GameConfig

def debug(info: object, y: float = 10, x: float = 10) -> None:
    debug_surf = GameConfig.FONTS["PressStart2P"].render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft = (x, y))
    draw.rect(GameState.WINDOW, 'Black', debug_rect)

    GameState.WINDOW.blit(debug_surf, debug_rect)
