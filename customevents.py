class CustomEvent:
    
    def __init__(self, key: str) -> None:
        self.key: str = key

class PlayerActionEvent(CustomEvent):
    
    def __init__(self, player) -> None:
        CustomEvent.__init__(self, "player_action")
        self.player = player

class MenuEvent(CustomEvent):
    
    def __init__(self, action: str) -> None:
        CustomEvent.__init__(self, "menu")
        self.action: str = action

class TitleScreenEvent(CustomEvent):
    
    def __init__(self, action: str) -> None:
        CustomEvent.__init__(self, "title_screen")
        self.action: str = action

class QuitEvent(CustomEvent):
    
    def __init__(self) -> None:
        CustomEvent.__init__(self, "quit")
