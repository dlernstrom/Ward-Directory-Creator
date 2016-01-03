# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import time

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.flowables import KeepInFrame, HRFlowable

from Engine.constants import role_lst, role_dict
from .DirectoryPage import DirectoryPage
from .PDFStyles import styles

STANDARD_MARGIN = 0.25 * inch
STANDARD_FRAME_WIDTH = landscape(letter)[0]/2 - 2 * STANDARD_MARGIN


def get_callings_data(app_handle):
    """Return a list of dictionaries of the positions ordered correctly"""
    # TODO: This should happen by my parent...
    # I am the customer and should get it how I want it already
    leadership_lst = []
    for role in role_lst:
        if role == 'miss':
            leadership_lst.append({"Role": '',
                                   "Name": role_dict[role],
                                   "Phone": '(435) 232-7293'})
        try:
            if getattr(app_handle, 'leadership_' + role + 'disp') == '1':
                leadership_lst.append(
                    {"Role": role_dict[role],
                     "Name": getattr(app_handle, 'leadership_' + role + 'name'),
                     "Phone": getattr(app_handle, 'leadership_' + role + 'phone')})
            else:
                leadership_lst.append({"Role": " ",
                                       "Name": " ",
                                       "Phone": " "})
                leadership_lst.append({"Role": " ",
                                       "Name": " ",
                                       "Phone": " "})
        except KeyError:
            leadership_lst.append({"Role": " ",
                                   "Name": " ",
                                   "Phone": " "})
            leadership_lst.append({"Role": " ",
                                   "Name": " ",
                                   "Phone": " "})
    return leadership_lst


def get_block_data(app_handle):
    block_data = []
    block_time_format = '%I:%M %p'
    if app_handle.block_displaysac:
        sac_time = time.strptime(app_handle.block_sacstart,
                                 block_time_format)
        block_data.append([sac_time, "Sacrament Meeting"])
    if app_handle.block_displayss:
        ss_time = time.strptime(app_handle.block_ssstart, block_time_format)
        block_data.append([ss_time, "Sunday School"])
    if app_handle.block_display_pr_rs:
        pr_rs_time = time.strptime(app_handle.block_pr_rs_start,
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


def get_directory_prefix_pages(app_handle, debug):
    pages = []
    pages.append(make_title_page(app_handle))

    #Page 2 Data
    prefix_page = DirectoryPage()
    prefix_page.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                        height=.125 * inch))
    sched = "<u>%s Meeting Schedule</u>" % datetime.date.today().strftime("%Y")
    prefix_page.flowables.append(
        Paragraph(text=sched, style=styles['Subtitle']))
    prefix_page.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                        height=.125 * inch))
    text_tbl = Table(get_block_data(app_handle), [1.5 * inch, 3.0 * inch])
    if debug:
        text_tbl.setStyle(
            TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -1), .25, colors.black)]))
    prefix_page.flowables.append(text_tbl)
    prefix_page.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                        height=.125 * inch))
    if app_handle.bldg_phone:
        prefix_page.flowables.append(
            Paragraph(text="Office Phone: " + app_handle.bldg_phone,
                      style=styles['PrefixBase']))
    else:
        prefix_page.flowables.append(Paragraph(text='',
                                               style=styles['PrefixBase']))
    prefix_page.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                        height=.125 * inch))
    prefix_page.flowables.append(
        HRFlowable(width="90%", thickness=1, lineCap='square',
                   color=colors.black))
    prefix_page.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                        height=.125 * inch))
    data = []

    for position in get_callings_data(app_handle):
        data.append([[Paragraph(text=position['Role'],
                                style=styles['RegTextR'])],
                     [Paragraph(text=position['Name'],
                                style=styles['RegTextL'])],
                     [Paragraph(text=position['Phone'],
                                style=styles['RegTextL'])]])
    text_tbl = Table(data, [2.0 * inch, 1.8 * inch, 1.2 * inch])
    if debug:
        text_tbl.setStyle(
            TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -1), .25, colors.black),
                       ]))
    content = [text_tbl,
               Spacer(width=STANDARD_FRAME_WIDTH, height=7.0 * inch)]
    prefix_page.flowables.append(KeepInFrame(maxWidth=STANDARD_FRAME_WIDTH,
                                             maxHeight=5.0 * inch,
                                             content=content,
                                             mode='truncate'))
    disc = """<b>This ward directory is to be used only for Church purposes
        and should not be copied without permission of the bishop
        or stake president.</b>
        """
    prefix_page.flowables.append(Paragraph(text=disc,
                                           style=styles['RegText']))
    prefix_page.flowables.append(PageBreak())
    if debug:
        for flow in prefix_page.flowables:
            if flow.__class__ in [Paragraph, Spacer]:
                flow._showBoundary = 1
    pages.append(prefix_page)
    return pages


def make_title_page(app_handle):
    # Page 1 Data
    prefix_page = DirectoryPage()
    prefix_page.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                        height=1.5 * inch))
    prefix_page.flowables.append(
        Paragraph(text="<b>" + app_handle.unit_unitname + "</b>",
                  style=styles['DocumentTitle']))
    prefix_page.flowables.append(Paragraph(text="Member Directory",
                                           style=styles['Subtitle']))
    prefix_page.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                        height=2.0 * inch))
    prefix_page.flowables.append(
        Paragraph(text=app_handle.unit_stakename,
                  style=styles['PrefixBase']))
    if app_handle.bldg_addy1:
        prefix_page.flowables.append(
            Paragraph(text=app_handle.bldg_addy1,
                      style=styles['PrefixBase']))
    else:
        prefix_page.flowables.append(
            Paragraph(text='', style=styles['PrefixBase']))
    if app_handle.bldg_addy2:
        prefix_page.flowables.append(
            Paragraph(text=app_handle.bldg_addy2,
                      style=styles['PrefixBase']))
    else:
        prefix_page.flowables.append(Paragraph(text='',
                                               style=styles['PrefixBase']))
    prefix_page.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                        height=2.0 * inch))
    prefix_page.flowables.append(
        Paragraph(
            text="Published: " + datetime.date.today().strftime("%d %B %Y"),
            style=styles['PrefixBase']))
    prefix_page.flowables.append(PageBreak())
    return prefix_page
