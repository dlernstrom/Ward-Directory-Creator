# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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


def get_missing_text(missing_name):
    if not missing_name:
        return ''
    comma_index = missing_name.index(',')
    first_name = missing_name[comma_index + 2:]
    last_name = missing_name[:comma_index]
    missing_name = first_name + ' ' + last_name
    return "Please contact %s to have your photograph added" % missing_name


def get_missing_img_pic(missing_name):
    background = Image(r'Engine\Missing.jpg',
                       width=1.5 * inch,
                       height=1.125 * inch,
                       kind='proportional')
    foreground_txt = Paragraph(text=get_missing_text(missing_name),
                               style=styles['TextOnImage'])
    return TextOnImage(P=foreground_txt, I=background,
                       xpad=0, ypad=0.3 * inch, side='center')


def get_listing_pages(app_handle, membership_list, debug):
    image_dir = app_handle.file_images_directory

    fam_flowables = []
    member_count = 0
    household_count = 0
    for household in membership_list:
        if not household.isMember:
            continue
        household_count += 1
        member_count += len(household.family)
        fam_flowables.append(
            tableize_family(app_handle, image_dir, household, debug))
        if debug:
            print str(household_count), household.coupleName
            print '------------------------------------------'
    fam_flowables.append(Paragraph('%d Families' % household_count,
                                   styles['DaveFooter']))
    fam_flowables.append(Paragraph('%d Individuals' % member_count,
                                   styles['DaveFooter']))

    return paginate_listings(app_handle, fam_flowables, debug)


def paginate_listings(app_handle, familyFlowables, debug):
    test_pdf = Canvas("DIRECTORY_TEST.pdf", pagesize=landscape(letter))
    church_flowable = Paragraph(
        '%s - For Church Use Only' % app_handle.unit_unitname,
        styles['DaveFooter'])
    footer_room = church_flowable.wrap(
        STANDARD_FRAME_WIDTH, STANDARD_FRAME_HEIGHT)[1] + \
        church_flowable.getSpaceBefore()
    header_flow_for_sizing = Paragraph('Page 1', styles['DaveHeaderLeft'])
    header_room = header_flow_for_sizing.wrap(STANDARD_FRAME_WIDTH,
                                              STANDARD_FRAME_HEIGHT)[1] + \
        header_flow_for_sizing.getSpaceBefore()

    pages = []
    dir_page = DirectoryPage()
    frame = dir_page.get_frame(debug=debug)
    carry_over = None
    temp_list = []
    for fam in familyFlowables:
        if len(dir_page.flowables) == 0:
            frame.add(church_flowable, test_pdf)
            frame.add(Paragraph('Page ' + str(test_pdf.getPageNumber() - 1),
                                styles['DaveHeaderLeft']), test_pdf)
            dir_page.flowables.append('CURRENT_PAGE_NUMBER')

        if carry_over:
            frame.add(carry_over, test_pdf)
            temp_list.append(carry_over)
            carry_over = None

        if frame.add(fam, test_pdf):
            temp_list.append(fam)
            continue
        carry_over = fam

        content = temp_list + [Spacer(width=STANDARD_FRAME_WIDTH,
                                      height=9 * inch)]
        dir_page.flowables.append(
            KeepInFrame(
                maxWidth=STANDARD_FRAME_WIDTH,
                maxHeight=STANDARD_FRAME_HEIGHT - footer_room - header_room,
                content=content,
                mode='truncate'))
        dir_page.flowables.append(church_flowable)

        pages.append(dir_page)
        # start a new test pdf page
        test_pdf.showPage()

        dir_page = DirectoryPage()
        frame = dir_page.get_frame(debug=debug)
        temp_list = []
    if carry_over:
        frame.add(carry_over, test_pdf)
        temp_list.append(carry_over)
        #pg.flowables.append(carryOver)

    if len(temp_list):
        content = temp_list + [Spacer(width=STANDARD_FRAME_WIDTH,
                                      height=9 * inch)]
        dir_page.flowables.append(
            KeepInFrame(
                maxWidth=STANDARD_FRAME_WIDTH,
                maxHeight=STANDARD_FRAME_HEIGHT - footer_room - header_room,
                content=content,
                mode='truncate'))
        dir_page.flowables.append(church_flowable)
        pages.append(dir_page)
        test_pdf.showPage()
    if debug:
        test_pdf.save()
    return pages


def tableize_family(app_handle, ImageDirectory, household, debug):
    family = []
    if debug:
        print '%s Family' % household.surname
        print "Number of Members: %d" % len(household.family)
    # minimum number of rows a family will take up
    # This is calculated by surname row, address row, HoH, filler
    rows = 3
    if 1 + len(household.family) > rows:
        rows = 1 + len(household.family)

    # Get me a blank populated table
    data = []
    for row_counter in xrange(rows):
        data.append([None, None, None, None, None])

    # Add the obvious entries
    data[0][0] = Preformatted(household.surname.upper(), styles['DaveBold'])
    addy_data = '%s\n%s' % (household.familyAddress,
                            household.familyEmail.email_addy)
    data[0][3] = Preformatted(addy_data, styles['DaveHeading'])
    phone_map_index = '%s\n%s' % (household.familyPhone.phone_formatted,
                                  str(household.mapIndexString))
    data[0][4] = Preformatted(phone_map_index, styles['DaveBoldSmall'])

    picture_path = os.path.join(ImageDirectory, household.expectedPhotoName)
    if os.path.isfile(picture_path):
        family_pic = Image(picture_path,
                           width=1.5 * inch,
                           height=1.125 * inch,
                           kind='proportional')
        if debug:
            print picture_path
    else:
        family_pic = get_missing_img_pic(app_handle.missing_missing_name)

    #########NOTICE THAT SPAN IS WRITTEN BASS ACKWARDS WITH COL,ROW
    table_style = TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (1, 0), (-1, -1), 0),
        ('SPAN', (0, 0), (2, 0)),
        ('VALIGN', (0, 0), (0, 0), 'TOP'),
        ('VALIGN', (4, 0), (4, 0), 'TOP'),
        ('BACKGROUND', (0, 0), (-1, 0), 'papayawhip'),
        ('LINEBELOW', (0, 0), (-1, 0), 0.25, colors.gray)])
    if debug:
        table_style.add('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)
        table_style.add('BOX', (0, 0), (-1, -1), .25, colors.black)
    img_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('LEFTPADDING', (0, 0), (-1, -1), 0),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                            ('LEADING', (0, 0), (-1, -1), 0)])
    combined_style = TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
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
        combined_style.add('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)
        combined_style.add('BOX', (0, 0), (-1, -1), 0.25, colors.black)

    #Add the family Members
    current_row = 0
    if debug:
        print "Family: %s" % str(family)
    for member in household.family:
        current_row += 1
        if member.is_parent:
            column = 1
            cell_style = styles['DaveBoldSmall']
        else:
            column = 2
            cell_style = styles['DaveHeading']
        data[current_row][column] = Preformatted(member.nameCSV, cell_style)
        data[current_row][3] = Preformatted(member.email.email_addy,
                                            styles['DaveHeading'])
        data[current_row][4] = Preformatted(member.phone.phone_formatted,
                                            styles['DaveHeading'])
    text_table = Table(data, [.125 * inch, .125 * inch, 0.9 * inch,
                              1.45 * inch, .8 * inch])
    text_table.setStyle(table_style)
    image_table = Table([[family_pic]])
    image_table.setStyle(img_style)
    combined_table = [[text_table, image_table]]
    master_table = Table(combined_table, ['*', 1.6 * inch])
    master_table.setStyle(combined_style)
    return master_table
