# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
import os
import urllib
from cStringIO import StringIO

from PIL import Image, ImageDraw, ImageFont, ImageEnhance

from .Calibration import Calibration
from .Coordinate import Coordinate
from .Pixel import Pixel


class Map(object):
    """upperLeftCoordinate and upperRightCoordinate are as though the user was
    facing North
    """
    def __init__(self, path, index, upperLeftCoordinate, upperRightCoordinate,
                 size, initialOrientation, finalDirection, myConfig, title,
                 titleCorners):
        self.url = 'http://maps.googleapis.com/maps/api/staticmap'
        self.imgPath = path
        self.mapName = os.path.join(self.imgPath, 'Map%d_modified.bmp' % index)
        # coordinates define view area
        self.upperLeftCoordinate = up_left = upperLeftCoordinate
        self.upperRightCoordinate = up_right = upperRightCoordinate
        distance = abs(upperLeftCoordinate.longitude - \
                       upperRightCoordinate.longitude)

        # size in ['large', 'small']
        # we're going to assume 300dpi
        self.size = size
        self.initialOrientation = initialOrientation
        self.finalDirection = finalDirection # lowercase
        self.title = title
        self.titleCorners = titleCorners

        # 'small' = 5.5"x8.5", at 300dpi, this translates to 1650x2550
        if size == 'small':
            if initialOrientation == 'portrait':
                height_ratio = 2550.0 / 1650.0
            else:
                height_ratio = 1650.0 / 2550.0
        else:# 'large' = 11"x8.5", at 300dpi, this translates to 3300x2550
            if initialOrientation == 'portrait':
                height_ratio = 3300.0 / 2550.0
            else:
                height_ratio = 2550.0 / 3300.0
        height_ratio = height_ratio * .8 # accounts for non-square lat/long
        # latitude is how far north, longitude is how far west
        new_latt = upperLeftCoordinate.latitude - distance * height_ratio
        self.lowerLeftCoordinate = low_left = Coordinate(
            new_latt, upperLeftCoordinate.longitude)
        self.lowerRightCoordinate = Coordinate(
            new_latt, upperRightCoordinate.longitude)

        config = {16: {'horizToCenter': 0.006865, 'horizRepeat': 0.01373,
                       'horizRepeatPixels': 1280, 'vertToCenter': 0.0051125,
                       'vertRepeat': 0.009825, 'vertRepeatPixels': 1230,
                       'fontSize': 60},
                  17: {'horizToCenter': 0.006865, 'horizRepeat': 0.01373,
                       'horizRepeatPixels': 1280, 'vertToCenter': 0.0051125,
                       'vertRepeat': 0.009825, 'vertRepeatPixels': 1230,
                       'fontSize': 20},
                  18: {'horizToCenter': 0.006865, 'horizRepeat': 0.01373,
                       'horizRepeatPixels': 1280, 'vertToCenter': 0.0051125,
                       'vertRepeat': 0.009825, 'vertRepeatPixels': 1230,
                       'fontSize': 15}}
        self.config = config
        self.myConfig = myConfig
        # fontSize of 25 was too small, trying 30
        self.font = ImageFont.truetype(
            "arial.ttf", config[myConfig]['fontSize'], encoding="UTF-8")
        rows_perfect = abs(up_left.latitude - low_left.latitude) / \
            config[myConfig]['vertRepeat']
        rows = int(math.ceil(rows_perfect))
        cols_perfect = abs(up_left.longitude - up_right.longitude) / \
            config[myConfig]['horizRepeat']
        cols = int(math.ceil(cols_perfect))
        name_fmt = 'imageCache_Lat%.7f_Lon%.7f_z%s_r%s_c%s.bmp'
        cached_name = name_fmt % (up_left.latitude, up_left.longitude, 16,
                                  rows, cols)
        cache_fname = os.path.join(self.imgPath, cached_name)
        uncropped_low_right = Coordinate(
            up_left.latitude - rows * config[myConfig]['vertRepeat'],
            up_left.longitude + cols * config[myConfig]['horizRepeat'])
        if not os.path.isfile(cache_fname):
            pil_img = Image.new(
                "RGB", (cols * config[myConfig]['horizRepeatPixels'],
                        rows * config[myConfig]['vertRepeatPixels']), "black")
            for row in xrange(rows):
                for col in xrange(cols):
                    position = '%s,%s' % (
                        up_left.latitude - row * config[myConfig]['vertRepeat'] - config[myConfig]['vertToCenter'],
                        up_left.longitude + col * config[myConfig]['horizRepeat'] + config[myConfig]['horizToCenter'])
                    # at scale2, size will be 1280x1280, roughly 4" square
                    params = {'center':position,
                              'zoom':'16',
                              'size':'640x640',
                              'maptype':'roadmap',
                              'sensor':'false',
                              'scale':2}
                    query_string = '%s?%s' % (self.url,
                                              urllib.urlencode(params))
                    img = Image.open(
                        StringIO(urllib.urlopen(query_string).read()))
                    pil_img.paste(
                        img,
                        (col * config[myConfig]['horizRepeatPixels'],
                         row * config[myConfig]['vertRepeatPixels']))
            pil_img.save(cache_fname)
        else:
            pil_img = Image.open(cache_fname)

        enh = ImageEnhance.Contrast(pil_img)
        pil_img = enh.enhance(2.5)

        print "Rows Perfect: %s" % rows_perfect
        print "Rows: %s" % rows
        rows_ratio = (rows - rows_perfect) / float(rows)
        print "RowsRatio: %s" % rows_ratio
        cols_ratio = (cols - cols_perfect) / float(cols)
        width, height = pil_img.size
        left = 0 # west
        upper = 0 # north
        right = width - int(cols_ratio * width) # east
        lower = height - int(rows_ratio * height) # south
        self.calibration = Calibration(coord1=up_left,
                                       pixel1=Pixel(0, 0),
                                       coord2=uncropped_low_right,
                                       pixel2=Pixel(pil_img.size[0],
                                                    pil_img.size[1]))
        # left, upper, right, lower
        self.pilImage = pil_img.crop((left, upper, right, lower))
        self.rotate_image()
        self.draw = ImageDraw.Draw(self.pilImage)
        """
        # this would put a 3 pixel wide border around the whole thing.
        Problem is the large image aliases this away on the bottom edge
        w, h = self.pilImage.size
        self.draw.rectangle([(0, 0), (w - 1, h - 1)], outline='#000000')
        self.draw.rectangle([(1, 1), (w - 2, h - 2)], outline='#000000')
        self.draw.rectangle([(2, 2), (w - 3, h - 3)], outline='#000000')
        """

    def save_map(self):
        self.pilImage.save(self.mapName, "BMP")

    def get_map_half(self, side):
        w, h = self.pilImage.size
        upper = 0
        lower = h
        if side == 'left':
            left = 0
            right = w/2
        else:
            left = w/2
            right = w
        # left, upper, right, lower
        pil_img = self.pilImage.crop((left, upper, right, lower))
        f_handle = StringIO()
        pil_img.save(f_handle, 'PNG')
        f_handle.seek(0)
        return f_handle

    def get_map(self):
        f_handle = StringIO()
        self.pilImage.save(f_handle, 'PNG')
        f_handle.seek(0)
        return f_handle

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

    def write_text(self, text, position, drawBox=True, font=None):
        if font is None:
            font = self.font
        #print "Writing %s at: %s" % (text, position)
        width, height = self.draw.textsize(text, font=font)
        mid_width = width * 0.5
        mid_height = height * 0.5
        if drawBox:
            box = [
                (position.x - mid_width * 1.2, position.y - mid_height),
                (position.x + mid_width * 1.2, position.y + mid_height * 2.0)]
            self.draw.rectangle(box, outline='#000000', fill='#FFFFFF')
        self.draw.text((position.x - mid_width, position.y - mid_height),
                       text, fill='#000000', font=font)

    def draw_boxed_text(self, text, corner1, corner2, fontSize, opacity):
        position1 = self.calibration.translate_world_to_pixel(corner1)
        position1 = self.get_rotated_position(position1)
        position2 = self.calibration.translate_world_to_pixel(corner2)
        position2 = self.get_rotated_position(position2)
        width = abs(position1.x - position2.x)
        height = abs(position1.y - position2.y)
        # 0 is transparent, 255 is opaque
        front_box = Image.new('RGBA', (width, height), (255, 255, 255, opacity))
        front_box_draw = ImageDraw.Draw(front_box)
        front_box_draw.rectangle([(0, 0), (width-1, height-1)],
                                 outline='#000000')
        self.pilImage.paste(front_box, box=(min(position1.x, position2.x),
                                            min(position1.y, position2.y)),
                            mask=front_box)
        middle_of_box = Pixel(
            min(position1.x, position2.x) + abs(position2.x - position1.x)/2,
            min(position1.y, position2.y) + abs(position2.y - position1.y)/2)
        font = ImageFont.truetype("arial.ttf", fontSize, encoding="UTF-8")
        if '\n' not in text:
            self.write_text(
                text=text, position=middle_of_box, drawBox=False, font=font)
        else:
            width, height = self.draw.textsize(text, font=font)
            posTop = Pixel(middle_of_box.x, middle_of_box.y - height)
            self.write_text(text=text.split('\n')[0], position=posTop,
                            drawBox=False, font=font)
            posBottom = Pixel(middle_of_box.x, middle_of_box.y + height)
            self.write_text(text=text.split('\n')[1], position=posBottom,
                            drawBox=False, font=font)

    def draw_map_title(self):
        self.draw_boxed_text(
            text=self.title,
            corner1=self.titleCorners[0],
            corner2=self.titleCorners[1],
            fontSize=int(self.config[self.myConfig]['fontSize'] * 1.5),
            opacity=220)


class Maps(object):
    def __init__(self, pages):
        # pages = list of maps,
        # first will be a two pager, 8.5"x11" landscape
        # second and further will be insets on the first map
        # each page entry has a map entry
        self.pages = pages

    def annotate_coordinate(self, counter, coordinate):
        for page in self.pages:
            #print "annotating %s: %s" % (counter, coordinate)
            page.annotate(counter, coordinate)

    def annotate_insets(self):
        inset_counter = 1
        for inset_map in self.pages[1:]:
            self.pages[0].draw_boxed_text(
                text="See\nInset %d" % inset_counter,
                corner1=inset_map.upperLeftCoordinate,
                corner2=inset_map.lowerRightCoordinate,
                fontSize=100,
                opacity=170)
            inset_counter += 1
        for one_map in self.pages:
            one_map.draw_map_title()

    def save(self):
        self.annotate_insets()
        for page in self.pages:
            page.save_map()
