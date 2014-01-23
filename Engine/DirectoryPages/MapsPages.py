import logging
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import Preformatted, Frame, Image, PageBreak, Paragraph, Table, TableStyle, Spacer, ParagraphAndImage
from reportlab.platypus.flowables import HRFlowable, KeepInFrame
from reportlab.pdfgen.canvas import Canvas

from PDFStyles import styles
from TextOnImage import TextOnImage
from DirectoryPage import DirectoryPage

STANDARD_MARGIN = 0.25 * inch
STANDARD_FRAME_WIDTH = landscape(letter)[0]/2 - 2 * STANDARD_MARGIN

def get_maps_pages(configData, membershipList, debug):
    pages = []
    pg = DirectoryPage()
    pg.flowables.extend(PrepareFiller('Map', 1))
    pages.append(pg)
    pg = DirectoryPage()
    pg.flowables.extend(PrepareFiller('Map', 2))
    pages.append(pg)
    pg = DirectoryPage()
    pg.flowables.extend(PrepareFiller('Map', 3))
    pages.append(pg)
    pg = DirectoryPage()
    pg.flowables.extend(PrepareFiller('Map', 4))
    pages.append(pg)
    return pages

def get_maps_lookup_pages(configData, membershipList, debug):
    pages = []
    pg = DirectoryPage()
    pg.flowables.extend(PrepareFiller('MapLookup', 1))
    pages.append(pg)
    pg = DirectoryPage()
    pg.flowables.extend(PrepareFiller('MapLookup', 2))
    pages.append(pg)
    pg = DirectoryPage()
    pg.flowables.extend(PrepareFiller('MapLookup', 3))
    pages.append(pg)
    return pages

def PrepareFiller(title, pageCounter):
    LineSpace_List = []
    for counter in xrange(30):
        LineSpace_List.append(Spacer(width = STANDARD_FRAME_WIDTH, height = .25 * inch))
        LineSpace_List.append(HRFlowable(width = "90%", thickness = 1, lineCap= 'square', color = colors.black))
    ReturnList = [Paragraph(text = "%s Page %d" % (title, pageCounter), style = styles['Subtitle']),
                  KeepInFrame(maxWidth = STANDARD_FRAME_WIDTH,
                              maxHeight = 7.5 * inch,
                              content = LineSpace_List,
                              mode = 'truncate'),
                  PageBreak()]
    return ReturnList

