from typing import Any

class ButtonScript:
    def __init__(self, fct, *args) -> None:
        self.fct = fct
        self.args = args

    def __call__(self) -> Any:
        #eventuel override des arguments prédéfinis a cet endroit
        self.fct(*self.args)

    def set_quit(game):
        game.should_quit = True
    
    def set_resume(game):
        game.resume = True