# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import Image, PageBreak, \
    Paragraph, Table, TableStyle, Spacer
from reportlab.platypus.flowables import HRFlowable, KeepInFrame

from .PDFStyles import styles
from .DirectoryPage import DirectoryPage

STANDARD_MARGIN = 0.25 * inch
HALF_PAGE_WIDTH = landscape(letter)[0]/2
STANDARD_FRAME_WIDTH = HALF_PAGE_WIDTH - 2 * STANDARD_MARGIN
STANDARD_FRAME_HEIGHT = landscape(letter)[1] - 2 * STANDARD_MARGIN
STANDARD_TABLE_WIDTH = (STANDARD_FRAME_WIDTH - STANDARD_MARGIN) / 2
MAP_PAGE_WIDTH = HALF_PAGE_WIDTH - STANDARD_MARGIN

CHURCH_FLOW_FOR_SIZING = Paragraph('For Church Use Only', styles['DaveFooter'])
FOOTER_ROOM = CHURCH_FLOW_FOR_SIZING.wrap(
    STANDARD_FRAME_WIDTH, STANDARD_FRAME_HEIGHT)[1] + \
    CHURCH_FLOW_FOR_SIZING.getSpaceBefore()
PAGE_HDR_FLOW_FOR_SIZING = Paragraph('Page 1', styles['DaveHeaderLeft'])
HEADER_ROOM = PAGE_HDR_FLOW_FOR_SIZING.wrap(
    STANDARD_FRAME_WIDTH, STANDARD_FRAME_HEIGHT)[1] + \
    PAGE_HDR_FLOW_FOR_SIZING.getSpaceBefore()

STANDARD_TABLE_HEIGHT = STANDARD_FRAME_HEIGHT - FOOTER_ROOM - HEADER_ROOM
STANDARD_MAP_HEIGHT = STANDARD_FRAME_HEIGHT - HEADER_ROOM


def get_maps_pages(app_handle, maps, membershipList, debug):
    pages = []
    maps.annotate_insets()
    for one_map in maps.pages:
        if one_map.size == 'small':
            dir_page = DirectoryPage()
            dir_page.flowables.append('CURRENT_PAGE_NUMBER')
            dir_page.flowables.append(Image(one_map.get_map(),
                                            width=MAP_PAGE_WIDTH,
                                            height=STANDARD_MAP_HEIGHT,
                                            kind='proportional'))
            pages.append(dir_page)
        if one_map.size == 'large':
            dir_page = DirectoryPage(rightPadding=0)
            dir_page.flowables.append('CURRENT_PAGE_NUMBER')
            dir_page.flowables.append(Image(one_map.get_map_half('left'),
                                            width=MAP_PAGE_WIDTH,
                                            height=STANDARD_MAP_HEIGHT,
                                            kind='proportional'))
            pages.append(dir_page)
            dir_page = DirectoryPage(leftPadding=0)
            dir_page.flowables.append('CURRENT_PAGE_NUMBER')
            dir_page.flowables.append(Image(one_map.get_map_half('right'),
                                            width=MAP_PAGE_WIDTH,
                                            height=STANDARD_MAP_HEIGHT,
                                            kind='proportional'))
            pages.append(dir_page)
    return pages


def make_member_dwellings_dict(dwellingsHandle, membershipList):
    dwellings_dict = {}
    for household in membershipList:
        index = dwellingsHandle.find_map_index_for_household(household)
        if index != None:
            dwellings_dict[index - 1] = dwellings_dict.get(index - 1, []) + \
                [household]
    return dwellings_dict


def get_maps_lookup_pages(app_handle, dwellingsHandle, membershipList, debug):
    church_use_text = '%s - For Church Use Only' % app_handle.unit_unitname
    church_flowable = Paragraph(church_use_text, styles['DaveFooter'])
    pages = []
    mbr_dwellings_dict = make_member_dwellings_dict(dwellingsHandle,
                                                    membershipList)
    table_data = [['#', 'Name']]
    ofstream = open(u'SortedByNumber.csv', u'w')
    # we are confident that this has already been sorted by map index
    for dwell_counter in xrange(len(dwellingsHandle.dwellingList)):
        dwelling = dwellingsHandle.dwellingList[dwell_counter]
        print "Dwelling: %s %s" % (dwelling.mapIndex, dwelling)
        mbrs = mbr_dwellings_dict.get(dwell_counter, [])
        print "Members: %s" % str(mbrs)
        mbr_str = '\n'.join(
            ['%s%s' % ('' if x.isMember else '*', x.coupleName) for x in mbrs])
        table_data.append([dwell_counter + 1, mbr_str])
        ofstream.write(
            '"%s","%s","%s"\n' % (dwell_counter + 1, dwelling.Street,
                                  mbr_str.replace(u'\n', u'')))
    ofstream.close()
    map_idx_width = 0.3 * inch
    name_width = STANDARD_TABLE_WIDTH - map_idx_width
    this_tbl = Table(
        data=table_data,
        colWidths=[map_idx_width, name_width],
        style=TableStyle([('GRID', (0, 0), (-1, -1), 0.25, colors.black),
                          ('FONTSIZE', (0, 0), (-1, -1), 8),
                          ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                          ('ALIGNMENT', (0, 0), (0, -1), 'CENTRE'),
                         ]),
        repeatRows=1)
    result = this_tbl.split(STANDARD_TABLE_WIDTH, STANDARD_TABLE_HEIGHT)
    brokenDownTables = []
    while len(result) == 2:
        brokenDownTables.append(result[0])
        result = result[1].split(STANDARD_TABLE_WIDTH, STANDARD_TABLE_HEIGHT)
    brokenDownTables.append(result[0])
    while len(brokenDownTables):
        pg = DirectoryPage()
        pg.flowables.append('CURRENT_PAGE_NUMBER')
        table_data = [brokenDownTables[:2]]
        if len(table_data[0]) == 1:
            table_data[0].append([])
        table_data[0].insert(1, [])
        brokenDownTables = brokenDownTables[2:]
        col_widths = [STANDARD_TABLE_WIDTH, STANDARD_MARGIN,
                      STANDARD_TABLE_WIDTH]
        pg.flowables.append(
            Table(data=table_data,
                  colWidths=col_widths,
                  style=TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),])))
        pg.flowables.append(church_flowable)
        pages.append(pg)
    return pages


def PrepareFiller(title, pageCounter):
    line_space_list = []
    for counter in xrange(30):
        line_space_list.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                      height=.25 * inch))
        line_space_list.append(HRFlowable(width="90%", thickness=1,
                                          lineCap='square',
                                          color=colors.black))
    return_list = [Paragraph(text="%s Page %d" % (title, pageCounter),
                             style=styles['Subtitle']),
                   KeepInFrame(maxWidth=STANDARD_FRAME_WIDTH,
                               maxHeight=7.5 * inch,
                               content=line_space_list,
                               mode='truncate'),
                   PageBreak()]
    return return_list
