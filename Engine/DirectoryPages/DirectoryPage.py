# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Frame, Paragraph

from .PDFStyles import styles
DEFAULT_PADDING = 0.25 * inch


class DirectoryPage(object):
    """
                width                    x2,y2
        +---------------------------------+
        | l  top padding                r | h
        | e +-------------------------+ i | e
        | f |                         | g | i
        | t |                         | h | g
        |   |                         | t | h
        | p |                         |   | t
        | a |                         | p |
        | d |                         | a |
        |   |                         | d |
        |   +-------------------------+   |
        |    bottom padding               |
        +---------------------------------+
        (x1,y1) <-- lower left corner

    NOTE!! Frames are stateful objects.  No single frame should be used in
    two documents at the same time (especially in the presence of
    multithreading.
    '''
    """
    # we'll always assume that x1 and y1 are the bottom left of the frame
    # corner
    # width and height will be the full half sheet of paper
    def __init__(self, left_padding=DEFAULT_PADDING,
                 right_padding=DEFAULT_PADDING):
        self.left_padding = left_padding
        self.right_padding = right_padding
        self.flowables = []
        self.page_number = 0

    def get_frame(self, debug, side='Left'): # or Right
        x1 = 0
        if side == 'Right':
            x1 = landscape(letter)[0]/2
        return Frame(x1=x1,
                     y1=0,
                     width=landscape(letter)[0]/2,
                     height=landscape(letter)[1],
                     leftPadding=self.left_padding,
                     bottomPadding=DEFAULT_PADDING,
                     rightPadding=self.right_padding,
                     topPadding=DEFAULT_PADDING,
                     showBoundary=debug)

    def make_frame(self, debug, side, pdfHandle):
        frame = self.get_frame(debug, side)
        counter = 0
        for flowable in self.flowables:
            if flowable == 'CURRENT_PAGE_NUMBER':
                flowable = Paragraph('Page %d' % self.page_number,
                                     styles['DaveHeader%s' % side])
            frame.add(flowable, pdfHandle)
            counter += 1
