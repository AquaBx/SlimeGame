from pygame.event import Event

class CustomEvent:
    
    def __init__(self, key: str) -> None:
        self.key: str = key

class PlayerActionEvent(CustomEvent):
    
    def __init__(self, player) -> None:
        CustomEvent.__init__(self, "player_action")
        self.player = player

class PlayerDeathEvent(CustomEvent):
    def __init__(self) -> None:
        CustomEvent.__init__(self, "player_death")

class MenuEvent(CustomEvent):
    
    def __init__(self, action: str) -> None:
        CustomEvent.__init__(self, "menu")
        self.action: str = action

class TitleScreenEvent(CustomEvent):
    
    def __init__(self, action: str) -> None:
        CustomEvent.__init__(self, "title_screen")
        self.action: str = action

class DeathScreenEvent(CustomEvent):

    def __init__(self, action: str) -> None:
        CustomEvent.__init__(self, "death_screen")
        self.action: str = action

# Unused
class QuitEvent(CustomEvent):
    
    def __init__(self) -> None:
        CustomEvent.__init__(self, "quit")

class ChangeStageEvent(CustomEvent):
    
    def __init__(self, next_map: str, next_position) -> None:
        CustomEvent.__init__(self, "change_stage")
        self.next_map: str = next_map
        self.next_position: tuple[int, int] = next_position

class FlushPygameEvent(CustomEvent):
    
    def __init__(self, events: list[Event]) -> None:
        CustomEvent.__init__(self, "flush_pygame")
        self.events: list[Event] = events
