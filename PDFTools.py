# PDFTools.py
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle, Image, Frame, Spacer, Preformatted
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

class PDFTools:
	def __init__(self, DEBUG = 0,
				 DIRECTORY_IMAGES = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\WardPictures\\'):
		self.DIRECTORY_IMAGES = DIRECTORY_IMAGES
		self.TheTableStyle = TableStyle([
				('LEFTPADDING', (0,0), (-1,-1), 3),
				('RIGHTPADDING', (0,0), (-1,-1), 3),
				('BOTTOMPADDING', (0,0), (-1,-1), 0),
				('TOPPADDING', (1,0), (-1,-1), 0),
			])
		self.TheTableStyle.add('SPAN', (0,0), (2,0))
		if DEBUG:
			self.TheTableStyle.add('INNERGRID', (0,0), (-1,-1), 0.25, colors.black)
			self.TheTableStyle.add('BOX', (0,0), (-1,-1), .25, colors.black)
		self.styles = getSampleStyleSheet()
		self.styles.add(ParagraphStyle(name='DaveFooter',
								  parent=self.styles['Heading3'],
								  fontSize = 8,
								  alignment=TA_CENTER,
								  ))
		self.styles.add(ParagraphStyle(name='DaveHeaderLeft',
								  parent=self.styles['Heading3'],
								  fontSize = 8,
								  alignment=TA_LEFT,
								  ))
		self.styles.add(ParagraphStyle(name='DaveHeaderRight',
								  parent=self.styles['DaveHeaderLeft'],
								  alignment=TA_RIGHT,
								  ))
		self.styles.add(ParagraphStyle(name='DaveHeading',
								  parent=self.styles['Heading3'],
								  fontName = 'Times-Roman',
								  spaceAfter=0,
								  spaceBefore=0,
								  fontSize = 8,
								  ))
		self.styles.add(ParagraphStyle(name='DaveBold',
								  parent=self.styles['DaveHeading'],
								  fontName = 'Times-Bold',
								  fontSize = 10,
								  ))
		self.styles.add(ParagraphStyle(name='DaveBoldSmall',
								  parent=self.styles['DaveBold'],
								  fontSize = 8,
								  ))
		self.CombinedStyle = TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'),
									('LINEBELOW', (0,0), (-1,-1), 1.0, colors.black),
									('LINEABOVE', (0,0), (-1,-1), 1.0, colors.black),
									('LEFTPADDING', (0,0), (-1,-1), 0),
									('RIGHTPADDING', (0,0), (-1,-1), 0),
									('BOTTOMPADDING', (0,0), (-1,-1), 0),
									('TOPPADDING', (0,0), (-1,-1), 0),
									('LEADING', (0,0), (-1,-1), 0),
									('ALIGN', (0,0), (-1,-1), 'LEFT'),
									('FONTSIZE', (0,0), (-1,-1), 0),
				])
		if DEBUG:
			self.CombinedStyle.add('INNERGRID', (0,0), (-1,-1), 0.25, colors.black)
			self.CombinedStyle.add('BOX', (0,0), (-1,-1), 0.25, colors.black)
		self.MissingPictures = []

	def GetMissingPictures(self):
		return self.MissingPictures

	def TableizeFamily(self, Household):
		Family = []
		print Household[0],'Family'
		print "Number of Members", str(len(Household[1][0]) + len(Household[1][1]))
		for Parent in Household[1][0]:
			Family.append([Parent,'P'])
		for Child in Household[1][1]:
			Family.append([Child, 'C'])

		Rows = 3
		if 1 + len(Household[1][0]) + len(Household[1][1]) > Rows:
			Rows = 1 + len(Household[1][0]) + len(Household[1][1])

		#Get me a blank populated table
		data = []
		for Row in range(Rows):
			data.append([None, None, None, None, None])

		#Add the obvious entries
		data[0][0] = Paragraph(Household[0], self.styles['DaveBold'])
		data[0][3] = Paragraph(Household[2][0], self.styles['DaveHeading'])
		data[0][4] = Paragraph(Household[2][1], self.styles['DaveBoldSmall'])
		try:
			FamilyPicture = Image(self.DIRECTORY_IMAGES + Household[3])
			FamilyPicture.drawHeight = 1.125 * inch
		except:
			self.MissingPictures.append(Household[4])
			FamilyPicture = Image(self.DIRECTORY_IMAGES + 'Missing.jpg')
			FamilyPicture.drawHeight = (1.5 * inch /180) * 100.0
		FamilyPicture.drawWidth = 1.5 * inch

		#Add the family Members
		CurrentRow = 0
		print "Family:",Family
		for Member in Family:
			CurrentRow += 1
			if Member[1] == 'P':
				Column = 1
			else:
				Column = 2
			if not Member[0].find('<') == -1:
				data[CurrentRow][3] = Preformatted(Member[0][Member[0].find('<')+1:Member[0].find('>')], self.styles['DaveHeading'])
				self.TheTableStyle.add('SPAN', (3, CurrentRow), (4, CurrentRow))
				Member[0] = Member[0][:Member[0].find('<')]
			data[CurrentRow][Column] = Preformatted(Member[0], self.styles['DaveHeading'])
		TextTable = Table(data, [.125 * inch, .125 * inch, 0.9 * inch, 1.45 * inch, .8 * inch])
		TextTable.setStyle(self.TheTableStyle)
		TextTable.hAlign = 'LEFT'
		ImageTable = Table([[FamilyPicture]], [1.5 * inch])
		CombinedTableData = [[TextTable, ImageTable]]
		MasterTable = Table(CombinedTableData, ['*', 1.6 * inch])
		MasterTable.setStyle(self.CombinedStyle)
		return MasterTable
