from pygame import Rect, Surface, Vector2 as v2
from pygame import transform, image
from pygame import Color

from input import Input
from button_script import ButtonScript
from text import Text
from assets import UI_DIR
from sounds import Sounds

class Button:

    IDLE: int  = 0
    HOVER: int    = 1
    DISABLED: int = 2
    
    DEFAULT_TEXTURES: list[Surface] = []
    # ne plus init les boutons comme ca, creer un ButtonManager.create qui retourne la ref du bouton
    def __init__(self, id: str, label: str, hitbox: Rect, script: ButtonScript, textures: Surface | list[Surface] = None, alive : bool = False, enabled : bool = True, font: str = "PressStart2P", label_color: Color = Color("white")) -> None:
        self.__id = id
        self.__label = label
        self.__hitbox = hitbox
        self.__script = script
        self.__state = 2*(not(enabled))
        self.__font = font
        self.__label_color = label_color

        # Default, Hover, Disabled
        if textures is None:
            # load default textures if needed
            if Button.DEFAULT_TEXTURES == []: 
                Button.DEFAULT_TEXTURES = [image.load(f"{UI_DIR}/button_{state}.png") for state in ["idle", "hover", "disabled"]]
            textures = Button.DEFAULT_TEXTURES 
        if isinstance(textures, Surface):
            self.__textures = [transform.scale(textures, hitbox.size)] * 3
        else: self.__textures = [transform.scale(texture, hitbox.size) for texture in textures]

        ButtonManager.register_buttons(self)
        if alive: ButtonManager.set_alive(id)

    def __del__(self):
        ButtonManager.unregister_buttons(self.__id)

    def draw(self, window: Surface) -> None:
        window.blit(self.__textures[self.__state], self.__hitbox)
        Text.display_message(self.__label, v2(self.__hitbox.center), self.__font, self.__label_color, True)

    def run(self):
        Sounds.play_audio("button")
        self.__script()

    @property
    def id(self) -> str:
        return self.__id

    @property
    def label(self) -> str:
        return self.__label

    @label.setter
    def label(self, value: str) -> None:
        self.__label = value

    @property
    def hitbox(self) -> Rect:
        return self.__hitbox

    @property
    def state(self) -> int:
        return self.__state

    @state.setter
    def state(self, value: int) -> None:
        self.__state = value

    @property
    def font(self) -> str:
        return self.__font

    @font.setter
    def font(self, value: str) -> None:
        self.__font = value

    @property
    def label_color(self) -> Color:
        return self.__label_color
    
    @label_color.setter
    def label_color(self, value: Color) -> None:
        self.__label_color = value

class ButtonManager():

    # Set of Buttons that are currently rendered
    __alives: set[str] = set()
    # List of ALL Buttons
    __buttons: dict[str, Button] = dict()

    __window: Surface

    is_init: bool = False

    

    def init(window: Surface) -> None:
        if not Input.is_init:
            Input.init()

        ButtonManager.__window = window

        ButtonManager.is_init = True

    def register_buttons(*buttons: list[Button]) -> None:
        for button in buttons:
            ButtonManager.__buttons[button.id] = button

    def unregister_buttons(*ids : list[str]) -> None:
        for id in ids:
            ButtonManager.kill(id)
            ButtonManager.__buttons.pop(id, None)

    def kill(*ids : list[str]) -> None:
        for id in [_id for _id in ids if ButtonManager.is_alive(_id)]:
            ButtonManager.__alives.remove(id)

    def set_alive(*ids : list[str]) -> None:
        for id in [_id for _id in ids if _id in ButtonManager.__buttons.keys()]:
            ButtonManager.__alives.add(id)

    def is_alive(id: str) -> bool:
        return id in ButtonManager.__alives

    def rename_menu(id: str, new_label: str) -> None:
        if id in ButtonManager.__buttons:
            ButtonManager.__buttons[id].label = new_label

    def __handle_motion(button: Button, mouse: v2) -> None:
        if button.hitbox.collidepoint(mouse):
            if button.state == Button.IDLE:
                button.state = Button.HOVER
                # print(f"hovering button {button.id}")
        elif button.state == Button.HOVER: 
            button.state = Button.IDLE
            # print(f"unhovering button {button.id}")

    def __handle_click(button: Button) -> None:
        if button.state == Button.HOVER:
            button.run()
            # print(f"clicking button {button.id}")

    # optimisable ?
    def __update_states():
        motion = Input.get_motion() != v2(0.0)
        click = Input.is_clicked_once()
        for id in ButtonManager.__alives:
            button = ButtonManager.__buttons[id]
            if button.state == Button.DISABLED: 
                continue
            if motion:
                ButtonManager.__handle_motion(button, Input.get_mouse())
            if click:
                ButtonManager.__handle_click(button)
                
    def __draw():
        for id in ButtonManager.__alives:
            ButtonManager.__buttons[id].draw(ButtonManager.__window)

    def update():
        ButtonManager.__update_states()
        ButtonManager.__draw()
