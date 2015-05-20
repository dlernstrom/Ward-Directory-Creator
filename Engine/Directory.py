# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import PageBreak, Paragraph, Spacer# Table, Image, Frame, Preformatted
from reportlab.platypus.flowables import HRFlowable, KeepInFrame
from reportlab.lib import colors

from DirectoryPages.PDFStyles import styles
from DirectoryPages.DirectoryPage import DirectoryPage

STANDARD_MARGIN = 0.25 * inch
STANDARD_FRAME_WIDTH = landscape(letter)[0]/2 - 2 * STANDARD_MARGIN


class Directory:
    flowableSectionOrder = ['prefix', 'directory', 'pre-map-spacers', 'maps', 'mapsLookup', 'post-map-spacers', 'suffix']
    pages = {'prefix': [],
             'directory': [],
             'maps': [],
             'mapsLookup': [],
             'post-map-spacers': [],
             'suffix': []} # pages is a dict of DirectoryPage lists

    def get_pages_for_binding(self, bindingType): # full or booklet
        result = []
        result.extend(self.pages['prefix'])
        result.extend(self.pages['directory'])
        result.extend(self.get_pre_map_spacers(bindingType))
        result.extend(self.pages['maps'])
        result.extend(self.pages['mapsLookup'])
        result.extend(self.get_post_map_spacers(bindingType))
        result.extend(self.pages['suffix'])
        pageNumber = 1
        for page in result:
            page.pageNumber = pageNumber
            pageNumber += 1
        return result

    def get_pre_map_spacers(self, bindingType): # full or booklet
        pageModulo = 2 # untested
        offset = 1
        if bindingType == 'full':
            pageModulo = 2 # untested
            offset = 2
        pages = []
        prefixLength = len(self.pages['prefix'])
        listingsLength = len(self.pages['directory'])

        usedFaces = prefixLength + listingsLength
        print "PRE MAP SPACERS"
        print "%d faces are present" % usedFaces
        fillers = (offset - usedFaces % pageModulo) % pageModulo
        print "%d blank faces will be added to make full pages" % fillers
        for count in xrange(fillers):
            pg = DirectoryPage()
            pg.flowables.extend(self.PrepareFiller())
            pages.append(pg)
        return pages

    def get_post_map_spacers(self, bindingType):
        pageModulo = 4 # untested
        if bindingType == 'full':
            pageModulo = 2 # untested
        pages = []
        prefixLength = len(self.pages['prefix'])
        listingsLength = len(self.pages['directory'])
        preMapSpacersLength = len(self.get_pre_map_spacers(bindingType))
        mapsLength = len(self.pages['maps'])
        mapsLookupLen = len(self.pages['mapsLookup'])
        suffixLength = len(self.pages['suffix'])

        usedFaces = prefixLength + listingsLength + preMapSpacersLength + mapsLength + mapsLookupLen + suffixLength
        print "POST MAP SPACERS"
        print "%d faces are present" % usedFaces
        fillers = (pageModulo - usedFaces % pageModulo) % pageModulo
        print "%d blank faces will be added to make full pages" % fillers
        for count in xrange(fillers):
            pg = DirectoryPage()
            pg.flowables.extend(self.PrepareFiller())
            pages.append(pg)
        return pages

    def PrepareFiller(self):
        LineSpace_List = []
        for counter in xrange(30):
            LineSpace_List.append(Spacer(width = STANDARD_FRAME_WIDTH, height = .25 * inch))
            LineSpace_List.append(HRFlowable(width = "90%", thickness = 1, lineCap= 'square', color = colors.black))
        ReturnList = [Paragraph(text = "NOTES", style = styles['Subtitle']),
                      KeepInFrame(maxWidth = STANDARD_FRAME_WIDTH,
                                  maxHeight = 7.5 * inch,
                                  content = LineSpace_List,
                                  mode = 'truncate'),
                      PageBreak()]
        return ReturnList

