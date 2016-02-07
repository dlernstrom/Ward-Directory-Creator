# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, Table, TableStyle

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


def get_maps_pages(maps):
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
            dir_page = DirectoryPage(right_padding=0)
            dir_page.flowables.append('CURRENT_PAGE_NUMBER')
            dir_page.flowables.append(Image(one_map.get_map_half('left'),
                                            width=MAP_PAGE_WIDTH,
                                            height=STANDARD_MAP_HEIGHT,
                                            kind='proportional'))
            pages.append(dir_page)
            dir_page = DirectoryPage(left_padding=0)
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


def get_maps_lookup_pages(app_handle, dwellingsHandle, membership_list):
    church_use_text = '%s - For Church Use Only' % app_handle.unit_unitname
    church_flowable = Paragraph(church_use_text, styles['DaveFooter'])
    pages = []
    mbr_dwellings_dict = make_member_dwellings_dict(dwellingsHandle,
                                                    membership_list)
    table_data = [['#', 'Name']]
    # we are confident that this has already been sorted by map index
    for dwell_counter in xrange(len(dwellingsHandle.dwellingList)):
        dwelling = dwellingsHandle.dwellingList[dwell_counter]
        print "Dwelling: %s %s" % (dwelling.mapIndex, dwelling)
        mbrs = mbr_dwellings_dict.get(dwell_counter, [])
        print "Members: %s" % str(mbrs)
        mbr_str = '\n'.join(
            ['%s%s' % ('' if x.isMember else '*', x.coupleName) for x in mbrs])
        table_data.append([dwell_counter + 1, mbr_str])
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
    broken_down_tbls = []
    while len(result) == 2:
        broken_down_tbls.append(result[0])
        result = result[1].split(STANDARD_TABLE_WIDTH, STANDARD_TABLE_HEIGHT)
    broken_down_tbls.append(result[0])
    while len(broken_down_tbls):
        dir_page = DirectoryPage()
        dir_page.flowables.append('CURRENT_PAGE_NUMBER')
        table_data = [broken_down_tbls[:2]]
        if len(table_data[0]) == 1:
            table_data[0].append([])
        table_data[0].insert(1, [])
        broken_down_tbls = broken_down_tbls[2:]
        col_widths = [STANDARD_TABLE_WIDTH, STANDARD_MARGIN,
                      STANDARD_TABLE_WIDTH]
        dir_page.flowables.append(
            Table(data=table_data,
                  colWidths=col_widths,
                  style=TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),])))
        dir_page.flowables.append(church_flowable)
        pages.append(dir_page)
    return pages
