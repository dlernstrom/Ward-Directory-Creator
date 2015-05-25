# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import time

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.flowables import KeepInFrame, HRFlowable

from DirectoryPage import DirectoryPage
from PDFStyles import styles

STANDARD_MARGIN = 0.25 * inch
STANDARD_FRAME_WIDTH = landscape(letter)[0]/2 - 2 * STANDARD_MARGIN


def get_callings_data(configData):
    # Return a list of dictionaries of the positions ordered correctly
    # TODO: This should happen by my parent...
    # I am the customer and should get it how I want it already
    role_lst = ['bish', 'first', 'second', 'exec', 'clerk', 'fin', 'mem', "NULL",
                'hp', 'eq', 'rs', 'ym', 'yw', 'primary', 'ss', "NULL",
                'wml', 'act', 'news', 'miss']
    role_dict = {'bish':	'Bishop',
                 'first':	'1st Counselor',
                 'second':	'2nd Counselor',
                 'exec':	'Executive Secretary',
                 'clerk':	'Ward Clerk',
                 'fin':		'Financial Clerk',
                 'mem':		'Membership Clerk',
                 'hp':		'High Priest Group Leader',
                 'eq':		'Elders Quorum President',
                 'rs':		'Relief Society President',
                 'ym':		"Young Men's President",
                 'yw':		"Young Women's President",
                 'primary':	'Primary President',
                 'ss':		'Sunday School President',
                 'wml':		'Ward Mission Leader',
                 'act':		'Activities Committee Chair',
                 'news':	'Ward Newsletter',
                 'dir':		'Ward Directory',
                 "NULL":	'',
                 'miss':	'Missionaries'}
    leadership_lst = []
    for role in role_lst:
        if role == 'miss':
            leadership_lst.append({"Role":	'',
                                   "Name":	role_dict[role],
                                   "Phone":	'(435) 232-7293'})
        try:
            if configData['leadership.' + role + 'disp'] == '1':
                leadership_lst.append({"Role":	role_dict[role],
                                       "Name":	configData['leadership.' + role + 'name'],
                                       "Phone":	configData['leadership.' + role + 'phone']})
            else:
                leadership_lst.append({"Role":	" ",
                                       "Name":	" ",
                                       "Phone":	" "})
                leadership_lst.append({"Role":	" ",
                                       "Name":	" ",
                                       "Phone":	" "})
        except KeyError:
            leadership_lst.append({"Role":	" ",
                                   "Name":	" ",
                                   "Phone":	" "})
            leadership_lst.append({"Role":	" ",
                                   "Name":	" ",
                                   "Phone":	" "})
    return leadership_lst


def get_block_data(configData):
    block_data = []
    block_time_format = '%I:%M %p'
    if configData['block.displaysac']:
        sac_time = time.strptime(configData['block.sacstart'],
                                 block_time_format)
        block_data.append([sac_time, "Sacrament Meeting"])
    if configData['block.displayss']:
        ss_time = time.strptime(configData['block.ssstart'], block_time_format)
        block_data.append([ss_time, "Sunday School"])
    if configData['block.display_pr_rs']:
        pr_rs_time = time.strptime(configData['block.pr_rs_start'],
                                   block_time_format)
        block_data.append([pr_rs_time, "Priesthood / Relief Society"])
    block_data.sort()
    for mtg in block_data:
        mtg[0] = time.strftime(block_time_format, mtg[0])
        if mtg[0][0] == '0':
            mtg[0] = mtg[0][1:]

    pdf_block_data = []
    for mtg in block_data:
        pdf_block_data.append(
            [[Paragraph(text=mtg[0], style=styles['PrefixBaseRight'])],
             [Paragraph(text=mtg[1], style=styles['PrefixBaseLeft'])]])
    return pdf_block_data


