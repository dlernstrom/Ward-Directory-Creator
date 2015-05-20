# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import PageBreak, Paragraph, Spacer
from reportlab.platypus.flowables import KeepInFrame
from reportlab.lib.units import inch

from DirectoryPage import DirectoryPage
from PDFStyles import styles
import __version__

STANDARD_MARGIN = 0.25 * inch
STANDARD_FRAME_WIDTH = landscape(letter)[0]/2 - 2 * STANDARD_MARGIN


def get_quote_data(configData):
    quoteData = ['','']
    if configData['quote.usequote'] == '1':
        quoteData = [configData['quote.quotecontent'],
                     configData['quote.quoteauthor']]
    return quoteData


def get_directory_suffix_pages(dictionaryData, debug):
    pages = []
    ##########################################
    ## LAST PAGE DATA
    suffixPage = DirectoryPage()
    #Here, we'll add our comment and disclaimer data to the end of the document
    suffixPage.flowables.append(Spacer(width = STANDARD_FRAME_WIDTH, height = 2.0 * inch))

    # ADD THE QUOTE
    QuoteText_List = []
    quoteData = get_quote_data(dictionaryData)
    for Line in quoteData[0].split('\n'):
        if not len(QuoteText_List) and len(quoteData[0].split('\n')) > 1:
            QuoteStyle = styles['QuoteTitle']
        else:
            QuoteStyle = styles['PrefixBase']
        QuoteText_List.append(Paragraph(text = Line, style = QuoteStyle))
    QuoteText_List.extend([Spacer(width = STANDARD_FRAME_WIDTH, height = .125 * inch),
                           Paragraph(text = "<i>- " + quoteData[1] + "</i>", style = styles['RegTextR']),
                           Spacer(width = STANDARD_FRAME_WIDTH, height = 7.0 * inch)])
    suffixPage.flowables.append(KeepInFrame(maxWidth = STANDARD_FRAME_WIDTH,
                                            maxHeight = 5.0 * inch,
                                            content = QuoteText_List,
                                            mode = 'truncate'))
    # END WITH QUOTE

    suffixPage.flowables.append(Paragraph(text = "Membership data taken from church records available via the",
                                          style = styles['RegText']))
    suffixPage.flowables.append(Paragraph(text = dictionaryData['unit.unitname'] + " website at www.lds.org/directory.",
                                          style = styles['RegText']))
    suffixPage.flowables.append(Paragraph(text = "Prepared using Ward Directory Creator v.%s" % __version__.__version__,
                                          style = styles['RegText']))
    suffixPage.flowables.append(Paragraph(text = "All information for Church use only.",
                                          style = styles['RegText']))
    suffixPage.flowables.append(PageBreak())
    #############################################
    ## END OF SUFFIX DATA
    pages.append(suffixPage)

    if debug:
        for aFlowable in suffixPage.flowables:
            if aFlowable.__class__ is Paragraph or aFlowable.__class__ is Spacer:
                aFlowable._showBoundary = 1
    return pages
