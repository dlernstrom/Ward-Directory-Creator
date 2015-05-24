# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from Pixel import Pixel


class Calibration(object):
    def __init__(self, coord1, pixel1, coord2, pixel2):
        self.pixel1 = pixel1
        self.coord1 = coord1
        self.pixel2 = pixel2
        self.coord2 = coord2
        self.worldWestDistance = self.coord2.longitude - self.coord1.longitude
        self.worldNorthDistance = self.coord2.latitude - self.coord1.latitude
        self.pixelXDistance = self.pixel2.x - self.pixel1.x
        self.pixelYDistance = self.pixel2.y - self.pixel1.y

    def translate_world_to_pixel(self, worldCoordinate):
        targetWestDistance = worldCoordinate.longitude - self.coord1.longitude # from known 1
        targetNorthDistance = worldCoordinate.latitude - self.coord1.latitude # from known 1
        targetXRatioWorld = targetWestDistance / self.worldWestDistance
        targetYRatioWorld = targetNorthDistance / self.worldNorthDistance
        pixelCoordinateX = targetXRatioWorld * self.pixelXDistance + self.pixel1.x
        pixelCoordinateY = targetYRatioWorld * self.pixelYDistance + self.pixel1.y
        pixelCoordinates = Pixel(pixelCoordinateX, pixelCoordinateY)
        return pixelCoordinates
