import os
import urllib, urllib2
from cStringIO import StringIO

import PIL
from PIL import Image, ImageDraw, ImageFont

from Coordinate import Coordinate

class Map:
    def __init__(self, index, upperLeftCoordinate, upperRightCoordinate, size, orientation):
        # coordinates define view area
        self.upperLeftCoordinate = upperLeftCoordinate
        self.upperRightCoordinate = upperRightCoordinate
        # size in ['large', 'small']
        self.size = size
        # we're going to assume 300dpi
        # 'large' = 11"x8.5", at 300dpi, this translates to 3300x2550
        # 'small' = 5.5"x8.5", at 300dpi, this translates to 1650x2550
        self.size = size
        # orientation in ['portrait', 'landscape']
        self.orientation = orientation
        # latitude is how far north, longitude is how far west
        if abs(upperLeftCoordinate.longitude - upperRightCoordinate.longitude) > abs(upperLeftCoordinate.latitude - upperRightCoordinate.latitude):
            self.establish_north_rotation()
            ul = self.upperLeftCoordinate
            lr = self.lowerRightCoordinate
        else:
            if upperLeftCoordinate.latitude > upperRightCoordinate.latitude:
                self.establish_east_rotation()
                ul = self.lowerLeftCoordinate
                lr = self.upperRightCoordinate
            else:
                self.establish_west_rotation()
                ul = self.upperRightCoordinate
                lr = self.lowerLeftCoordinate
        # I need to get the bounds of the image that is returned
        # best thing I can do is retrieve 2 images and start guessing

        url = 'http://maps.googleapis.com/maps/api/staticmap'
        config = {16: {'horizToCenter': 0.006865, 'horizRepeat': 0.01373, 'horizRepeatPixels': 1280, 'vertToCenter': 0.0051125, 'vertRepeat': 0.009825, 'vertRepeatPixels': 1230}}
        myConfig = 16
        rows = 5
        cols = 4
        imgPath = 'C:\\Users\\dlernstrom\\Desktop\\DirectoryCherryCreek\\'
        cachedName = 'imageCache_Lat%.3f_Lon%.3f_z%s_r%s_c%s.bmp' % (ul.latitude, ul.longitude, 16, rows, cols)
        if not os.path.isfile(imgPath + cachedName):
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
                    qs = '%s?%s' % (url, urllib.urlencode(params))
                    img = Image.open(StringIO(urllib.urlopen(qs).read()))
                    pilImage.paste(img, (col * config[myConfig]['horizRepeatPixels'], row * config[myConfig]['vertRepeatPixels']))
            pilImage.save(imgPath + cachedName)
        else:
            pilImage = Image.open(imgPath + cachedName)
        #TODO: let's trim the image now to the size we were after in the first place
        if self.rotate == 'East':
            pilImage = pilImage.rotate(90)
        elif self.rotate == 'West':
            pilImage = pilImage.rotate(-90)
        pilImage.save(imgPath + 'Map%d_modified.bmp' % index,"BMP")

    def establish_east_rotation(self):
        # latitude is how far north, longitude is how far west
        self.rotate = 'East'
        distance = abs(self.upperLeftCoordinate.latitude - self.upperRightCoordinate.latitude)
        if self.orientation == 'portrait':# small
            if self.size == 'large':
                raise Exception("Impossible!")
            # 1650x2550
            westDistance = distance * 2550.0 / 1650.0
        else: # landscape, large
            if self.size == 'small':
                raise Exception("Impossible!")
            # 3300x2550
            westDistance = distance * 2550.0 / 3300.0
        self.lowerLeftCoordinate = Coordinate(self.upperLeftCoordinate.latitude, self.upperLeftCoordinate.longitude - westDistance)
        self.lowerRightCoordinate = Coordinate(self.upperRightCoordinate.latitude, self.upperRightCoordinate.longitude - westDistance)

    def establish_west_rotation(self):
        # latitude is how far north, longitude is how far west
        self.rotate = 'West'
        distance = abs(self.upperLeftCoordinate.latitude - self.upperRightCoordinate.latitude)
        if self.orientation == 'portrait':# small
            if self.size == 'large':
                raise Exception("Impossible!")
            # 1650x2550
            eastDistance = distance * 2550.0 / 1650.0
        else: # landscape, large
            if self.size == 'small':
                raise Exception("Impossible!")
            # 3300x2550
            eastDistance = distance * 2550.0 / 3300.0
        self.lowerLeftCoordinate = Coordinate(self.upperLeftCoordinate.latitude, self.upperLeftCoordinate.longitude + eastDistance)
        self.lowerRightCoordinate = Coordinate(self.upperRightCoordinate.latitude, self.upperRightCoordinate.longitude + eastDistance)

    def establish_north_rotation(self):
        # latitude is how far north, longitude is how far west
        self.rotate = 'North'
        distance = abs(self.upperLeftCoordinate.longitude - self.upperRightCoordinate.longitude)
        if self.orientation == 'portrait':# small
            if self.size == 'large':
                raise Exception("Impossible!")
            # 1650x2550
            southDistance = distance * 2550.0 / 1650.0
        else: # landscape, large
            if self.size == 'small':
                raise Exception("Impossible!")
            # 3300x2550
            southDistance = distance * 2550.0 / 3300.0
        self.lowerLeftCoordinate = Coordinate(self.upperLeftCoordinate.latitude - southDistance, self.upperLeftCoordinate.longitude)
        self.lowerRightCoordinate = Coordinate(self.upperRightCoordinate.latitude - southDistance, self.upperRightCoordinate.longitude)

    def annotate(self, counter, coordinate):
        """
        fname = 'C:\\Users\\dlernstrom\\Desktop\\DirectoryCherryCreek\\Map1.bmp'
        calibration = Calibration(coord1 = Coordinate(41.9706778, -111.7705975),
                                  pixel1 = Pixel(150, 430),
                                  coord2 = Coordinate(41.9329083, -111.7993547),
                                  pixel2 = Pixel(2740, 1870),
                                  rotated = True)
        image = Image.open(fname)
        self.draw  = ImageDraw.Draw(image)
        """
        #self.font  = ImageFont.truetype("arial.ttf", 25, encoding="UTF-8")
        position = self.calibration.translate_world_to_pixel(Coordinate(d.latitude, d.longitude))
        self.write_text(str(counter), position)

    def write_text(self, text, position):
        #width, height = self.font.getsize(text)
        width, height = self.draw.textsize(text, font=self.font)
        upperLeftX = position.x - math.ceil(width / 2.0)
        upperLeftY = position.y - math.ceil(height / 2.0)
        box = [(upperLeftX, upperLeftY), (upperLeftX + width + 1, upperLeftY + height + 9)]
        self.draw.rectangle(box, outline='#000000', fill='#FFFFFF')
        self.draw.text( (upperLeftX, upperLeftY), text, fill='#000000', font=self.font)

class Maps:
    def __init__(self, pages):
        # pages = list of maps, first will be a two pager, 8.5"x11" landscape
        #                       second and further will be insets on the first map
        # each page entry has a map entry
        self.pages = pages

    def annotate_coordinate(self, counter, coordinate):
        """
        for mapPage in self.pages:
            mapPage.annotate(counter, coordinate)
        """
        pass




