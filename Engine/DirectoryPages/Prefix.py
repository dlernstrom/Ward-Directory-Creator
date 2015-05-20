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
    #Return a list of dictionaries of the positions ordered correctly
    #TODO: This should happen by my parent... I am the customer and should get it how I want it already
    RoleList = ['bish', 'first', 'second', 'exec', 'clerk', 'fin', 'mem', "NULL",
                'hp', 'eq', 'rs', 'ym', 'yw', 'primary', 'ss', "NULL",
                'wml', 'act', 'news', 'miss']
    RoleDict = {'bish' :	'Bishop',
                'first' :	'1st Counselor',
                'second' :	'2nd Counselor',
                'exec' :	'Executive Secretary',
                'clerk' :	'Ward Clerk',
                'fin' :		'Financial Clerk',
                'mem' :		'Membership Clerk',
                'hp' :		'High Priest Group Leader',
                'eq' :		'Elders Quorum President',
                'rs' :		'Relief Society President',
                'ym' :		"Young Men's President",
                'yw' :		"Young Women's President",
                'primary' :	'Primary President',
                'ss':           'Sunday School President',
                'wml' :		'Ward Mission Leader',
                'act' :		'Activities Committee Chair',
                'news' :	'Ward Newsletter',
                'dir' :		'Ward Directory',
                "NULL" :	'',
                'miss':         'Missionaries'}
    LeadershipList = []
    for Role in RoleList:
        if Role == 'miss':
            LeadershipList.append({"Role" :		'',
                                   "Name" :		RoleDict[Role],
                                   "Phone" :	'(435) 232-7293'})
        try:
            if configData['leadership.' + Role + 'disp'] == '1':
                LeadershipList.append({"Role" :		RoleDict[Role],
                                       "Name" :		configData['leadership.' + Role + 'name'],
                                       "Phone" :	configData['leadership.' + Role + 'phone']})
            else:
                LeadershipList.append({"Role" :		" ",
                                       "Name" :		" ",
                                       "Phone" :	" "})
                LeadershipList.append({"Role" :		" ",
                                       "Name" :		" ",
                                       "Phone" :	" "})
        except KeyError:
            LeadershipList.append({"Role" :		" ",
                                   "Name" :		" ",
                                   "Phone" :	" "})
            LeadershipList.append({"Role" :		" ",
                                   "Name" :		" ",
                                   "Phone" :	" "})
    return LeadershipList


def get_block_data(configData):
    BlockData = []
    format = '%I:%M %p'
    if configData['block.displaysac']:
        BlockData.append([time.strptime(configData['block.sacstart'], format),
                          "Sacrament Meeting"])
    if configData['block.displayss']:
        BlockData.append([time.strptime(configData['block.ssstart'], format),
                          "Sunday School"])
    if configData['block.display_pr_rs']:
        BlockData.append([time.strptime(configData['block.pr_rs_start'], format),
                          "Priesthood / Relief Society"])
    BlockData.sort()
    for Mtg in BlockData:
        Mtg[0] = time.strftime(format, Mtg[0])
        if Mtg[0][0] == '0':
            Mtg[0] = Mtg[0][1:]

    myDisplayBlock = []
    for Mtg in BlockData:
        myDisplayBlock.append([[Paragraph(text = Mtg[0], style = styles['PrefixBaseRight'])],
                               [Paragraph(text = Mtg[1], style = styles['PrefixBaseLeft'])]])
    return myDisplayBlock


