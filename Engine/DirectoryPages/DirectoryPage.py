from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Frame, Paragraph

from PDFStyles import styles
DEFAULT_PADDING = 0.25 * inch

class DirectoryPage:
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
    two documents at the same time (especially in the presence of multithreading.
    '''
    """
    # we'll always assume that x1 and y1 are the bottom left of the frame corner
    # width and height will be the full half sheet of paper
    def __init__(self, pageNumber = 0, leftPadding = DEFAULT_PADDING, bottomPadding = DEFAULT_PADDING, rightPadding = DEFAULT_PADDING, topPadding = DEFAULT_PADDING):
        self.leftPadding = leftPadding
        self.bottomPadding = bottomPadding
        self.rightPadding = rightPadding
        self.topPadding = topPadding
        self.flowables = []
        self.pageNumber = 0

    def get_frame(self, debug, side = 'Left', pdfHandle = None): # or Right
        x1 = 0
        if side == 'Right':
            x1 = landscape(letter)[0]/2
        fm = Frame(x1 = x1,
                   y1 = 0,
                   width = landscape(letter)[0]/2,
                   height = landscape(letter)[1],
                   leftPadding = self.leftPadding,
                   bottomPadding = self.bottomPadding,
                   rightPadding = self.rightPadding,
                   topPadding = self.topPadding,
                   showBoundary = debug)
        if pdfHandle:
            counter = 0
            for flowable in self.flowables:
                if flowable == 'CURRENT_PAGE_NUMBER':
                    flowable = Paragraph('Page %d' % self.pageNumber, styles['DaveHeader%s' % side])
                fm.add(flowable, pdfHandle)
                counter += 1
        return fm
