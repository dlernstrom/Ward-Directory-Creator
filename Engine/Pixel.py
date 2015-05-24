# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Pixel(object):
    def __init__(self, x, y):
        self.x = int(round(x, 0))
        self.y = int(round(y, 0))

    def __unicode__(self):
        return 'Pixel(%s,%s)' % (self.x, self.y)