def get_directory_prefix_pages(dictionaryData, debug):
    pages = []
    if debug:
        print "Here's the dictionary I received"
        print dictionaryData
    #Page 1 Data
    prefixPage = DirectoryPage()
    prefixPage.flowables.append(Spacer(width = STANDARD_FRAME_WIDTH, height = 1.5 * inch))
    prefixPage.flowables.append(Paragraph(text = "<b>" + dictionaryData['unit.unitname'] + "</b>", style = styles['DocumentTitle']))
    prefixPage.flowables.append(Paragraph(text = "Member Directory", style = styles['Subtitle']))
    prefixPage.flowables.append(Spacer(width = STANDARD_FRAME_WIDTH, height = 2.0 * inch))
    prefixPage.flowables.append(Paragraph(text = dictionaryData['unit.stakename'], style = styles['PrefixBase']))
    if 'bldg.addy1' in dictionaryData.keys():
        prefixPage.flowables.append(Paragraph(text = dictionaryData['bldg.addy1'], style = styles['PrefixBase']))
    else:
        prefixPage.flowables.append(Paragraph(text = '', style = styles['PrefixBase']))
    if 'bldg.addy2' in dictionaryData.keys():
        prefixPage.flowables.append(Paragraph(text = dictionaryData['bldg.addy2'], style = styles['PrefixBase']))
    else:
        prefixPage.flowables.append(Paragraph(text = '', style = styles['PrefixBase']))
    prefixPage.flowables.append(Spacer(width = STANDARD_FRAME_WIDTH, height = 2.0 * inch))
    CurrentDateString = datetime.date.today().strftime("%d %B %Y")
    prefixPage.flowables.append(Paragraph(text = "Published: " + CurrentDateString, style = styles['PrefixBase']))
    prefixPage.flowables.append(PageBreak())
    pages.append(prefixPage)

    #Page 2 Data
    prefixPage = DirectoryPage()
    prefixPage.flowables.append(Spacer(width = STANDARD_FRAME_WIDTH, height = .125 * inch))
    prefixPage.flowables.append(Paragraph(text = "<u>%s Meeting Schedule</u>" % datetime.date.today().strftime("%Y"), style = styles['Subtitle']))
    prefixPage.flowables.append(Spacer(width = STANDARD_FRAME_WIDTH, height = .125 * inch))
    blockData = get_block_data(dictionaryData)
    TextTable = Table(blockData, [1.5 * inch, 3.0 * inch])
    if debug:
        TextTable.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                       ('BOX', (0,0), (-1,-1), .25, colors.black)]))
    prefixPage.flowables.append(TextTable)
    prefixPage.flowables.append(Spacer(width = STANDARD_FRAME_WIDTH, height = .125 * inch))
    if 'bldg.phone' in dictionaryData.keys():
        prefixPage.flowables.append(Paragraph(text = "Office Phone: " + dictionaryData['bldg.phone'], style = styles['PrefixBase']))
    else:
        prefixPage.flowables.append(Paragraph(text = '', style = styles['PrefixBase']))
    prefixPage.flowables.append(Spacer(width = STANDARD_FRAME_WIDTH, height = .125 * inch))
    prefixPage.flowables.append(HRFlowable(width = "90%", thickness = 1, lineCap= 'square', color = colors.black))
    prefixPage.flowables.append(Spacer(width = STANDARD_FRAME_WIDTH, height = .125 * inch))
    data = []

    for Position in get_callings_data(dictionaryData):
        data.append([[Paragraph(text = Position['Role'], style = styles['RegTextR'])],
                     [Paragraph(text = Position['Name'], style = styles['RegTextL'])],
                     [Paragraph(text = Position['Phone'], style = styles['RegTextL'])]])
    TextTable = Table(data, [2.0 * inch, 1.8 * inch, 1.2 * inch])
    if debug:
        TextTable.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                       ('BOX', (0,0), (-1,-1), .25, colors.black),
                                       ]))
    prefixPage.flowables.append(KeepInFrame(maxWidth = STANDARD_FRAME_WIDTH,
                                            maxHeight = 5.0 * inch,
                                            content = [TextTable,
                                                       Spacer(width = STANDARD_FRAME_WIDTH, height = 7.0 * inch)],
                                            mode = 'truncate'))
    Disclaimer = """This ward directory is to be used only for Church purposes
                                             and should not be copied without permission of the bishop
                                             or stake president.
                                             """
    prefixPage.flowables.append(Paragraph(text = "<b>" + Disclaimer + "</b>", style = styles['RegText']))
    prefixPage.flowables.append(PageBreak())
    if debug:
        for aFlowable in prefixPage.flowables:
            if aFlowable.__class__ is Paragraph or aFlowable.__class__ is Spacer:
                aFlowable._showBoundary = 1
    pages.append(prefixPage)
    return pages
