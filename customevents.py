class CustomEvent:
    
    def __init__(self, key: str) -> None:
        self.key: str = key

class PlayerActionEvent(CustomEvent):
    
    def __init__(self, player) -> None:
        CustomEvent.__init__(self, "player_action")
        self.player = player
