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
    leftPadding = 0
    bottomPadding = 0
    rightPadding = 0
    topPadding = 0
    flowables = []
    pageNumber = 0
    def __init__(self, pageNumber, padding = .25 * inch, flowables = []):
        self.leftPadding = padding
        self.bottomPadding = padding
        self.rightPadding = padding
        self.topPadding = padding
        self.flowables = flowables
