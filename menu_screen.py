from pygame import Rect, Color
from pygame import image, mouse

from buttons import ButtonManager, Button
from button_script import ButtonScript
from assets import UI_DIR
from config import GameConfig

from eventlistener import EventManager
from customevents import TitleScreenEvent, MenuEvent

class Menu :
    """
    Cette classe permet d'afficher deux menus : le menu principal hors-partie et le menu en jeu

    Le menu principal contient :
    Une image de fond
    Un rectangle par option de menu
    Dans chaque rectangle, on affiche une option
    """
    __menus: dict = dict()
    __open_menus: set[str] = set()

    def init():
        Menu.__menus = { name: fct() for name, fct in {
            "ingame_pause": Menu.__create_ingame_menu,
            "title_screen": Menu.__create_title_screen
        }.items()}

    def open_menu(menu: str) -> None:
        ButtonManager.set_alive(*Menu.__menus[menu])
        Menu.__open_menus.add(menu)
        mouse.set_visible(True)

    def close_menu(menu: str) -> None:
        ButtonManager.kill(*Menu.__menus[menu])
        if menu in Menu.__open_menus: Menu.__open_menus.remove(menu)
        mouse.set_visible(Menu.is_open())

    def is_open(menu: str = None) -> bool:
        """Indique si un menu est ouvert.

        Paramètres:
            menu (str, optional): le nom du menu. None par défaut. None => au moins un menu d'ouvert.

        Retourne:
            bool: True si le menu est ouvert, False sinon.
        """
        if menu is None:
            return len(Menu.__open_menus) != 0

        return menu in Menu.__open_menus

    def __create_menu(menu_rect: Rect, interval_ratio: int, *props_buttons: list[dict[str]]) -> list[str]:
        """_summary_

        Args:
            menu_rect (Rect): rectangle that the menu will occup
            interval_ratio (int): ratio button/interval
            props_buttons (list[dict[str, Any]]): data used to build the button instances

        Returns:
            list[str]: list of button ids
        """
        interval_height = menu_rect.height // ((len(props_buttons)-1)+(interval_ratio*len(props_buttons)))
        button_height = interval_ratio * interval_height
        for k, props in enumerate(props_buttons):
            props["hitbox"] = Rect(menu_rect.left, menu_rect.top + k*(interval_height+button_height) , menu_rect.width, button_height)
        return [Button(**props).id for props in props_buttons]

    def __create_ingame_menu() -> list[str]:
        texture = image.load(f"{UI_DIR}/button1.png")
        texture_disabled = image.load(f"{UI_DIR}/button1_disabled.png")

        top: int = int(0.1 * GameConfig.Graphics.WindowHeight)
        left: int = int(0.325*GameConfig.Graphics.WindowWidth)
        width: int = int(0.35*GameConfig.Graphics.WindowWidth)
        height: int = int(0.8 * GameConfig.Graphics.WindowHeight)

        return Menu.__create_menu(Rect(left,top,width,height), 2, {
                "id":          "menu.ingame.resume",
                "label":       "Continuer",
                "script":      ButtonScript(EventManager.push_event, MenuEvent("menu.ingame.resume")),
                "textures":    [texture, texture, texture_disabled],
                "label_color": Color("gray90")
            },
            {
                "id":          "menu.ingame.settings",
                "label":       "Paramètres",
                "script":      ButtonScript(EventManager.push_event, MenuEvent("menu.ingame.settings")),
                "textures":    [texture, texture, texture_disabled],
                "label_color": Color("gray90"),
                "enabled": False
            },
            {
                "id":          "menu.ingame.save_and_quit",
                "label":       "Sauver & Quitter",
                "script":      ButtonScript(EventManager.push_event, MenuEvent("menu.ingame.save_and_quit")),
                "textures":    [texture, texture, texture_disabled],
                "label_color": Color("gray90")
            }
        )

    def __create_title_screen() -> list[str]:
        texture = image.load(f"{UI_DIR}/button1.png")
        texture_disabled = image.load(f"{UI_DIR}/button1_disabled.png")

        top: int = int(0.1 * GameConfig.Graphics.WindowHeight)
        left: int = int(0.325*GameConfig.Graphics.WindowWidth)
        width: int = int(0.35*GameConfig.Graphics.WindowWidth)
        height: int = int(0.8 * GameConfig.Graphics.WindowHeight)
        return Menu.__create_menu(Rect(left, top, width, height), 2, {
                "id": "menu.title.continue",
                "label": "Continuer",
                "script": ButtonScript(EventManager.push_event, TitleScreenEvent("menu.title.continue")),
                "textures": [texture, texture, texture_disabled],
                "label_color": Color("gray90")
            },
            {
                "id": "menu.title.settings",
                "label": "Paramètres",
                "script": ButtonScript(EventManager.push_event, TitleScreenEvent("menu.title.settings")),
                "textures": [texture, texture, texture_disabled],
                "label_color": Color("gray90"),
                "enabled": False
            },
            {
                "id": "menu.title.quit",
                "label": "Quitter",
                "script": ButtonScript(EventManager.push_event, TitleScreenEvent("menu.title.quit")),
                "textures": [texture, texture, texture_disabled],
                "label_color": Color("gray90")
            }
        )
