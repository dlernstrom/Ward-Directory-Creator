# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import Preformatted, Image, Paragraph, Table, \
    TableStyle, Spacer
from reportlab.platypus.flowables import KeepInFrame
from reportlab.pdfgen.canvas import Canvas

from .PDFStyles import styles
from .TextOnImage import TextOnImage
from .DirectoryPage import DirectoryPage

STANDARD_MARGIN = 0.25 * inch
HALF_PAGE_WIDTH = landscape(letter)[0] / 2
STANDARD_FRAME_WIDTH = HALF_PAGE_WIDTH - 2 * STANDARD_MARGIN
STANDARD_FRAME_HEIGHT = landscape(letter)[1] - 2 * STANDARD_MARGIN


def get_missing_text(app_handle):
    if not app_handle.missing_missing_name:
        return ''
    contact_name = app_handle.missing_missing_name
    comma_index = contact_name.index(',')
    first_name = contact_name[comma_index + 2:]
    last_name = contact_name[:comma_index]
    contact_name = first_name + ' ' + last_name
    return "Please contact %s to have your photograph added" % contact_name


def get_listing_pages(app_handle, membershipList, debug):
    image_dir = app_handle.file_images_directory

    #Here I start adding family flowables
    familyFlowables = []
    numberOfMembers = 0
    numberOfHouseholds = 0
    for household in membershipList:
        if not household.isMember:
            continue
        numberOfHouseholds += 1
        numberOfMembers += len(household.family)
        familyFlowables.append(
            tableize_family(app_handle, image_dir, household, debug))
        if debug:
            print str(numberOfHouseholds), household.coupleName
            print '------------------------------------------'
    familyFlowables.append(Paragraph('%d Families' % numberOfHouseholds,
                                     styles['DaveFooter']))
    familyFlowables.append(Paragraph('%d Individuals' % numberOfMembers,
                                     styles['DaveFooter']))
    # end aggregating family flowables

    pages = paginate_listings(app_handle, familyFlowables, debug)
    return pages


def paginate_listings(app_handle, familyFlowables, debug):
    pdf_TEST = Canvas("DIRECTORY_TEST.pdf", pagesize=landscape(letter))
    churchFlowable = Paragraph(
        '%s - For Church Use Only' % app_handle.unit_unitname,
        styles['DaveFooter'])
    FooterRoom = churchFlowable.wrap(
        STANDARD_FRAME_WIDTH, STANDARD_FRAME_HEIGHT)[1] + \
        churchFlowable.getSpaceBefore()
    pageHeaderFlowableForSizing = Paragraph('Page 1', styles['DaveHeaderLeft'])
    headerRoom = pageHeaderFlowableForSizing.wrap(STANDARD_FRAME_WIDTH,
                                                  STANDARD_FRAME_HEIGHT)[1] + \
        pageHeaderFlowableForSizing.getSpaceBefore()

    pages = []
    pg = DirectoryPage()
    fm = pg.get_frame(debug=debug)
    carryOver = None
    tmpList = []
    for fam in familyFlowables:
        if len(pg.flowables) == 0:
            fm.add(churchFlowable, pdf_TEST)
            fm.add(Paragraph('Page ' + str(pdf_TEST.getPageNumber() - 1),
                             styles['DaveHeaderLeft']), pdf_TEST)
            pg.flowables.append('CURRENT_PAGE_NUMBER')

        if carryOver:
            fm.add(carryOver, pdf_TEST)
            #pg.flowables.append(carryOver)
            tmpList.append(carryOver)
            carryOver = None

        if fm.add(fam, pdf_TEST):
            #pg.flowables.append(fam)
            tmpList.append(fam)
            continue
        carryOver = fam

        content = tmpList + [Spacer(width=STANDARD_FRAME_WIDTH,
                                    height=9 * inch)]
        pg.flowables.append(
            KeepInFrame(
                maxWidth=STANDARD_FRAME_WIDTH,
                maxHeight=STANDARD_FRAME_HEIGHT - FooterRoom - headerRoom,
                content=content,
                mode='truncate'))
        pg.flowables.append(churchFlowable)

        pages.append(pg)
        # start a new test pdf page
        pdf_TEST.showPage()

        pg = DirectoryPage()
        fm = pg.get_frame(debug=debug)
        tmpList = []
    if carryOver:
        fm.add(carryOver, pdf_TEST)
        tmpList.append(carryOver)
        #pg.flowables.append(carryOver)

    if len(tmpList):
        content = tmpList + [Spacer(width=STANDARD_FRAME_WIDTH,
                                    height=9 * inch)]
        pg.flowables.append(
            KeepInFrame(maxWidth=STANDARD_FRAME_WIDTH,
                        maxHeight=STANDARD_FRAME_HEIGHT - FooterRoom - headerRoom,
                        content=content,
                        mode='truncate'))
        pg.flowables.append(churchFlowable)
        pages.append(pg)
        pdf_TEST.showPage()
    if debug:
        pdf_TEST.save()
    return pages


