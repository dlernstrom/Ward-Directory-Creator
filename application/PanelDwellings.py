import wx
from ColoredPanel import *
import  wx.lib.filebrowsebutton as filebrowse
from PIL import Image, ImageDraw, ImageFont

import csv
import math
from rtree import index

class DwellingsPanel(ColoredPanel):
    Title = "Dwellings"
    def __init__(self, parent):
        ColoredPanel.__init__(self, parent, wx.BLUE)

        ScheduleGrid = wx.GridBagSizer()

        self.SetSizer(ScheduleGrid)
        self.font  = ImageFont.truetype("arial.ttf", 25, encoding="UTF-8")

        #st = wx.StaticText(self, -1,
        #		  "Help will go here",
        #		  (10, 10))
        #st.SetForegroundColour(wx.WHITE)
        #st.SetBackgroundColour(wx.GREEN)

    def makingActive(self):
        fname = 'C:\\Users\\dlernstrom\\Desktop\\DirectoryCherryCreek\\Cherry_Creek_Ward.csv'
        reader = csv.reader(open(fname))
        myAddressData = []
        headerData = reader.next()
        try:
            while True:
                rowData = reader.next()
                if not rowData[0][0] == '-':
                    continue
                myAddressData.append(rowData)
        except Exception:
            pass
        #print myAddressData
        self.idx = index.Index()
        counter = 0
        for entry in myAddressData:
            left = float(entry[0])
            bottom = float(entry[1])
            right = float(entry[0])
            top = float(entry[1])
            self.idx.insert(counter, (left, bottom, right, top), obj=entry)
            print entry
            counter += 1
        self.annotate_image()

    def annotate_image(self):
        currentPosition = (-112, 45, -112, 45)

        fname = 'C:\\Users\\dlernstrom\\Desktop\\DirectoryCherryCreek\\Map1.bmp'
        image = Image.open(fname)
        self.draw  = ImageDraw.Draw(image)
        done = False
        counter = 1
        while done == False:
            nearest = list(self.idx.nearest(coordinates = currentPosition,
                                            num_results=1,
                                            objects=True))
            if len(nearest) == 0:
                done = True
                continue
            print nearest
            nearest = nearest[0]
            print nearest.id
            print nearest.object
            print nearest.bounds
            self.idx.delete(nearest.id, [float(nearest.object[0]), float(nearest.object[1]), float(nearest.object[0]), float(nearest.object[1])])
            currentPosition = [float(nearest.object[0]), float(nearest.object[1]), float(nearest.object[0]), float(nearest.object[1])]
            self.write_number(str(counter), [float(nearest.object[0]), float(nearest.object[1])])
            print counter
            counter += 1
        image.save('C:\\Users\\dlernstrom\\Desktop\\DirectoryCherryCreek\\Map1_modified.bmp',"BMP")

    def translate_world_to_pixel(self, worldCoordinates):
        known1 = [-111.7705975, 41.9706778, 150, 430]
        known2 = [-111.7993547, 41.9329083, 2740, 1850]
        worldXDistance = known2[0] - known1[0]
        worldYDistance = known2[1] - known1[1]
        pixelXDistance = known2[2] - known1[2]
        pixelYDistance = known2[3] - known1[3]
        targetXDistance = worldCoordinates[0] - known1[0]
        targetYDistance = worldCoordinates[1] - known1[1]
        targetXRatioWorld = targetXDistance / worldXDistance
        targetYRatioWorld = targetYDistance / worldYDistance
        pixelCoordinateX = targetXRatioWorld * pixelXDistance + known1[2]
        pixelCoordinateY = targetYRatioWorld * pixelYDistance + known1[3]
        pixelCoordinates = [pixelCoordinateX, pixelCoordinateY]
        return pixelCoordinates

    def write_number(self, number, position):
        position = self.translate_world_to_pixel(position)
        #width, height = self.font.getsize(number)
        width, height = self.draw.textsize(number, font=self.font)
        upperLeftX = position[0] - math.ceil(width / 2.0)
        upperLeftY = position[1] - math.ceil(height / 2.0)
        print width, height
        box = [(upperLeftX - 2, upperLeftY), (upperLeftX + width + 1, upperLeftY + height + 5)]
        box = [(upperLeftX, upperLeftY), (upperLeftX + width + 1, upperLeftY + height + 9)]
        self.draw.rectangle(box, outline='#000000', fill='#FFFFFF')
        self.draw.text( (upperLeftX, upperLeftY), number, fill='#000000', font=self.font)

