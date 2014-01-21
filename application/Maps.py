import math
import os
import urllib, urllib2
from cStringIO import StringIO

import PIL
from PIL import Image, ImageDraw, ImageFont

from Calibration import Calibration
from Coordinate import Coordinate
from Pixel import Pixel

class Map:
    def __init__(self, index, upperLeftCoordinate, upperRightCoordinate, size, initialOrientation, finalDirection, myConfig):
        self.url = 'http://maps.googleapis.com/maps/api/staticmap'
        self.imgPath = 'C:\\Users\\dlernstrom\\Desktop\\DirectoryCherryCreek\\'
        self.mapName = self.imgPath + 'Map%d_modified.bmp' % index
        # coordinates define view area
        self.upperLeftCoordinate = ul = upperLeftCoordinate
        self.upperRightCoordinate = ur = upperRightCoordinate
        distance = abs(upperLeftCoordinate.longitude - upperRightCoordinate.longitude)

        # size in ['large', 'small']
        # we're going to assume 300dpi
        self.size = size
        self.initialOrientation = initialOrientation
        self.finalDirection = finalDirection # lowercase

        if size == 'small': # 'small' = 5.5"x8.5", at 300dpi, this translates to 1650x2550
            if initialOrientation == 'portrait':
                heightRatio = 2550.0 / 1650.0
            else:
                heightRatio = 1650.0 / 2550.0
        else:# 'large' = 11"x8.5", at 300dpi, this translates to 3300x2550
            if initialOrientation == 'portrait':
                heightRatio = 3300.0 / 2550.0
            else:
                heightRatio = 2550.0 / 3300.0
        heightRatio = heightRatio * .8 # accounts for non-square lat/long
        # latitude is how far north, longitude is how far west
        newLatitude = upperLeftCoordinate.latitude - distance * heightRatio
        self.lowerLeftCoordinate = ll = Coordinate(newLatitude, upperLeftCoordinate.longitude)
        self.lowerRightCoordinate = lr = Coordinate(newLatitude, upperRightCoordinate.longitude)

        config = {16: {'horizToCenter': 0.006865, 'horizRepeat': 0.01373, 'horizRepeatPixels': 1280, 'vertToCenter': 0.0051125, 'vertRepeat': 0.009825, 'vertRepeatPixels': 1230, 'fontSize': 60},
                  17: {'horizToCenter': 0.006865, 'horizRepeat': 0.01373, 'horizRepeatPixels': 1280, 'vertToCenter': 0.0051125, 'vertRepeat': 0.009825, 'vertRepeatPixels': 1230, 'fontSize': 20},
                  18: {'horizToCenter': 0.006865, 'horizRepeat': 0.01373, 'horizRepeatPixels': 1280, 'vertToCenter': 0.0051125, 'vertRepeat': 0.009825, 'vertRepeatPixels': 1230, 'fontSize': 15}}
        self.font  = ImageFont.truetype("arial.ttf", config[myConfig]['fontSize'], encoding="UTF-8") # fontSize of 25 was too small, trying 30
        rowsPerfect = abs(ul.latitude - ll.latitude) / config[myConfig]['vertRepeat']
        rows = int(math.ceil(rowsPerfect))
        colsPerfect = abs(ul.longitude - ur.longitude) / config[myConfig]['horizRepeat']
        cols = int(math.ceil(colsPerfect))
        cachedName = 'imageCache_Lat%.7f_Lon%.7f_z%s_r%s_c%s.bmp' % (ul.latitude, ul.longitude, 16, rows, cols)
        unCroppedLR = Coordinate(ul.latitude - rows * config[myConfig]['vertRepeat'], ul.longitude + cols * config[myConfig]['horizRepeat'])
        if not os.path.isfile(self.imgPath + cachedName):
            pilImage = Image.new("RGB", (cols * config[myConfig]['horizRepeatPixels'], rows * config[myConfig]['vertRepeatPixels']), "black")
            for row in xrange(rows):
                for col in xrange(cols):
                    position = '%s,%s' % (ul.latitude - row * config[myConfig]['vertRepeat'] - config[myConfig]['vertToCenter'],
                                          ul.longitude + col * config[myConfig]['horizRepeat'] + config[myConfig]['horizToCenter'])
                    params = {'center':position,
                              'zoom':'16',
                              'size':'640x640',
                              'maptype':'roadmap',
                              'sensor':'false',
                              'scale':2} # at scale2, size will be 1280x1280, roughly 4" square
                    qs = '%s?%s' % (self.url, urllib.urlencode(params))
                    img = Image.open(StringIO(urllib.urlopen(qs).read()))
                    pilImage.paste(img, (col * config[myConfig]['horizRepeatPixels'], row * config[myConfig]['vertRepeatPixels']))
            pilImage.save(self.imgPath + cachedName)
        else:
            pilImage = Image.open(self.imgPath + cachedName)

        print "Rows Perfect: %s" % rowsPerfect
        print "Rows: %s" % rows
        rowsRatio = (rows - rowsPerfect) / float(rows)
        print "RowsRatio: %s" % rowsRatio
        colsRatio = (cols - colsPerfect) / float(cols)
        w, h = pilImage.size
        left = 0 # west
        upper = 0 # north
        right = w - int(colsRatio * w) # east
        lower = h - int(rowsRatio * h) # south
        self.calibration = Calibration(coord1 = ul,
                                       pixel1 = Pixel(0, 0),
                                       coord2 = unCroppedLR,
                                       pixel2 = Pixel(pilImage.size[0], pilImage.size[1]))
        self.pilImage = pilImage.crop((left, upper, right, lower)) # left, upper, right, lower
        self.rotate_image()
        self.draw  = ImageDraw.Draw(self.pilImage)

    def save_map(self):
        self.pilImage.save(self.mapName, "BMP")

    def rotate_image(self):
        if self.finalDirection == 'east':
            self.pilImage = self.pilImage.rotate(90)
        elif self.finalDirection == 'west':
            self.pilImage = self.pilImage.rotate(-90)
        elif self.finalDirection == 'north':
            pass

    def get_rotated_position(self, position):
        w, h = self.pilImage.size
        if self.finalDirection == 'east':
            position = Pixel(position.y, h - position.x)
        elif self.finalDirection == 'west':
            position = Pixel(w - position.y, position.x)
        elif self.finalDirection == 'north':
            pass
        return position

    def annotate(self, counter, coordinate):
        position = self.calibration.translate_world_to_pixel(coordinate)
        position = self.get_rotated_position(position)
        self.write_text(str(counter), position)

    def write_text(self, text, position):
        print "Writing %s at: %s" % (text, position)
        width, height = self.draw.textsize(text, font=self.font)
        midWidth = width * 0.5
        midHeight = height * 0.5
        box = [(position.x - midWidth * 1.2, position.y - midHeight), (position.x + midWidth * 1.2, position.y + midHeight * 2.0)]
        self.draw.rectangle(box, outline='#000000', fill='#FFFFFF')
        self.draw.text( (position.x - midWidth, position.y - midHeight), text, fill='#000000', font=self.font)

    def annotate_inset(self, corner1, corner2):
        position1 = self.calibration.translate_world_to_pixel(corner1)
        position1 = self.get_rotated_position(position1)
        position2 = self.calibration.translate_world_to_pixel(corner2)
        position2 = self.get_rotated_position(position2)
        box = [(position1.x, position1.y), (position2.x, position2.y)]
        self.draw.rectangle(box, outline='#000000', fill='#FFFFFF')

class Maps:
    def __init__(self, pages):
        # pages = list of maps, first will be a two pager, 8.5"x11" landscape
        #                       second and further will be insets on the first map
        # each page entry has a map entry
        self.pages = pages

    def annotate_coordinate(self, counter, coordinate):
        for mapPage in self.pages:
            print "annotating %s: %s" % (counter, coordinate)
            mapPage.annotate(counter, coordinate)

    def save(self):
        for insetMap in self.pages[1:]:
            self.pages[0].annotate_inset(insetMap.upperLeftCoordinate, insetMap.lowerRightCoordinate)
        for mapPage in self.pages:
            mapPage.save_map()

