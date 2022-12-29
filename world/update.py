def update(self) -> None:
    self.player.update_frame(self.is_flying(self.player)[0])
    self.update_pos(self.player)
    self.camera.update()