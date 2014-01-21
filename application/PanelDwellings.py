import csv
import math

import wx
import  wx.lib.filebrowsebutton as filebrowse

from ColoredPanel import *
from rtree import index
from Calibration import Calibration
from Coordinate import Coordinate
from Dwellings import Dwelling, Dwellings
from Pixel import Pixel
from Maps import Map, Maps

class DwellingsPanel(ColoredPanel):
    Title = "Dwellings"
    def __init__(self, parent):
        ColoredPanel.__init__(self, parent, wx.BLUE)

        ScheduleGrid = wx.GridBagSizer()

        self.SetSizer(ScheduleGrid)

    def makingActive(self):
        self.annotate_images()

    def create_sortable_index(self):
        homes = Dwellings()
        self.idx = index.Index()
        counter = 0
        for entry in homes.dwellingList:
            left = float(entry.Longitude)
            bottom = float(entry.Latitude)
            right = float(entry.Longitude)
            top = float(entry.Latitude)
            self.idx.insert(counter, (left, bottom, right, top), obj=entry)
            counter += 1

    def annotate_images(self):
        self.create_sortable_index()
        # furthest north person is at 41.9706778
        # furthest south person is at ?
        # furthest west person is at -111.8081775
        # furthest east person is at -111.7705975
        ourMaps = Maps([Map(1, Coordinate(41.9720, -111.8117775), Coordinate(41.9720, -111.7669975), 'large', 'portrait', 'east', 16),
                        Map(2, Coordinate(41.9366, -111.806247), Coordinate(41.9366, -111.7958776), 'small', 'landscape', 'east', 17),
                        Map(3, Coordinate(41.93105, -111.8086775), Coordinate(41.93105, -111.799827), 'small', 'landscape', 'east', 18)])
        currentPosition = (-112, 45, -112, 45) # must be left, bottom, right, top
        done = False
        counter = 1
        """
        overrides = {13: (41.9557139, -111.7872486), # allen, craig
                     15: (41.9523412, -111.788422), # dutro
                     16: (41.9510287, -111.7850893), # compton
                     17: (41.950471, -111.7819565), # ernstrom
                     18: (41.9503411, -111.7882183), # eskelson
                     19: (41.94972, -111.7850972), # griffiths
                     }
        """
        while done == False:
            #if counter in overrides.keys():
            #    currentPosition = [overrides[counter][1], overrides[counter][0], overrides[counter][1], overrides[counter][0]] # must be left, bottom, right, top
            nearest = list(self.idx.nearest(coordinates = currentPosition,
                                            num_results=1,
                                            objects=True))
            if len(nearest) == 0:
                done = True
                continue
            print counter
            print "Nearest", nearest
            nearest = nearest[0]
            d = nearest.object
            #print "Nearest ID", nearest.id
            print "Nearest Object", d
            print "Nearest Bounds", nearest.bounds
            currentPosition = [d.Longitude, d.Latitude, d.Longitude, d.Latitude] # must be left, bottom, right, top
            self.idx.delete(nearest.id, currentPosition)
            ourMaps.annotate_coordinate(counter, Coordinate(d.Latitude, d.Longitude))
            print "*" * 30
            counter += 1
        ourMaps.save()

