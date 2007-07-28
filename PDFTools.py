# PDFTools.py
import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle, Image, Frame, Spacer, Preformatted, PageBreak
from reportlab.platypus.flowables import HRFlowable, KeepInFrame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import time
import datetime

class PDFTools:
	def __init__(self,
				 DEBUG,
				 ImagesFolder,
				 OutputFolder,
				 Full,
				 Booklet,
				 DictionaryData,
				 BlockData,
				 QuoteData,
				 FullVersionString
				 ):
		self.DEBUG = DEBUG
		self.ImagesFolder = str(ImagesFolder)
		self.OutputFolder = str(OutputFolder)
		self.Full = Full
		self.Booklet = Booklet
		self.DictionaryData = DictionaryData
		self.BlockData = BlockData
		self.QuoteData = QuoteData
		self.FullVersionString = FullVersionString

		self.filename = self.OutputFolder + os.sep + 'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '.pdf'
		self.front = self.OutputFolder + os.sep + 'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '_FRONT.pdf'
		self.back = self.OutputFolder + os.sep + 'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '_BACK.pdf'

		self.styles = getSampleStyleSheet()
		#This is what sets Helvetica as the base font for the PrefixPages
		self.styles.add(ParagraphStyle(name = 'PrefixBase',
									   fontName = 'Times-Roman',#Helvetica',
									   fontSize = 14,
									   leading = 1.3 * 14,
									   alignment = TA_CENTER,
									   ))
		#Here I create a style for the header pages
		self.styles.add(ParagraphStyle(name = 'DocumentTitle',
									   parent = self.styles['PrefixBase'],
									   fontSize = 30,
									   leading = 1.2 * 30,
									   ))
		self.styles.add(ParagraphStyle(name = 'QuoteTitle',
									   parent = self.styles['PrefixBase'],
									   fontSize = 26,
									   leading = 1.2 * 26,
									   ))
		self.styles.add(ParagraphStyle(name = 'Subtitle',
									   parent = self.styles['PrefixBase'],
									   fontSize = 18,
									   leading = 1.2 * 18,
									   ))
		self.styles.add(ParagraphStyle(name = 'PrefixBaseRight',
									   parent = self.styles['PrefixBase'],
									   alignment = TA_RIGHT,
									   ))
		self.styles.add(ParagraphStyle(name = 'PrefixBaseLeft',
									   parent = self.styles['PrefixBase'],
									   alignment = TA_LEFT,
									   ))
		self.styles.add(ParagraphStyle(name = 'RegText',
									   #parent = self.styles['PrefixBase'],
									   fontsize = 8,
									   alignment = TA_CENTER,
									   leading = 1.5 * 8,
									   ))
		self.styles.add(ParagraphStyle(name = 'RegTextL',
									   parent = self.styles['RegText'],
									   alignment = TA_LEFT,
									   ))
		self.styles.add(ParagraphStyle(name = 'RegTextR',
									   parent = self.styles['RegText'],
									   alignment = TA_RIGHT,
									   ))


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
		self.ChurchFlowable = Paragraph('For Church Use Only', self.styles['DaveFooter'])

	def GetPositionData(self):
		#Return a list of dictionaries of the positions ordered correctly
		#TODO: This should happen by my parent... I am the customer and should get it how I want it already
		RoleList = ['bish', 'first', 'second', 'exec', 'clerk', 'fin', 'mem', "NULL",
					'hp', 'eq', 'rs', 'ym', 'yw', 'primary', "NULL",
					'wml', 'act', 'news', 'dir']
		RoleDict = {'bish' :	'Bishop',
					'first' :	'1st Counselor',
					'second' :	'2nd Counselor',
					'exec' :	'Executive Secretary',
					'clerk' :	'Ward Clerk',
					'fin' :		'Financial Clerk',
					'mem' :		'Membership Clerk',
					'hp' :		'High Priest Group Leader',
					'eq' :		'Elders Quorum President',
					'rs' :		'Relief Society President',
					'ym' :		"Young Men's President",
					'yw' :		"Young Women's President",
					'primary' :	'Primary President',
					'wml' :		'Ward Mission Leader',
					'act' :		'Activities Committee Chair',
					'news' :	'Ward Newsletter',
					'dir' :		'Ward Directory',
					"NULL" :	''}
		LeadershipList = []
		for Role in RoleList:
			try:
				if self.DictionaryData['leadership.' + Role + 'disp'] == '1':
					LeadershipList.append({"Role" :		RoleDict[Role],
										   "Name" :		self.DictionaryData['leadership.' + Role + 'name'],
										   "Phone" :	self.DictionaryData['leadership.' + Role + 'phone']})
				else:
					LeadershipList.append({"Role" :		" ",
										   "Name" :		" ",
										   "Phone" :	" "})
					LeadershipList.append({"Role" :		" ",
										   "Name" :		" ",
										   "Phone" :	" "})
			except KeyError:
				LeadershipList.append({"Role" :		" ",
									   "Name" :		" ",
									   "Phone" :	" "})
				LeadershipList.append({"Role" :		" ",
									   "Name" :		" ",
									   "Phone" :	" "})
		return LeadershipList

	def GetBlockData(self):
		if self.DEBUG:
			print "Here, I parse the block data stuff that was sent to me"
			print self.BlockData
		myDisplayBlock = []
		for Mtg in self.BlockData:
			myDisplayBlock.append([[Paragraph(text = Mtg[0], style = self.styles['PrefixBaseRight'])],
								   [Paragraph(text = Mtg[1], style = self.styles['PrefixBaseLeft'])]])
		if self.DEBUG:
			print "and return a data = [[,],[,],[,]] to be used in the PDFTools Sections"
		return myDisplayBlock

	def AddDirectoryPrefixData(self):
		if self.DEBUG:
			print "Here's the dictionary I received"
			print self.DictionaryData
		#TODO: Need to validate that I have at least a blank in all of the following fields:
		"""
		Send it to a validation function to do the following:
		unit.unitname
		unit.stakename
		bldg.addy1
		bldg.addy2
		block.sacstart
		block.ssstart
		block.pr_rs_start
		bldg.phone
		"""
		#Page 1 Data
		self.PrefixFlowables = []
		self.PrefixFlowables.append(Spacer(width = self.FrameWidth, height = 1.5 * inch))
		self.PrefixFlowables.append(Paragraph(text = "<b>" + self.DictionaryData['unit.unitname'] + "</b>", style = self.styles['DocumentTitle']))
		self.PrefixFlowables.append(Paragraph(text = "Member Directory", style = self.styles['Subtitle']))
		self.PrefixFlowables.append(Spacer(width = self.FrameWidth, height = 2.0 * inch))
		self.PrefixFlowables.append(Paragraph(text = self.DictionaryData['unit.stakename'], style = self.styles['PrefixBase']))
		self.PrefixFlowables.append(Paragraph(text = self.DictionaryData['bldg.addy1'], style = self.styles['PrefixBase']))
		self.PrefixFlowables.append(Paragraph(text = self.DictionaryData['bldg.addy2'], style = self.styles['PrefixBase']))
		self.PrefixFlowables.append(Spacer(width = self.FrameWidth, height = 2.0 * inch))
		CurrentDateString = datetime.date.today().strftime("%d %B %Y")
		self.PrefixFlowables.append(Paragraph(text = "Published: " + CurrentDateString, style = self.styles['PrefixBase']))
		self.PrefixFlowables.append(PageBreak())

		#Page 2 Data
		self.PrefixFlowables.append(Spacer(width = self.FrameWidth, height = .125 * inch))
		CurrentYearString = datetime.date.today().strftime("%Y")
		self.PrefixFlowables.append(Paragraph(text = "<u>" + CurrentYearString + " Meeting Schedule</u>", style = self.styles['Subtitle']))
		self.PrefixFlowables.append(Spacer(width = self.FrameWidth, height = .125 * inch))
		TextTable = Table(self.GetBlockData(), [1.5 * inch, 3.0 * inch])
		if self.DEBUG:
			TextTable.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
										   ('BOX', (0,0), (-1,-1), .25, colors.black),
										   ]))
		self.PrefixFlowables.append(TextTable)
		self.PrefixFlowables.append(Spacer(width = self.FrameWidth, height = .125 * inch))
		self.PrefixFlowables.append(Paragraph(text = "Office Phone: " + self.DictionaryData['bldg.phone'], style = self.styles['PrefixBase']))
		self.PrefixFlowables.append(Spacer(width = self.FrameWidth, height = .125 * inch))
		self.PrefixFlowables.append(HRFlowable(width = "90%", thickness = 1, lineCap= 'square', color = colors.black))
		self.PrefixFlowables.append(Spacer(width = self.FrameWidth, height = .125 * inch))
		data = []
		
		for Position in self.GetPositionData():
			data.append([[Paragraph(text = Position['Role'], style = self.styles['RegTextR'])],
						 [Paragraph(text = Position['Name'], style = self.styles['RegTextL'])],
						 [Paragraph(text = Position['Phone'], style = self.styles['RegTextL'])]])
		TextTable = Table(data, [1.8 * inch, 2.0 * inch, 1.2 * inch])
		if self.DEBUG:
			TextTable.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
										   ('BOX', (0,0), (-1,-1), .25, colors.black),
										   ]))
		self.PrefixFlowables.append(KeepInFrame(maxWidth = self.FrameWidth,
												maxHeight = 5.0 * inch,
												content = [TextTable,
														   Spacer(width = self.FrameWidth, height = 7.0 * inch)],
												mode = 'truncate'))
		Disclaimer = """This ward directory is to be used only for Church purposes
						 and should not be copied without permission of the bishop
						 or stake president.
						 """
		self.PrefixFlowables.append(Paragraph(text = "<b>" + Disclaimer + "</b>", style = self.styles['RegText']))
		self.PrefixFlowables.append(PageBreak())
		if self.DEBUG:
			for aFlowable in self.PrefixFlowables:
				if not aFlowable.__class__ is PageBreak and not aFlowable.__class__ is HRFlowable and not aFlowable.__class__ is Table and not aFlowable.__class__ is Image:
					aFlowable._showBoundary = 1

	def AddDirectorySuffixData(self):
		self.SuffixFlowables = []
		self.SuffixFlowables.append(Image(self.ImagesFolder + os.sep + '-003.jpg', width=self.FrameWidth, height=self.FrameHeight))
		self.SuffixFlowables.append(Image(self.ImagesFolder + os.sep + '-002.jpg', width=self.FrameWidth, height=self.FrameHeight))
		self.SuffixFlowables.append(Image(self.ImagesFolder + os.sep + '-001.jpg', width=self.FrameWidth, height=self.FrameHeight))

		#Here, we'll add our comment and disclaimer data to the end of the document
		self.SuffixFlowables.append(Spacer(width = self.FrameWidth, height = 2.0 * inch))

		textdata = "As children of the Lord\nwe should strive every day to rise to a higher level of personal righteousness in all of our actions."
		QuoteText_List = []
		for Line in self.QuoteData[0].split('\n'):
			if not len(QuoteText_List) and len(self.QuoteData[0].split('\n')) > 1:
				QuoteStyle = self.styles['QuoteTitle']
			else:
				QuoteStyle = self.styles['PrefixBase']
			QuoteText_List.append(Paragraph(text = Line, style = QuoteStyle))
		QuoteText_List.extend([Spacer(width = self.FrameWidth, height = .125 * inch),
							   Paragraph(text = "<i>- " + self.QuoteData[1] + "</i>", style = self.styles['RegTextR']),
							   Spacer(width = self.FrameWidth, height = 7.0 * inch)])
		self.SuffixFlowables.append(KeepInFrame(maxWidth = self.FrameWidth,
												maxHeight = 5.0 * inch,
												content = QuoteText_List,
												mode = 'truncate'))

		self.SuffixFlowables.append(Paragraph(text = "Membership data taken from church records available via the",
											  style = self.styles['RegText']))
		self.SuffixFlowables.append(Paragraph(text = self.DictionaryData['unit.unitname'] + " website at www.lds.org/units.",
											  style = self.styles['RegText']))
		self.SuffixFlowables.append(Paragraph(text = "Prepared using Ward Directory Creator " + self.FullVersionString,
											  style = self.styles['RegText']))
		self.SuffixFlowables.append(Paragraph(text = "All information for Church use only.",
											  style = self.styles['RegText']))
		self.SuffixFlowables.append(PageBreak())

		if self.DEBUG:
			for aFlowable in self.SuffixFlowables:
				if not aFlowable.__class__ is PageBreak and not aFlowable.__class__ is HRFlowable and not aFlowable.__class__ is Table and not aFlowable.__class__ is Image:
					aFlowable._showBoundary = 1

	def AddFooter(self, FooterText):
		self.CurrentWardDirectory.append(Paragraph(FooterText, self.styles['DaveFooter']))

	def AddFamily(self, Household):
		self.CurrentWardDirectory.append(self.TableizeFamily(Household))

	def FlowableGenerator(self):
		##Make a backup of the current document
		Test_PrefixFlowables = self.PrefixFlowables[:]
		Test_MemberFlowables = self.CurrentWardDirectory[:]
		Test_SuffixFlowables = self.SuffixFlowables[:]
		#The following section has a True or False to tell me if I add page header/footer data
		DirSections = [[Test_PrefixFlowables, False],
					   [Test_MemberFlowables, True],
					   [Test_SuffixFlowables, False]]
		self.FlowablesConsumed = 0
		for FlowableList, Header_Footer in DirSections:
			for SingleFlowable in FlowableList:
				yield Header_Footer
				yield SingleFlowable
				self.FlowablesConsumed += 1

	def PrepareFiller(self):
		LineSpace_List = []
		for Counter in range(30):
			LineSpace_List.append(Spacer(width = self.FrameWidth, height = .25 * inch))
			LineSpace_List.append(HRFlowable(width = "90%", thickness = 1, lineCap= 'square', color = colors.black))
		ReturnList = [Paragraph(text = "NOTES", style = self.styles['Subtitle']),
				KeepInFrame(maxWidth = self.FrameWidth,
							maxHeight = 7.5 * inch,
							content = LineSpace_List,
							mode = 'truncate'),
				PageBreak()]
		return ReturnList

	def GenerateWardPagination(self):
		pdf_TEST = Canvas("DIRECTORY_TEST.pdf", pagesize = landscape(letter))

		##THE NEXT LOOP IS TO GET THE COUNTS OF HOW MANY PAGES I'LL END UP WITH AND HOW MANY FLOWABLES WILL FALL ONTO EACH PAGE
		FlowablesOnPages = []

		#PREPARE FOR FIRST TIME THROUGH
		self.TotalFlowables = len(self.CurrentWardDirectory) + len(self.PrefixFlowables) + len(self.SuffixFlowables)
		if self.DEBUG:
			for element in self.PrefixFlowables:
				print element.__class__
			print "Start Length", self.TotalFlowables
		GeneratorHandle = self.FlowableGenerator()
		Header_Footer = GeneratorHandle.next()
		SingleFlowable = GeneratorHandle.next()
		while self.TotalFlowables - self.FlowablesConsumed > 0:
			#PREPARE FOR A FRAME
			StartingFlowablesConsumed = self.FlowablesConsumed
			#BUILD THE FRAME
			MyFrame = Frame(self.FarLeft, self.Bottom, self.FrameWidth, self.FrameHeight, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0, showBoundary = self.DEBUG)
			if Header_Footer:
				MyFrame.add(self.ChurchFlowable, pdf_TEST)
				MyFrame.add(Paragraph('Page ' + str(pdf_TEST.getPageNumber() - 1), self.styles['DaveHeaderLeft']), pdf_TEST)
			try:
				PageFull = False
				while not PageFull:
					if not MyFrame.add(SingleFlowable, pdf_TEST):
						PageFull = True
					else:
						Header_Footer = GeneratorHandle.next()
						SingleFlowable = GeneratorHandle.next()
			except:
				print "Ran out of Flowables"
			if self.DEBUG:
				print "Flowables Consumed TOTAL:", self.FlowablesConsumed
			NumberIConsumed = self.FlowablesConsumed - StartingFlowablesConsumed
			NumberRemaining = self.TotalFlowables - self.FlowablesConsumed
			FlowablesOnPages.append([pdf_TEST.getPageNumber() - 1, StartingFlowablesConsumed, NumberIConsumed, NumberRemaining])
			#END BUILDING THE TEST FRAME
			pdf_TEST.showPage()
		if self.DEBUG:
			pdf_TEST.save()

		UsedFaces = len(FlowablesOnPages)
		if self.DEBUG:
			print str(UsedFaces) + " faces are present"
		Fillers = (4 - UsedFaces % 4) % 4
		if self.DEBUG:
			print str(Fillers) + " blank faces will be added to make full pages"
		for Count in range(Fillers):
			FlowablesOnPages.insert(-4, [-1, 0, len(self.PrepareFiller()), 0])
		PageCount = (UsedFaces + Fillers) / 4
		if self.DEBUG:
			print str(PageCount) + " slices of paper per directory are needed"

		if self.DEBUG:
			print "Before Flowable Filler Addition"
			for Item in FlowablesOnPages:
				print Item

		##Insert filler flowables
		for Count in range(Fillers):
			self.SuffixFlowables = self.PrepareFiller() + self.SuffixFlowables

		##Renumber FamiliesOnPages
		NewPageCounts = []
		Remaining = FlowablesOnPages[0][2] + FlowablesOnPages[0][3] + Fillers
		Used = 0
		PageCounter = 0
		for item in FlowablesOnPages:
			Remaining -= item[2]
			NewPageCounts.append([PageCounter, Used, item[2], Remaining])
			Used += item[2]
			PageCounter += 1
		self.FlowablesOnPages = NewPageCounts

		if self.DEBUG:
			print "After Flowable Filler Addition"
			for Item in self.FlowablesOnPages:
				print Item

	def GeneratePDFDocs(self):
		##Print to PDF using the correct formats now and the correct page ordering
		FrontPageLayout = []
		BackPageLayout = []
		NormalPageLayout = []
		Sides = (self.FlowablesOnPages[-1][0]+1) / 2
		for pageside in range(Sides):
			NormalPageLayout.append([pageside*2, pageside*2 + 1])
			if pageside < Sides / 2:
				FrontPageLayout.append([(Sides * 2 - 1) - 2 * pageside, pageside * 2])
				BackPageLayout.append([pageside * 2 + 1, Sides * 2 - 2 - 2 * pageside])
		if self.DEBUG:
			print FrontPageLayout
			print BackPageLayout
			print NormalPageLayout

		pdf = Canvas(self.filename, pagesize = landscape(letter))
		pdf.setAuthor('David Ernstrom')
		pdf.setTitle('Ward Directory')
		pdf.setSubject('Subject Line')
		pdf.setFont('Helvetica', 18)
		
		pdf_FRONT = Canvas(self.front, pagesize = landscape(letter))
		pdf_FRONT.setAuthor('David Ernstrom')
		pdf_FRONT.setTitle('Ward Directory')
		pdf_FRONT.setSubject('Subject Line')
		pdf_FRONT.setFont('Helvetica', 18)

		pdf_BACK = Canvas(self.back, pagesize = landscape(letter))
		pdf_BACK.setAuthor('David Ernstrom')
		pdf_BACK.setTitle('Ward Directory')
		pdf_BACK.setSubject('Subject Line')
		pdf_BACK.setFont('Helvetica', 18)

		ThingsToPrint = []
		if self.Full:
			ThingsToPrint.append([NormalPageLayout, pdf])
		if self.Booklet:
			ThingsToPrint.append([FrontPageLayout, pdf_FRONT])
			ThingsToPrint.append([BackPageLayout, pdf_BACK])

		for PrintJob in ThingsToPrint:
			for page in PrintJob[0]:
				LeftFrame = Frame(self.FarLeft, self.Bottom, self.FrameWidth, self.FrameHeight, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0, showBoundary = self.DEBUG)
				RightFrame = Frame(self.NotSoFarLeft, self.Bottom, self.FrameWidth, self.FrameHeight, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0, showBoundary = self.DEBUG)

				MyLeftFrame = page[0]
				MyRightFrame = page[1]

				LeftFrameStartFlowable = self.FlowablesOnPages[MyLeftFrame][1]
				LeftFrameFlowablesConsumed = self.FlowablesOnPages[MyLeftFrame][2]
				if LeftFrameStartFlowable < len(self.PrefixFlowables):
					LeftHandle = self.PrefixFlowables
					Left_Header_Footer = False
				elif LeftFrameStartFlowable < len(self.CurrentWardDirectory) + len(self.PrefixFlowables):
					LeftHandle = self.CurrentWardDirectory
					LeftFrameStartFlowable -= len(self.PrefixFlowables)
					Left_Header_Footer = True
				else:
					LeftHandle = self.SuffixFlowables
					LeftFrameStartFlowable -= len(self.PrefixFlowables) + len(self.CurrentWardDirectory)
					Left_Header_Footer = False

				#DO THE LEFT PANEL PRINTING
				if Left_Header_Footer:
					LeftFrame.add(Paragraph('Page ' + str(MyLeftFrame), self.styles['DaveHeaderLeft']), PrintJob[1])
				LeftFrame.addFromList(LeftHandle[LeftFrameStartFlowable:LeftFrameStartFlowable + LeftFrameFlowablesConsumed], PrintJob[1])
				if Left_Header_Footer:
					LeftFrame.add(self.ChurchFlowable, PrintJob[1])

				RightFrameStartFlowable = self.FlowablesOnPages[MyRightFrame][1]
				RightFrameFlowablesConsumed = self.FlowablesOnPages[MyRightFrame][2]
				if RightFrameStartFlowable < len(self.PrefixFlowables):
					RightHandle = self.PrefixFlowables
					Right_Header_Footer = False
				elif RightFrameStartFlowable < len(self.CurrentWardDirectory) + len(self.PrefixFlowables):
					RightHandle = self.CurrentWardDirectory
					RightFrameStartFlowable -= len(self.PrefixFlowables)
					Right_Header_Footer = True
				else:
					RightHandle = self.SuffixFlowables
					RightFrameStartFlowable -= len(self.PrefixFlowables) + len(self.CurrentWardDirectory)
					Right_Header_Footer = False

				#DO THE RIGHT PANEL PRINTING
				if Right_Header_Footer:
					RightFrame.addFromList([Paragraph('Page ' + str(MyRightFrame), self.styles['DaveHeaderRight'])], PrintJob[1])
				RightFrame.addFromList(RightHandle[RightFrameStartFlowable:RightFrameStartFlowable + RightFrameFlowablesConsumed], PrintJob[1])
				if not RightFrameFlowablesConsumed == 1:
					RightFrame.addFromList([self.ChurchFlowable], PrintJob[1])

				PrintJob[1].showPage()
			print "PDF Completed"
			try:
				PrintJob[1].save()
			except IOError:
				os.mkdir(win32api.GetEnvironmentVariable('APPDATA') + os.sep + APPDATAFOLDER)
				PrintJob[1].save()

		#os.system('\"' + self.filename + '\"')

	def TableizeFamily(self, Household):
		Family = []
		if self.DEBUG:
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
			FamilyPicture = Image(self.ImagesFolder + os.sep + Household[3],
								  width = 1.5 * inch,
								  height = 1.125 * inch,
								  kind = 'proportional')
			if self.DEBUG:
				print self.ImagesFolder + os.sep + Household[3]
		except:
			FamilyPicture = Image(self.ImagesFolder + os.sep + 'Missing.jpg',
								  width = 1.5 * inch,
								  height = 1.125 * inch,
								  kind = 'proportional')
			if self.DEBUG:
				print self.ImagesFolder + os.sep + 'Missing.jpg'
		FamilyPicture.drawWidth = 1.5 * inch

		#Add the family Members
		CurrentRow = 0
		if self.DEBUG:
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