def get_directory_prefix_pages(dict_data, debug):
    pages = []
    if debug:
        print "Here's the dictionary I received"
        print dict_data
    #Page 1 Data
    prefixPage = DirectoryPage()
    prefixPage.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                       height=1.5 * inch))
    prefixPage.flowables.append(
        Paragraph(text="<b>" + dict_data['unit.unitname'] + "</b>",
                  style=styles['DocumentTitle']))
    prefixPage.flowables.append(Paragraph(text="Member Directory",
                                          style=styles['Subtitle']))
    prefixPage.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                       height=2.0 * inch))
    prefixPage.flowables.append(
        Paragraph(text=dict_data['unit.stakename'],
                  style=styles['PrefixBase']))
    if 'bldg.addy1' in dict_data.keys():
        prefixPage.flowables.append(
            Paragraph(text=dict_data['bldg.addy1'],
                      style=styles['PrefixBase']))
    else:
        prefixPage.flowables.append(Paragraph(text='',
                                              style=styles['PrefixBase']))
    if 'bldg.addy2' in dict_data.keys():
        prefixPage.flowables.append(
            Paragraph(text=dict_data['bldg.addy2'],
                      style=styles['PrefixBase']))
    else:
        prefixPage.flowables.append(Paragraph(text='',
                                              style=styles['PrefixBase']))
    prefixPage.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                       height=2.0 * inch))
    CurrentDateString = datetime.date.today().strftime("%d %B %Y")
    prefixPage.flowables.append(
        Paragraph(text="Published: " + CurrentDateString,
                  style=styles['PrefixBase']))
    prefixPage.flowables.append(PageBreak())
    pages.append(prefixPage)

    #Page 2 Data
    prefixPage = DirectoryPage()
    prefixPage.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                       height=.125 * inch))
    sched = "<u>%s Meeting Schedule</u>" % datetime.date.today().strftime("%Y")
    prefixPage.flowables.append(
        Paragraph(text=sched, style=styles['Subtitle']))
    prefixPage.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                       height=.125 * inch))
    blockData = get_block_data(dict_data)
    TextTable = Table(blockData, [1.5 * inch, 3.0 * inch])
    if debug:
        TextTable.setStyle(
            TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), .25, colors.black)]))
    prefixPage.flowables.append(TextTable)
    prefixPage.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                       height=.125 * inch))
    if 'bldg.phone' in dict_data.keys():
        prefixPage.flowables.append(
            Paragraph(text="Office Phone: " + dict_data['bldg.phone'],
                      style=styles['PrefixBase']))
    else:
        prefixPage.flowables.append(Paragraph(text='',
                                              style=styles['PrefixBase']))
    prefixPage.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                       height=.125 * inch))
    prefixPage.flowables.append(
        HRFlowable(width="90%", thickness=1, lineCap='square',
                   color=colors.black))
    prefixPage.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                       height=.125 * inch))
    data = []

    for Position in get_callings_data(dict_data):
        data.append([[Paragraph(text=Position['Role'],
                                style=styles['RegTextR'])],
                     [Paragraph(text=Position['Name'],
                                style=styles['RegTextL'])],
                     [Paragraph(text=Position['Phone'],
                                style=styles['RegTextL'])]])
    TextTable = Table(data, [2.0 * inch, 1.8 * inch, 1.2 * inch])
    if debug:
        TextTable.setStyle(
            TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                        ('BOX', (0,0), (-1,-1), .25, colors.black),
                        ]))
    content = [TextTable,
               Spacer(width=STANDARD_FRAME_WIDTH, height=7.0 * inch)]
    prefixPage.flowables.append(KeepInFrame(maxWidth=STANDARD_FRAME_WIDTH,
                                            maxHeight=5.0 * inch,
                                            content=content,
                                            mode='truncate'))
    disc = """<b>This ward directory is to be used only for Church purposes
        and should not be copied without permission of the bishop
        or stake president.</b>
        """
    prefixPage.flowables.append(Paragraph(text=disc,
                                          style=styles['RegText']))
    prefixPage.flowables.append(PageBreak())
    if debug:
        for flow in prefixPage.flowables:
            if flow.__class__ in [Paragraph, Spacer]:
                flow._showBoundary = 1
    pages.append(prefixPage)
    return pages
