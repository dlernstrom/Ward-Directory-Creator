from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape

class PDFTools:
    def __init__(self, DEBUG):
        self.DEBUG = 1

    def AddFooter(self, FooterText):
        self.CurrentWardDirectory.append(Paragraph(FooterText, self.styles['DaveFooter']))

    def generate_doc(self, filename, jobType, pages):
        layout =[]
        sides = (len(pages)+1) / 2
        for pageside in xrange(sides):
            if jobType == 'full':
                layout.append([pageside * 2, pageside * 2 + 1])
            if pageside < sides / 2:
                if jobType == 'front':
                    layout.append([(sides * 2 - 1) - 2 * pageside, pageside * 2])
                elif jobType == 'back':
                    layout.append([pageside * 2 + 1, sides * 2 - 2 - 2 * pageside])
                elif jobType == 'special':
                    SpecialPageLayout.append([(sides * 2 - 1) - 2 * pageside, pageside * 2])
                    SpecialPageLayout.append([pageside * 2 + 1, sides * 2 - 2 - 2 * pageside])

        pdf = Canvas(filename, pagesize = landscape(letter))
        pdf.setAuthor('David Ernstrom')
        pdf.setTitle('Ward Directory')
        pdf.setSubject('Subject Line')
        pdf.setFont('Helvetica', 18)

        for page in layout:
            leftFrame = pages[page[0]].get_frame(debug = self.DEBUG, side = 'Left', pdfHandle = pdf)
            try:
                rightFrame = pages[page[1]].get_frame(debug = self.DEBUG, side = 'Right', pdfHandle = pdf)
            except IndexError:
                pass
            pdf.showPage()
        print "PDF Completed"
        pdf.save()
