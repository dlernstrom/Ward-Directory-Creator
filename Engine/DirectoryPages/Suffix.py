# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import PageBreak, Paragraph, Spacer
from reportlab.platypus.flowables import KeepInFrame
from reportlab.lib.units import inch

from DirectoryPage import DirectoryPage
from PDFStyles import styles
from __version__ import __version__

STANDARD_MARGIN = 0.25 * inch
STANDARD_FRAME_WIDTH = landscape(letter)[0]/2 - 2 * STANDARD_MARGIN


def get_quote_data(config_data):
    quote_data = ['','']
    if config_data['quote.usequote'] == '1':
        quote_data = [config_data['quote.quotecontent'],
                     config_data['quote.quoteauthor']]
    return quote_data


def get_directory_suffix_pages(dict_data, debug):
    pages = []
    ###########################################################################
    ## LAST PAGE DATA
    suffix_pg = DirectoryPage()
    # We'll add our comment and disclaimer data to the end of the document
    suffix_pg.flowables.append(Spacer(width=STANDARD_FRAME_WIDTH,
                                      height=2.0 * inch))

    # ADD THE QUOTE
    QuoteText_List = []
    quoteData = get_quote_data(dict_data)
    for Line in quoteData[0].split('\n'):
        if not len(QuoteText_List) and len(quoteData[0].split('\n')) > 1:
            QuoteStyle = styles['QuoteTitle']
        else:
            QuoteStyle = styles['PrefixBase']
        QuoteText_List.append(Paragraph(text=Line, style=QuoteStyle))
    QuoteText_List.extend([Spacer(width=STANDARD_FRAME_WIDTH,
                                  height=.125 * inch),
                           Paragraph(text="<i>- " + quoteData[1] + "</i>",
                                     style=styles['RegTextR']),
                           Spacer(width=STANDARD_FRAME_WIDTH,
                                  height=7.0 * inch)])
    suffix_pg.flowables.append(KeepInFrame(maxWidth=STANDARD_FRAME_WIDTH,
                                           maxHeight=5.0 * inch,
                                           content=QuoteText_List,
                                           mode='truncate'))
    # END WITH QUOTE

    suffix_pg.flowables.append(Paragraph(text="Membership data taken from church records available via the",
                                         style=styles['RegText']))
    suffix_pg.flowables.append(Paragraph(text=dict_data['unit.unitname'] + " website at www.lds.org/directory.",
                                         style=styles['RegText']))
    suffix_pg.flowables.append(Paragraph(text="Prepared using Ward Directory Creator v.%s" % __version__,
                                         style=styles['RegText']))
    suffix_pg.flowables.append(Paragraph(text="All information for Church use only.",
                                         style=styles['RegText']))
    suffix_pg.flowables.append(PageBreak())
    ###########################################################################
    ## END OF SUFFIX DATA
    pages.append(suffix_pg)

    if debug:
        for flow in suffix_pg.flowables:
            if flow.__class__ in [Paragraph, Spacer]:
                flow._showBoundary = 1
    return pages
