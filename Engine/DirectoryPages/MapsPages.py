import logging
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import Preformatted, Frame, Image, PageBreak, Paragraph, Table, TableStyle, Spacer
from reportlab.platypus.flowables import HRFlowable, KeepInFrame
from reportlab.pdfgen.canvas import Canvas

from PDFStyles import styles
from TextOnImage import TextOnImage
from DirectoryPage import DirectoryPage

STANDARD_MARGIN = 0.25 * inch
HALF_PAGE_WIDTH = landscape(letter)[0]/2
STANDARD_FRAME_WIDTH = HALF_PAGE_WIDTH - 2 * STANDARD_MARGIN
STANDARD_FRAME_HEIGHT = landscape(letter)[1] - 2 * STANDARD_MARGIN
STANDARD_TABLE_WIDTH = (STANDARD_FRAME_WIDTH - STANDARD_MARGIN) / 2
STANDARD_TABLE_HEIGHT = STANDARD_FRAME_HEIGHT - 1.0 * inch

def get_maps_pages(configData, maps, membershipList, debug):
    pages = []
    MAP_PAGE_WIDTH = HALF_PAGE_WIDTH - STANDARD_MARGIN
    maps.annotate_insets()
    for oneMap in maps.pages:
        if oneMap.size == 'small':
            pg = DirectoryPage()
            pg.flowables.append('CURRENT_PAGE_NUMBER')
            pg.flowables.append(Image(oneMap.get_map(),
                                      width = MAP_PAGE_WIDTH,
                                      height = 8.5 * inch, # overridden by the proportional flag, but still a required parameter, perhaps should set this to the available height remaining TODO
                                      kind = 'proportional'))
            pages.append(pg)
        if oneMap.size == 'large':
            pg = DirectoryPage(rightPadding = 0)
            pg.flowables.append('CURRENT_PAGE_NUMBER')
            pg.flowables.append(Image(oneMap.get_map_half('left'),
                                      width = MAP_PAGE_WIDTH,
                                      height = 8.5 * inch, # overridden by the proportional flag, but still a required parameter, perhaps should set this to the available height remaining TODO
                                      kind = 'proportional'))
            pages.append(pg)
            pg = DirectoryPage(leftPadding = 0)
            pg.flowables.append('CURRENT_PAGE_NUMBER')
            pg.flowables.append(Image(oneMap.get_map_half('right'),
                                      width = MAP_PAGE_WIDTH,
                                      height = 8.5 * inch, # overridden by the proportional flag, but still a required parameter, perhaps should set this to the available height remaining TODO
                                      kind = 'proportional'))
            pages.append(pg)
    return pages

def make_member_dwellings_dict(dwellingsHandle, membershipList):
    myDict = {}
    for household in membershipList:
        index = dwellingsHandle.find_map_index_for_household(household)
        if not index == None:
            myDict[index - 1] = myDict.get(index - 1, []) + [household]
    return myDict

def get_maps_lookup_pages(configData, dwellingsHandle, membershipList, debug):
    pages = []
    memberDwellingsDict = make_member_dwellings_dict(dwellingsHandle, membershipList)
    tableData = [['#', 'Name']]
    for dwellingCounter in xrange(len(dwellingsHandle.dwellingList)): # we are confident that this has already been sorted by map index
        dwelling = dwellingsHandle.dwellingList[dwellingCounter]
        print "Dwelling: %s %s" % (dwelling.mapIndex, dwelling)
        members = memberDwellingsDict.get(dwellingCounter, [])
        print "Members: %s" % str(members)
        membersString = '\n'.join(map(lambda x: x.coupleName, members))
        tableData.append([dwellingCounter + 1, membersString])
    mapIndexWidth = 0.3 * inch
    nameWidth = STANDARD_TABLE_WIDTH - mapIndexWidth
    myTable = Table(data = tableData,
                    colWidths = [mapIndexWidth, nameWidth],
                    style = TableStyle([('GRID', (0,0), (-1,-1), 0.25, colors.black),
                                        ('FONTSIZE', (0,0), (-1,-1), 8),
                                        ('VALIGN', (0,0), (-1,-1), 'TOP'),
                                        ('ALIGNMENT', (0, 0), (0, -1), 'CENTRE'),
                                        ]),
                    repeatRows = 1)
    result = myTable.split(STANDARD_TABLE_WIDTH, STANDARD_TABLE_HEIGHT)
    brokenDownTables = []
    while len(result) == 2:
        brokenDownTables.append(result[0])
        result = result[1].split(STANDARD_TABLE_WIDTH, STANDARD_TABLE_HEIGHT)
    brokenDownTables.append(result[0])
    while len(brokenDownTables):
        pg = DirectoryPage()
        pg.flowables.append('CURRENT_PAGE_NUMBER')
        tableData = [brokenDownTables[:2]]
        if len(tableData[0]) == 1:
            tableData[0].append([])
        tableData[0].insert(1,[])
        brokenDownTables = brokenDownTables[2:]
        pg.flowables.append(Table(data = tableData,
                                  colWidths = [STANDARD_TABLE_WIDTH, STANDARD_MARGIN, STANDARD_TABLE_WIDTH],
                                  style = TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'),])))
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

