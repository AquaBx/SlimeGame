class Camera:

    def __init__(self, link):
        self.link = link

    def update(self):
        self.position = self.link.position
    
    def convert_coord(self,rect):
        #(block.rect.left - block.rect.width/2  - self.position.x + Config.WINDOW_W / 2,
        #              block.rect.bottom - camera.position.y + Config.WINDOW_H / 2)
#
        #(-self.rect.width/2 + Config.WINDOW_W / 2 , Config.WINDOW_H / 2 -self.rect.height/2  )
        return rect