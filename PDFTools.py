# PDFTools.py
import win32api
import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle, Image, Frame, Spacer, Preformatted
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import time
import datetime

class PDFTools:
	def __init__(self, DEBUG = 0,
				 DIRECTORY_IMAGES = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\WardPictures\\',
				 APPDATAFOLDER = 'Ward Directory',
				 filename = 'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '.pdf',
				 front = 'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '_FRONT.pdf',
				 back = 'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '_BACK.pdf'
				 ):
		self.DEBUG = DEBUG
		self.DIRECTORY_IMAGES = DIRECTORY_IMAGES

		self.filename = win32api.GetEnvironmentVariable('APPDATA') + os.sep + APPDATAFOLDER + os.sep + filename
		self.front = win32api.GetEnvironmentVariable('APPDATA') + os.sep + APPDATAFOLDER + os.sep + front
		self.back = win32api.GetEnvironmentVariable('APPDATA') + os.sep + APPDATAFOLDER + os.sep + back
		
		styles = getSampleStyleSheet()
		styles.add(ParagraphStyle(name='DaveFooter',
								  parent=styles['Heading3'],
								  fontSize = 8,
								  alignment=TA_CENTER,
								  ))
		styles.add(ParagraphStyle(name='DaveHeaderLeft',
								  parent=styles['Heading3'],
								  fontSize = 8,
								  alignment=TA_LEFT,
								  ))
		styles.add(ParagraphStyle(name='DaveHeaderRight',
								  parent=styles['DaveHeaderLeft'],
								  alignment=TA_RIGHT,
								  ))
		styles.add(ParagraphStyle(name='DaveHeading',
								  parent=styles['Heading3'],
								  fontName = 'Times-Roman',
								  spaceAfter=0,
								  spaceBefore=0,
								  fontSize = 8,
								  ))
		styles.add(ParagraphStyle(name='DaveBold',
								  parent=styles['DaveHeading'],
								  fontName = 'Times-Bold',
								  fontSize = 10,
								  ))
		styles.add(ParagraphStyle(name='DaveBoldSmall',
								  parent=styles['DaveBold'],
								  fontSize = 8,
								  ))
		self.CurrentWardDirectory = []

		self.TheTableStyle = TableStyle([
				('LEFTPADDING', (0,0), (-1,-1), 3),
				('RIGHTPADDING', (0,0), (-1,-1), 3),
				('BOTTOMPADDING', (0,0), (-1,-1), 0),
				('TOPPADDING', (1,0), (-1,-1), 0),
			])
		#########NOTICE THAT SPAN IS WRITTEN BASS ACKWARDS WITH COL,ROW
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
		Margin = .25 * inch
		self.Bottom = Margin
		self.FarLeft = Margin
		self.NotSoFarLeft = landscape(letter)[0]/2 + Margin
		self.FrameWidth = landscape(letter)[0]/2 - 2 * Margin
		self.FrameHeight = landscape(letter)[1] - 2 * Margin
		self.ChurchFlowable = Paragraph('For Church Use Only', styles['DaveFooter'])

	def AddDirectoryWrapperImages(self):
		#Let's make some stock flowables for 'FOR CHURCH USE ONLY' and 'PAGE NUMBER'
		self.CurrentWardDirectory.insert(0, Image(self.DIRECTORY_IMAGES + '001.jpg', width=self.FrameWidth, height=self.FrameHeight))
		self.CurrentWardDirectory.insert(0, Image(self.DIRECTORY_IMAGES + '000.jpg', width=self.FrameWidth, height=self.FrameHeight))
		self.CurrentWardDirectory.append(Image(self.DIRECTORY_IMAGES + '-003.jpg', width=self.FrameWidth, height=self.FrameHeight))
		self.CurrentWardDirectory.append(Image(self.DIRECTORY_IMAGES + '-002.jpg', width=self.FrameWidth, height=self.FrameHeight))
		self.CurrentWardDirectory.append(Image(self.DIRECTORY_IMAGES + '-001.jpg', width=self.FrameWidth, height=self.FrameHeight))
		self.CurrentWardDirectory.append(Image(self.DIRECTORY_IMAGES + '-000.jpg', width=self.FrameWidth, height=self.FrameHeight))

	def AddFooter(self, FooterText):
		self.CurrentWardDirectory.append(Paragraph(FooterText, self.styles['DaveFooter']))

	def AddFamily(self, Household):
		MasterTable = self.TableizeFamily(Household)
		self.CurrentWardDirectory.append(MasterTable)

	def GenerateWardPagination(self):
		##Make a backup of the current document
		FlowableBackup = []
		for myFlowable in self.CurrentWardDirectory:
			FlowableBackup.append(myFlowable)

		pdf_TEST = Canvas("DIRECTORY_TEST.pdf", pagesize = landscape(letter))
		
		##THE NEXT LOOP IS TO GET THE COUNTS OF HOW MANY PAGES I'LL END UP WITH AND HOW MANY FLOWABLES WILL FALL ONTO EACH PAGE
		CurrentPage = -1
		FamiliesOnPages = []
		TotalFlowables = len(self.CurrentWardDirectory)
		while len(self.CurrentWardDirectory):
			LeftFrame = Frame(self.FarLeft, self.Bottom, self.FrameWidth, self.FrameHeight, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0, showBoundary = self.DEBUG)
			RightFrame = Frame(self.NotSoFarLeft, self.Bottom, self.FrameWidth, self.FrameHeight, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0, showBoundary = self.DEBUG)
			CurrentPage += 1
			print len(self.CurrentWardDirectory)
			Start = len(self.CurrentWardDirectory)
			if CurrentPage >= 2 and len(self.CurrentWardDirectory) > 4:
				LeftFrame.addFromList([self.ChurchFlowable], pdf_TEST)
				LeftFrame.addFromList([Paragraph('Page ' + str(CurrentPage), self.styles['DaveHeaderLeft'])], pdf_TEST)
			LeftFrame.addFromList(self.CurrentWardDirectory, pdf_TEST)
			FamiliesOnPages.append([CurrentPage, TotalFlowables - Start, Start - len(self.CurrentWardDirectory), len(self.CurrentWardDirectory)])

			if len(self.CurrentWardDirectory) == 0:
				continue

			CurrentPage += 1
			Start = len(self.CurrentWardDirectory)
			if CurrentPage >= 2 and len(self.CurrentWardDirectory) > 4:
				RightFrame.addFromList([self.ChurchFlowable], pdf_TEST)
				RightFrame.addFromList([Paragraph('Page ' + str(CurrentPage), self.styles['DaveHeaderRight'])], pdf_TEST)
			RightFrame.addFromList(self.CurrentWardDirectory, pdf_TEST)
			FamiliesOnPages.append([CurrentPage, TotalFlowables - Start, Start - len(self.CurrentWardDirectory), len(self.CurrentWardDirectory)])
			pdf_TEST.showPage()

		UsedFaces = CurrentPage + 1
		print str(UsedFaces) + " faces are present"
		Fillers = (4 - UsedFaces % 4) % 4
		print str(Fillers) + " blank faces will be added to make full pages"
		for Count in range(Fillers):
			FamiliesOnPages.insert(-4, [-1, 0, 1, 0])
		PageCount = (UsedFaces + Fillers) / 4
		print str(PageCount) + " slices of paper per directory are needed"

		print "Before Flowable Filler Addition"
		for Item in FamiliesOnPages:
			print Item

		##Insert filler flowables
		for Count in range(Fillers):
			FlowableBackup.insert(-4, Image(self.DIRECTORY_IMAGES + 'blank.jpg', width=self.FrameWidth, height=self.FrameHeight))

		##Renumber FamiliesOnPages
		NewPageCounts = []
		Remaining = FamiliesOnPages[0][2] + FamiliesOnPages[0][3] + Fillers
		Used = 0
		PageCounter = 0
		for item in FamiliesOnPages:
			Remaining -= item[2]
			NewPageCounts.append([PageCounter, Used, item[2], Remaining])
			Used += item[2]
			PageCounter += 1
		self.FamiliesOnPages = NewPageCounts

		##Recover From Flowable Backup
		self.CurrentWardDirectory = []
		for myFlowable in FlowableBackup:
			self.CurrentWardDirectory.append(myFlowable)

		print "After Flowable Filler Addition"
		for Item in self.FamiliesOnPages:
			print Item

	def GeneratePDFDocs(self):
		##Print to PDF using the correct formats now and the correct page ordering
		FrontPageLayout = []
		BackPageLayout = []
		NormalPageLayout = []
		Sides = (self.FamiliesOnPages[-1][0]+1) / 2
		for pageside in range(Sides):
			NormalPageLayout.append([pageside*2, pageside*2 + 1])
			if pageside < Sides / 2:
				FrontPageLayout.append([(Sides * 2 - 1) - 2 * pageside, pageside * 2])
				BackPageLayout.append([pageside * 2 + 1, Sides * 2 - 2 - 2 * pageside])
		print FrontPageLayout
		print BackPageLayout
		print NormalPageLayout

		pdf = Canvas(self.filename, pagesize = landscape(letter))
		pdf.setAuthor('David Ernstrom')
		pdf.setTitle('Ward Directory')
		pdf.setSubject('Subject Line')
		pdf_FRONT = Canvas(self.front, pagesize = landscape(letter))
		pdf_FRONT.setAuthor('David Ernstrom')
		pdf_FRONT.setTitle('Ward Directory')
		pdf_FRONT.setSubject('Subject Line')
		pdf_BACK = Canvas(self.back, pagesize = landscape(letter))
		pdf_BACK.setAuthor('David Ernstrom')
		pdf_BACK.setTitle('Ward Directory')
		pdf_BACK.setSubject('Subject Line')

		ThingsToPrint = [[NormalPageLayout, pdf],
						 [FrontPageLayout, pdf_FRONT],
						 [BackPageLayout, pdf_BACK]]

		for PrintJob in ThingsToPrint:
			for page in PrintJob[0]:
				LeftFrame = Frame(self.FarLeft, self.Bottom, self.FrameWidth, self.FrameHeight, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0, showBoundary = self.DEBUG)
				RightFrame = Frame(self.NotSoFarLeft, self.Bottom, self.FrameWidth, self.FrameHeight, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0, showBoundary = self.DEBUG)

				MyLeftFrame = page[0]
				MyRightFrame = page[1]

				LeftFrameStartFlowable = self.FamiliesOnPages[MyLeftFrame][1]
				LeftFrameFlowablesConsumed = self.FamiliesOnPages[MyLeftFrame][2]

				RightFrameStartFlowable = self.FamiliesOnPages[MyRightFrame][1]
				RightFrameFlowablesConsumed = self.FamiliesOnPages[MyRightFrame][2]

				if not LeftFrameFlowablesConsumed == 1:
					LeftFrame.addFromList([Paragraph('Page ' + str(MyLeftFrame), self.styles['DaveHeaderLeft'])], PrintJob[1])

				LeftFrame.addFromList(self.CurrentWardDirectory[LeftFrameStartFlowable:LeftFrameStartFlowable + LeftFrameFlowablesConsumed], PrintJob[1])

				if not LeftFrameFlowablesConsumed == 1:
					LeftFrame.addFromList([self.ChurchFlowable], PrintJob[1])


				if not RightFrameFlowablesConsumed == 1:
					RightFrame.addFromList([Paragraph('Page ' + str(MyRightFrame), self.styles['DaveHeaderRight'])], PrintJob[1])

				RightFrame.addFromList(self.CurrentWardDirectory[RightFrameStartFlowable:RightFrameStartFlowable + RightFrameFlowablesConsumed], PrintJob[1])

				if not RightFrameFlowablesConsumed == 1:
					RightFrame.addFromList([self.ChurchFlowable], PrintJob[1])

				#page[0] is the left side
				CurrentDateString = datetime.date.today().strftime("%d %B %Y")
				if page[0] == 0:
					PrintJob[1].drawString(self.FarLeft + self.FrameWidth/2, 75, CurrentDateString)
				if page[1] == 0:
					PrintJob[1].drawString(self.NotSoFarLeft + self.FrameWidth/2, 75, CurrentDateString)
				PrintJob[1].showPage()
			print "PDF Completed"

		try:
			pdf.save()
			pdf_FRONT.save()
			pdf_BACK.save()
		except IOError:
			os.mkdir(win32api.GetEnvironmentVariable('APPDATA') + os.sep + APPDATAFOLDER)
			pdf.save()
			pdf_FRONT.save()
			pdf_BACK.save()
		os.system('\"' + self.filename + '\"')

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