def tableize_family(app_handle, ImageDirectory, household, debug):
    Family = []
    if debug:
        print '%s Family' % household.surname
        print "Number of Members: %d" % len(household.family)
    # minimum number of rows a family will take up
    # This is calculated by surname row, address row, HoH, filler
    Rows = 3
    if 1 + len(household.family) > Rows:
        Rows = 1 + len(household.family)

    #Get me a blank populated table
    data = []
    for rowCounter in xrange(Rows):
        data.append([None, None, None, None, None])

    #Add the obvious entries
    data[0][0] = Preformatted(household.surname.upper(), styles['DaveBold'])
    data[0][3] = Preformatted(household.familyAddress + '\n' + household.familyEmail.email_addy, styles['DaveHeading'])
    data[0][4] = Preformatted(household.familyPhone.phone_formatted + '\n' + str(household.mapIndexString), styles['DaveBoldSmall'])

    expectedName = household.expectedPhotoName
    picturePath = ImageDirectory + os.sep + expectedName
    if os.path.isfile(picturePath):
        FamilyPicture = Image(picturePath,
                              width=1.5 * inch,
                              height=1.125 * inch,
                              kind='proportional')
        if debug:
            print picturePath
    else:
        logging.debug(expectedName)
        FamilyPictureBase = Image(r'Engine\Missing.jpg',
                                  width=1.5 * inch,
                                  height=1.125 * inch,
                                  kind='proportional')
        MissingImageText = Paragraph(text=get_missing_text(app_handle),
                                     style=styles['TextOnImage'])
        FamilyPicture = TextOnImage(P=MissingImageText, I=FamilyPictureBase,
                                    xpad=0, ypad=0.3 * inch, side='center')

    #########NOTICE THAT SPAN IS WRITTEN BASS ACKWARDS WITH COL,ROW
    TheTableStyle = TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 3),
                                ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                                ('TOPPADDING', (1, 0), (-1, -1), 0),
                                ('SPAN', (0, 0), (2, 0)),
                                ('VALIGN', (0, 0), (0, 0), 'TOP'),
                                ('VALIGN', (4, 0), (4, 0), 'TOP'),
                                ('BACKGROUND', (0, 0), (-1, 0), 'papayawhip'),
                                ('LINEBELOW', (0, 0), (-1, 0), 0.25, colors.gray)])
    if debug:
        TheTableStyle.add('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)
        TheTableStyle.add('BOX', (0, 0), (-1, -1), .25, colors.black)
    ImageStyle = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                             ('LEFTPADDING', (0, 0), (-1, -1), 0),
                             ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                             ('LEADING', (0, 0), (-1, -1), 0)])
    CombinedStyle = TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                ('LINEBELOW', (0, 0), (-1, -1), 1.0, colors.black),
                                ('LINEABOVE', (0, 0), (-1, -1), 1.0, colors.black),
                                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                                ('TOPPADDING', (0, 0), (-1, -1), 0),
                                ('LEADING', (0, 0), (-1, -1), 0),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTSIZE', (0, 0), (-1, -1), 0)])
    if debug:
        CombinedStyle.add('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)
        CombinedStyle.add('BOX', (0, 0), (-1, -1), 0.25, colors.black)

    #Add the family Members
    CurrentRow = 0
    if debug:
        print "Family: %s" % str(Family)
    for member in household.family:
        CurrentRow += 1
        if member.is_parent:
            Column = 1
            cellStyle = styles['DaveBoldSmall']
        else:
            Column = 2
            cellStyle = styles['DaveHeading']
        data[CurrentRow][Column] = Preformatted(member.nameCSV,
                                                cellStyle)
        data[CurrentRow][3] = Preformatted(member.email.email_addy,
                                           styles['DaveHeading'])
        data[CurrentRow][4] = Preformatted(member.phone.phone_formatted,
                                           styles['DaveHeading'])
    TextTable = Table(data, [.125 * inch, .125 * inch, 0.9 * inch, 1.45 * inch, .8 * inch])
    TextTable.setStyle(TheTableStyle)
    ImageTable = Table([[FamilyPicture]])
    ImageTable.setStyle(ImageStyle)
    CombinedTableData = [[TextTable, ImageTable]]
    MasterTable = Table(CombinedTableData, ['*', 1.6 * inch])
    MasterTable.setStyle(CombinedStyle)
    return MasterTable
