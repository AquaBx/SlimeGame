from pygame import Rect

from pygame_gui.elements.ui_button import UIButton
from pygame_gui.windows.ui_file_dialog import UIFileDialog
from pygame_gui.elements.ui_selection_list import UISelectionList

from config import *
from assets import MAP_DIR
from serializer import Serializer
from gamestates import GameStates

class GUI:

    def __init__(self, editor) -> None:
        self.editor = editor
        self.buttons = {
            l:(UIButton(relative_rect=r,manager=GameStates.ui_manager, text=l),f) for r,l,f in [
                (Rect(WINDOW_W-200,WINDOW_H-90,100,30),"Load Tile", self.load_tile),
                (Rect(WINDOW_H-150,WINDOW_H-60,100,30),"Save Map",  self.save_map),
                (Rect(WINDOW_H-150,WINDOW_H-30,100,30),"Load Map",  self.load_map),
                (Rect(WINDOW_W-100,WINDOW_H-90,100,30),"CT",        self.compute_ct),
                (Rect(WINDOW_W-100,WINDOW_H-60,100,30),"Clear",     self.clear_grid),
                (Rect(WINDOW_W-100,WINDOW_H-30,100,30),"Quit",      self.quit_editor)
            ]
        }

        # this functionnality is not yet implemented
        self.buttons["Load Tile"][0].disable()

        self.file_selections: dict[str, UIFileDialog] = { "load": None, "save": None }
        self.palette_tile_selection: UISelectionList = None
        self.current_hovered_tile_selection: int = None

    def detect_pressed_button(self, button: UIButton) -> None:
        """Detects which button got pressed and executes its script

        Args:
            button (UIButton): Pressed button 
        """
        # menu buttons
        # These buttons are used to close a menu
        if("#cancel_button" in button.object_ids or "#close_button" in button.object_ids):
            GameStates.menu_open = False

        # These buttons are used while in a menu
        elif ("#ok_button" in button.object_ids):
            GameStates.menu_open = False

            if("map_loading" in button.object_ids):
                file = self.file_selections["load"].current_file_path.name
                self.editor.palette, self.editor.grid = Serializer.deserialize(file)
                self.file_selections["load"] = None
            elif("map_saving" in button.object_ids):
                file: str = self.file_selections["save"].current_file_path.name
                Serializer.serialize(self.editor.grid, self.editor.palette, file if file.endswith(".map") else f"{file}.map")
                self.file_selections["save"] = None

        # non menu buttons
        # These buttons cannot be used while in a menu
        if not GameStates.menu_open:
            if button.text in self.buttons:
                self.buttons[button.text][1]()

    def load_tile(self) -> None:
        """Opens tile loading menu (not implemented)
        """
        self.palette_tile_selection = UISelectionList(
            Rect(0, 0, 500, 500),
            manager=GameStates.ui_manager,
            item_list=[str(i) for i in range(100)],
            object_id="asset_selection"
        )
        GameStates.menu_open = True

    def save_map(self) -> None:
        """Opens map saving menu
        """
        self.file_selections["save"] = UIFileDialog(
            rect=Rect(0, 0, WINDOW_W, WINDOW_H),
            manager=GameStates.ui_manager,
            allow_existing_files_only=False,
            window_title="Save map",
            initial_file_path=MAP_DIR,
            object_id="map_saving"
        )
        GameStates.menu_open = True

    def load_map(self) -> None:
        """Opens map loading menu
        """
        self.file_selections["load"] = UIFileDialog(
            rect=Rect(0, 0, WINDOW_W, WINDOW_H),
            manager=GameStates.ui_manager,
            allow_existing_files_only=True,
            window_title="Load map",
            initial_file_path=MAP_DIR,
            object_id="map_loading"
        )
        GameStates.menu_open = True

    def quit_editor(self) -> None:
        GameStates.should_quit = True

    def clear_grid(self) -> None:
        self.editor.grid.clear()

    def compute_ct(self) -> None:
        self.editor.grid.compute_ct(self.editor.palette)
