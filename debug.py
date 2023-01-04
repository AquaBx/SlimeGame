from pygame import draw
from config import GameState

def debug(info: object, y: float = 10, x: float = 10) -> None:
    debug_surf = GameState.DEFAULT_FONT.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft = (x, y))
    draw.rect(GameState.WINDOW, 'Black', debug_rect)

    GameState.WINDOW.blit(debug_surf, debug_rect)
