from pygame import Rect, Color, Surface
from pygame import image, transform, mouse

from buttons import ButtonManager, Button
from button_script import ButtonScript
from config import GameConfig, GameState
from assets import SPRITE_DIR

from eventlistener import EventManager
from customevents import TitleScreenEvent, MenuEvent

class Menu:
    def __init__(self, buttons: list[str], buttons_rect: Rect, menu_rect: Rect, background: Surface) -> None:
        self.buttons: list[str] = buttons
        self.buttons_rect: Rect = buttons_rect
        self.menu_rect: Rect = menu_rect
        self.background: Surface = background

class MenuManager :
    """
    Cette classe permet d'afficher deux menus : le menu principal hors-partie et le menu en jeu

    Le menu principal contient :
    Une image de fond
    Un rectangle par option de menu
    Dans chaque rectangle, on affiche une option
    """

    window: Surface
    __menus: dict[str, Menu] = dict()
    __open_menus: set[str] = set()

    def init(window: Surface):
        MenuManager.window = window

        MenuManager.__menus = { name: fct() for name, fct in {
            "ingame_pause": MenuManager.__create_ingame_menu,
            "title_screen": MenuManager.__create_title_screen
        }.items()}

    def open_menu(menu: str) -> None:
        ButtonManager.set_alive(*MenuManager.__menus[menu].buttons)
        MenuManager.__open_menus.add(menu)
        GameState.paused = True
        mouse.set_visible(True)

    # TODO default value to str -> close all
    def close_menu(menu: str) -> None:
        ButtonManager.kill(*MenuManager.__menus[menu].buttons)
        if menu in MenuManager.__open_menus: MenuManager.__open_menus.remove(menu)
        GameState.paused = MenuManager.is_open()
        mouse.set_visible(MenuManager.is_open())

    def is_open(menu: str = None) -> bool:
        """Indique si un menu est ouvert.

        Paramètres:
            menu (str, optional): le nom du menu. None par défaut. None => au moins un menu d'ouvert.

        Retourne:
            bool: True si le menu est ouvert, False sinon.
        """
        if menu is None:
            return len(MenuManager.__open_menus) != 0

        return menu in MenuManager.__open_menus

    def __create_menu(buttons_rect: Rect, interval_ratio: int, menu_rect: Rect, background_path: str, *props_buttons: list[dict[str]]) -> Menu:
        """_summary_

        Args:
            menu_rect (Rect): rectangle that the menu will occup
            interval_ratio (int): ratio button/interval
            props_buttons (list[dict[str, Any]]): data used to build the button instances

        Returns:
            list[str]: list of button ids
        """
        interval_height = buttons_rect.height // ((len(props_buttons)-1)+(interval_ratio*len(props_buttons)))
        button_height = interval_ratio * interval_height
        
        for k, props in enumerate(props_buttons):
            props["hitbox"] = Rect(buttons_rect.left, buttons_rect.top + k*(interval_height+button_height) , buttons_rect.width, button_height)
        
        buttons = [Button(**props).id for props in props_buttons]
        background = transform.scale(image.load(background_path),menu_rect.size)
        menu = Menu(buttons, buttons_rect, menu_rect, background)
        return menu

    def __create_ingame_menu() -> Menu:
        left_m = int(0.3 * GameConfig.gameGraphics.WindowWidth)
        top_m = int(0.05 * GameConfig.gameGraphics.WindowHeight)
        width_m =  int(0.4 * GameConfig.gameGraphics.WindowWidth)
        height_m = int(0.9 * GameConfig.gameGraphics.WindowHeight)

        left_b: int = int(0.325*GameConfig.gameGraphics.WindowWidth)
        top_b: int = int(0.1 * GameConfig.gameGraphics.WindowHeight)
        width_b: int = int(0.35*GameConfig.gameGraphics.WindowWidth)
        height_b: int = int(0.8 * GameConfig.gameGraphics.WindowHeight)

        return MenuManager.__create_menu(Rect(left_b,top_b,width_b,height_b), 2, Rect(left_m, top_m, width_m, height_m), f"{SPRITE_DIR}/backgrounds/ingame_background.png", {
                "id":          "menu.ingame.resume",
                "label":       "Continuer",
                "script":      ButtonScript(EventManager.push_event, MenuEvent("menu.ingame.resume")),
                "label_color": Color("gray90")
            },
            {
                "id":          "menu.ingame.settings",
                "label":       f"RTX {'on' if GameConfig.Graphics.EnableLights else 'off'}",
                "script":      ButtonScript(EventManager.push_event, MenuEvent("menu.ingame.settings")),
                "label_color": Color("gray90")
            },
            {
                "id":          "menu.ingame.save_and_quit",
                "label":       "Sauver & Quitter",
                "script":      ButtonScript(EventManager.push_event, MenuEvent("menu.ingame.save_and_quit")),
                "label_color": Color("gray90")
            })

    def __create_title_screen() -> Menu:     
        top_b: int = int(0.4 * GameConfig.gameGraphics.WindowHeight)
        left_b: int = int(0.325*GameConfig.gameGraphics.WindowWidth)
        width_b: int = int(0.35*GameConfig.gameGraphics.WindowWidth)
        height_b: int = int(0.5 * GameConfig.gameGraphics.WindowHeight)
        return MenuManager.__create_menu(Rect(left_b, top_b, width_b, height_b), 2, Rect((0,0),GameConfig.gameGraphics.WindowSize), f"{SPRITE_DIR}/backgrounds/title_screen_menu.png", 
            {
                "id": "menu.title.continue",
                "label": "Continuer",
                "script": ButtonScript(EventManager.push_event, TitleScreenEvent("menu.title.continue")),
                "label_color": Color("gray90")
            },
            {
                "id":           "menu.title.reset",
                "label":        "Recommencer",
                "script":       ButtonScript(EventManager.push_event, TitleScreenEvent("menu.title.reset")), 
                "label_color":  Color("gray90")
            },
            {
                "id":           "menu.title.settings",
                "label":        "Paramètres",
                "script":       ButtonScript(EventManager.push_event, TitleScreenEvent("menu.title.settings")), 
                "label_color":  Color("gray50"),
                "enabled": False
            },
            {
                "id": "menu.title.quit",
                "label": "Quitter",
                "script": ButtonScript(EventManager.push_event, TitleScreenEvent("menu.title.quit")),
                "label_color": Color("gray90")
            }
        )

    def draw_menus() -> None:
        opens = list(MenuManager.__open_menus)
        for menu_id in opens:
            menu = MenuManager.__menus[menu_id]
            MenuManager.window.blit(menu.background, menu.menu_rect.topleft)