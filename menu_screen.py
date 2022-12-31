from pygame import Rect, Color
from pygame import image

from buttons import ButtonManager, Button
from button_script import ButtonScript
from assets import ASSET_DIR
from config import GameConfig

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

    def init(game):
        Menu.__menus = {name:fct(game) for name,fct in {
            "ingame_pause": Menu.__create_ingame_menu,
        }.items()}

    def open_menu(menu: str) -> None:
        ButtonManager.set_alive(*Menu.__menus[menu])
        Menu.__open_menus.add(menu)

    def close_menu(menu: str) -> None:
        ButtonManager.kill(*Menu.__menus[menu])
        if menu in Menu.__open_menus: Menu.__open_menus.remove(menu)

    def is_open(menu: str):
        return menu in Menu.__open_menus

    def __create_menu(menu_rect: Rect, interval_ratio: int, props_buttons: list[dict[str]], ) -> list[str]:
        """_summary_

        Args:
            menu_rect (Rect): _description_
            interval_ratio (int): ratio button/interval
            props_buttons (list[dict[str, Any]]): _description_

        Returns:
            list[str]: _description_
        """
        interval_height = menu_rect.height // ((len(props_buttons)-1)+(interval_ratio*len(props_buttons)))
        button_height = interval_ratio * interval_height
        for k, props in enumerate(props_buttons):
            props["hitbox"] = Rect(menu_rect.left, menu_rect.top + k*(interval_height+button_height) , menu_rect.width, button_height)
        return [Button(**props).id for props in props_buttons]
            
    def __create_ingame_menu(game) -> list[str]:
        texture = image.load(f"{ASSET_DIR}/UI/button1.png")

        left: int = int(0.325*GameConfig.Graphics.WindowWidth)
        width: int = int(0.35*GameConfig.Graphics.WindowWidth)
        top: int = int(0.1 * GameConfig.Graphics.WindowHeight)
        height: int = int(0.8 * GameConfig.Graphics.WindowHeight)
        return Menu.__create_menu(Rect(left,top,width,height), 2, 
        [
            {"id":"menu.ingame.resume",
                "label":"Continuer",
                "script":ButtonScript(print,"NOT IMPLEMENTED"),
                "textures":texture,
                "label_color":Color("red")
            },
            {"id":"menu.ingame.new_game", 
                "label":"Nouvelle Partie",
                "script":ButtonScript(print,"NOT IMPLEMENTED"),
                "textures":texture,
                "label_color":Color("red")
            },
            {"id":"menu.ingame.load_game",
                "label":"Sauvegarder",
                "script":ButtonScript(print,"NOT IMPLEMENTED"),
                "textures":texture,
                "label_color":Color("red")
            },
            {"id":"menu.ingame.quit",
                "label":"Quitter",
                "script":ButtonScript(ButtonScript.set_quit,game),
                "textures":texture,
                "label_color":Color("red")
            }
        ])
