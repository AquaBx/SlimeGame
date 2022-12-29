def update(self) -> None:
    self.player.update_frame()
    self.update_pos(self.player)
    self.camera.update()