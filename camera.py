class Camera:

    def __init__(self, link):
        self.link = link

    def update(self):
        self.position = self.link.position