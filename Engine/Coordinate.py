# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Coordinate(object):
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return 'Coordiante(%s,%s)' % (self.latitude, self.longitude)

    def swap(self):
        tmp = self.longitude
        self.longitude = self.latitude
        self.latitude = tmp
