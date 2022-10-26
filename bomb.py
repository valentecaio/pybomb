from bprint import bprint

class Bomb:
    def __init__(self, x, y, timer, range):
        self.x = x
        self.y = y
        self.timer = timer
        self.range = range

    def draw(self):
        if self.timer < 0:
            bprint.p("O", bprint.RED)
        elif self.timer%2 == 1:
            bprint.p("Ó", bprint.BOLD)
        else:
            bprint.p("ó", bprint.BOLD)

