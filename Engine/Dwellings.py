# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
from decimal import Decimal


class Dwelling(object):
    mapIndex = None
    def __init__(self, dwellingDict):
        # DwellingDict has the following keys:
        self.Street = None
        self.City = None
        self.State = None
        self.Zip = None
        keys = dwellingDict.keys()
        for key in keys:
            setattr(self, key, dwellingDict[key])
        self.Longitude = float(self.Longitude)
        self.Latitude = float(self.Latitude)
        self.dwellingDict = dwellingDict
        params = (self.Street.replace(',', ''), self.City, self.State,
                  self.Zip)
        self.addressForCompare = '%s\n%s, %s %s' % params
        if not self.NextDwellingOverride == '':
            print self.NextDwellingOverride
            print len(self.NextDwellingOverride)

            self.NextDwellingOverride = (
                Decimal(self.NextDwellingOverride.split(',')[0].split('(')[1].strip()),
                Decimal(self.NextDwellingOverride.split(',')[1].split(')')[0].strip()))

    def __repr__(self):
        return '%s\n%s, %s %s' % (self.Street, self.City, self.State, self.Zip)

    def save_map_index(self, mapIndex):
        self.mapIndex = mapIndex
        self.dwellingDict['MapIndex'] = mapIndex


class Dwellings(object):
    def __init__(self, dwellings_file_name):
        self.dwellingsFname = dwellings_file_name
        self.dwellingList = []
        self.read_from_file()

    def order_dwelling_list(self):
        self.dwellingList = sorted(self.dwellingList, key=lambda x: x.mapIndex)

    def __del__(self):
        self.write_to_file()

    def read_from_file(self):
        reader = csv.DictReader(open(self.dwellingsFname))
        try:
            while True:
                self.add_dwelling_if_unique(Dwelling(reader.next()))
        except StopIteration:
            pass

    def add_dwelling_if_unique(self, d):
        for currDwelling in self.dwellingList:
            if str(currDwelling) == str(d):
                print "Dwelling already exists!"
                print currDwelling
                return
        self.dwellingList.append(d)

    def write_to_file(self):
        print "Saving file"
        writer = csv.DictWriter(open(self.dwellingsFname, 'wb'),
                                ["MapIndex", "Longitude", "Latitude", "Street",
                                 "City", "State", "Zip",
                                 'NextDwellingOverride'])
        writer.writeheader()
        for d in self.dwellingList:
            writer.writerow(d.dwellingDict)

    def find_map_index_for_household(self, household):
        for d in self.dwellingList:
            if household.familyAddress == d.addressForCompare:
                return d.mapIndex
        return None
