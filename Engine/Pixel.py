class Pixel:
    x = None
    y = None
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return 'Pixel(%s,%s)' % (self.x, self.y)

