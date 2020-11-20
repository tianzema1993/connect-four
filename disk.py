class Disk:
    def __init__(self, x, y, diam, color):
        self.x = x
        self.y = y
        self.color = color
        self.active = True
        self.fall = False
        self.rate = 25
        self.diam = diam
        self.land = False

    def display(self):
        noStroke()
        if self.color == 'RED':
            fill(255, 0, 0)
            ellipse(self.x, self.y, self.diam, self.diam)
        if self.color == 'YELLOW':
            fill(255, 255, 0)
            ellipse(self.x, self.y, self.diam, self.diam)
