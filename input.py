from typing import Sequence
from pygame import Vector2 as v2
from pygame import key, mouse

class Input:
    """Listens to the keyboard and mouse inputs
    """
    is_init: bool = False

    def init() -> None:
        """Initializes the Input class. Has to be runned once before using Input.update()
        """
        nb_keys = len(key.get_pressed())
        nb_mouse_button = len(mouse.get_pressed())
        Input.__keys: Sequence = [False]*nb_keys
        Input.__keys_once: Sequence = [False]*nb_keys
        Input.__click: list[bool] = [False]*nb_mouse_button
        Input.__click_once: list[bool] = [False]*nb_mouse_button
        Input.__mouse_motion: v2 = v2(0,0)
        Input.__mouse_pos: v2 = v2(0,0)
        
        Input.is_init = True


    def is_pressed(key: int) -> bool:
        """Checks if a key is currently pressed

        Args:
            key (int): the given keyboard key

        Returns:
            bool: True if the key is currently pressed
        """
        return Input.__keys[key]
    
    def is_pressed_once(key: int) -> bool:
        """Checks if a key just got pressed

        Args:
            key (int): the given keyboard key

        Returns:
            bool: True if the key just got pressed
        """
        return Input.__keys_once[key]

    def is_clicked(button: int = None) -> bool:
        """Checks if a mouse button is currently pressed

        Args:
            button (int, optional): 1:Left, 2:Middle, 3:Right. All buttons if None. Defaults to None.

        Returns:
            bool: True if the given button is currently presssed
        """
        return any(Input.__click) if button is None else Input.__click[button]

    def is_clicked_once(button: int = None) -> bool:
        """Checks if a mouse button just got pressed

        Args:
            button (int, optional): 1:Left, 2:Middle, 3:Right. All buttons if None. Defaults to None.

        Returns:
            bool: True if the given button just got presssed
        """
        return any(Input.__click_once) if button is None else Input.__click_once[button]

    def get_motion() -> v2:
        """Returns the motion of the mouse cursor

        Returns:
            v2: Motion vector
        """
        return Input.__mouse_motion

    def get_mouse() -> v2:
        """Returns mouse coordinates

        Returns:
            v2: Mouse coordinates
        """
        return Input.__mouse_pos
        
    def update() -> None:
        """Update to current keyboard and mouse state
        """
        key_states : Sequence = key.get_pressed()
        Input.__keys_once = [not Input.__keys[i] and key_states[i] for i in range(len(key_states))]
        Input.__keys = key_states

        click_states: tuple[bool] = mouse.get_pressed()
        Input.__click_once = [not Input.__click[i] and click_states[i] for i in range(len(click_states))]
        Input.__click = click_states
        
        mouse_state = v2(mouse.get_pos())
        Input.__mouse_motion = mouse_state - Input.__mouse_pos
        Input.__mouse_pos = mouse.get_pos()
        
    