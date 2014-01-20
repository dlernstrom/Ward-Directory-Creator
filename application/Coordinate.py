class Coordinate:
    latitude = None # 41.93
    longitude = None # -111.80
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return 'Coordiante(%s,%s)' % (self.latitude, self.longitude)

    def swap(self):
        tmp = self.longitude
        self.longitude = self.latitude
        self.latitude = tmp