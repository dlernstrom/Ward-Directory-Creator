# PDFTools.py
import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle, Image, Frame, Spacer, Preformatted, PageBreak
from reportlab.platypus.flowables import HRFlowable, KeepInFrame, ImageAndFlowables
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import time
import datetime
from RotatedTable import RotatedTable90, RotatedTable270
from TextOnImage import TextOnImage

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
		#self.DEBUG = 1
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
								  leading = 1.5 * 8
								  ))
		self.styles.add(ParagraphStyle(name='DaveBold',
								  parent=self.styles['DaveHeading'],
								  fontName = 'Times-Bold',
								  fontSize = 10,
								  leading = 1.5 * 10
								  ))
		self.styles.add(ParagraphStyle(name='DaveBoldSmall',
								  parent=self.styles['DaveBold'],
								  fontSize = 8,
								  leading = 1.5 * 8
								  ))
		self.styles.add(ParagraphStyle(name = 'TextOnImage',
									   parent = self.styles['DaveBoldSmall'],
									   fontSize = 7,
									   leading = 1.2 * 7,
									   leftIndent = .06 * inch,
									   rightIndent = .2 * inch,
									   alignment = TA_CENTER
									   ))

		self.CurrentWardDirectory = []

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

	def _MakeBoxes(self, StartRow, StartCol, BoxCount):
		ReturnList = []
		for Counter in range(BoxCount):
			ReturnList.append(('BOX', (StartCol + 2 * Counter, StartRow), (StartCol + 2 * Counter, StartRow), .25, colors.black))
		return ReturnList

	def _GetChangeForm(self):
		ColumnWidths = []
		myTableData = []
		myTableData2 = []
		#Currently set up for 20 rows
		RowHeights = []
		BoxHeight = .25 * inch
		SpacerHeight = .05 * inch
		TextHeight = .25 * inch
		RowHeights.append(TextHeight)		# First Name, Date
		RowHeights.append(BoxHeight)		# Boxes
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(TextHeight)		# Last Name, Phone Number
		RowHeights.append(BoxHeight)		# Boxes
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(TextHeight)		# Please describe the problem for us...
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes Row 1
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes Row 2
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes Row 3
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes Row 4
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes Row 5
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes Row 6
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes Row 7
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes Row 8
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes Row 9
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes Row 10
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes Row 11
		BoxWidth = .2 * inch
		SpacerWidth = .05 * inch
		ColumnSetCount = 27
		ColumnSet = [SpacerWidth, BoxWidth]
		ColumnWidths = ColumnSet * ColumnSetCount + [SpacerWidth]
		BlankRow = [''] * len(ColumnWidths)
		myTableData = []
		for Counter in range(len(RowHeights)):
			myTableData.append(BlankRow[:])
		myTableData[0][1]   = 'First Name'
		myTableData[0][35]  = "Today's Date (mm/dd/yyyy)"
		myTableData[1][38]  = '/'
		myTableData[1][42]  = '/'
		myTableData[1][43]  = "2"
		myTableData[1][45]  = "0"
		myTableData[3][1]   = "Last Name"
		myTableData[3][35]  = "Phone Number"
		myTableData[4][34]  = '('
		myTableData[4][40]  = ')'
		myTableData[4][46]  = '-'
		myTableData[8][1]   = 'Please describe the problem(s) as detailed as possible'

		TableStyleData = []
		TableStyleData += self._MakeBoxes( 1,  1, 16)
		TableStyleData += self._MakeBoxes( 4,  1, 16)
		TableStyleData += self._MakeBoxes( 1, 35,  8)
		TableStyleData += self._MakeBoxes( 4, 35, 10)
		if self.DEBUG:
			TableStyleData += [('BOX', (0,0), (-1,-1), .25, colors.black)]
		TableStyleData += [('ALIGN', (0,1), (-1,1), 'CENTER')]
		TableStyleData += [('ALIGN', (0,4), (-1,4), 'CENTER')]
		TableStyleData += [('LINEBELOW', (0,10), (-1,10), .25, colors.black),
						   ('LINEBELOW', (0,12), (-1,12), .25, colors.black),
						   ('LINEBELOW', (0,14), (-1,14), .25, colors.black),
						   ('LINEBELOW', (0,16), (-1,16), .25, colors.black),
						   ('LINEBELOW', (0,18), (-1,18), .25, colors.black),
						   ('LINEBELOW', (0,20), (-1,20), .25, colors.black),
						   ('LINEBELOW', (0,22), (-1,22), .25, colors.black),
						   ('LINEBELOW', (0,24), (-1,24), .25, colors.black),
						   ('LINEBELOW', (0,26), (-1,26), .25, colors.black),
						   ('LINEBELOW', (0,28), (-1,28), .25, colors.black)]

		myTableStyle = TableStyle(TableStyleData)
		return myTableData, RowHeights, ColumnWidths, myTableStyle

	def _GetRequestForm(self):
		ColumnWidths = []
		myTableData = []
		myTableData2 = []
		#Currently set up for 20 rows
		RowHeights = []
		BoxHeight = .25 * inch
		SpacerHeight = .05 * inch
		TextHeight = .25 * inch
		RowHeights.append(TextHeight)		# Last Name
		RowHeights.append(BoxHeight)		# Boxes
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(TextHeight)		# Parents First and middle names
		RowHeights.append(BoxHeight)		# Boxes
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(TextHeight)		# Children's First and Middle Names
		RowHeights.append(BoxHeight)		# Boxes Child 1
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes Child 2
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes Child 3
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes Child 4
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(BoxHeight)		# Boxes Child 5
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(TextHeight)		# Phone Numbers
		RowHeights.append(BoxHeight)		# Boxes
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(TextHeight)		# Address
		RowHeights.append(BoxHeight)		# Boxes
		RowHeights.append(SpacerHeight)		# Gap
		RowHeights.append(TextHeight)		# Email Address
		RowHeights.append(BoxHeight)		# Boxes
		BoxWidth = .2 * inch
		SpacerWidth = .05 * inch
		ColumnSetCount = 27
		ColumnSet = [SpacerWidth, BoxWidth]
		ColumnWidths = ColumnSet * ColumnSetCount + [SpacerWidth]
		BlankRow = [''] * len(ColumnWidths)
		RowCount = 27
		myTableData = []
		for Counter in range(RowCount):
			myTableData.append(BlankRow[:])
		myTableData[0][1]   = 'Last Name'
		myTableData[0][39]  = "Today's Date (mm/dd/yyyy)"
		myTableData[1][42]  = '/'
		myTableData[1][46]  = '/'
		myTableData[1][47]  = "2"
		myTableData[1][49]  = "0"
		myTableData[3][1]   = "Parent's First & Middle Names"
		myTableData[3][39]  = "Birth Date (mm/dd/yyyy)"
		myTableData[4][42]  = '/'
		myTableData[4][46]  = '/'
		myTableData[4][47]  = "1"
		myTableData[4][49]  = "9"
		myTableData[6][42]  = '/'
		myTableData[6][46]  = '/'
		myTableData[6][47]  = "1"
		myTableData[6][49]  = "9"
		myTableData[8][1]   = "Children's First & Middle Names"
		myTableData[8][39]  = "Birth Date (mm/dd/yyyy)"
		myTableData[9][42]  = '/'
		myTableData[9][46]  = '/'
		myTableData[11][42] = '/'
		myTableData[11][46] = '/'
		myTableData[13][42] = '/'
		myTableData[13][46] = '/'
		myTableData[15][42] = '/'
		myTableData[15][46] = '/'
		myTableData[17][42] = '/'
		myTableData[17][46] = '/'
		myTableData[19][1]  = 'Primary Phone Number'
		myTableData[20][0]  = '('
		myTableData[20][6]  = ')'
		myTableData[20][12] = '-'
		myTableData[20][22] = '('
		myTableData[20][28] = ')'
		myTableData[20][34] = '-'
		myTableData[19][23] = 'Secondary Phone Number'
		myTableData[22][1]  = 'Street Address'
		myTableData[22][45] = 'Apartment'
		myTableData[25][1]  = 'Email Address'

		TableStyleData = []
		TableStyleData += self._MakeBoxes( 1,  1, 18)
		TableStyleData += self._MakeBoxes( 4,  1, 18)
		TableStyleData += self._MakeBoxes( 6,  1, 18)
		TableStyleData += self._MakeBoxes( 9,  1, 18)
		TableStyleData += self._MakeBoxes(11,  1, 18)
		TableStyleData += self._MakeBoxes(13,  1, 18)
		TableStyleData += self._MakeBoxes(15,  1, 18)
		TableStyleData += self._MakeBoxes(17,  1, 18)
		TableStyleData += self._MakeBoxes( 1, 39,  8)
		TableStyleData += self._MakeBoxes( 4, 39,  8)
		TableStyleData += self._MakeBoxes( 6, 39,  8)
		TableStyleData += self._MakeBoxes( 9, 39,  8)
		TableStyleData += self._MakeBoxes(11, 39,  8)
		TableStyleData += self._MakeBoxes(13, 39,  8)
		TableStyleData += self._MakeBoxes(15, 39,  8)
		TableStyleData += self._MakeBoxes(17, 39,  8)
		TableStyleData += self._MakeBoxes(20,  1, 10)
		TableStyleData += self._MakeBoxes(20, 23, 10)
		TableStyleData += self._MakeBoxes(23,  1, 21)
		TableStyleData += self._MakeBoxes(23, 45,  5)
		TableStyleData += self._MakeBoxes(26,  1, 27)
		if self.DEBUG:
			TableStyleData += [('BOX', (0,0), (-1,-1), .25, colors.black)]
		TableStyleData += [('ALIGN', (42,0), (-1,18), 'CENTER')]
		TableStyleData += [('ALIGN', (0,20), (-1,20), 'CENTER')]

		myTableStyle = TableStyle(TableStyleData)
		return myTableData, RowHeights, ColumnWidths, myTableStyle

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
		self.PrefixFlowables = []
		#Page 1 Data
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
				if aFlowable.__class__ is Paragraph or aFlowable.__class__ is Spacer:
					aFlowable._showBoundary = 1

	def _RecordRequestPage(self, rotation = '90'):
		self.SuffixFlowables.append(Paragraph(text = "Record Request Form", style = self.styles['Subtitle']))
		RecordRequestTextA = """<i>To have your records requested into our ward, please fill out this form,
		remove it from the directory, and turn it in to a member of the Bishopric or the Membership Clerk.</i>"""
		RecordRequestTextB = """<i>We will contact you with any questions.</i>"""
		RecordRequestTextC = """<i>Please be sure to have your picture taken so that your family
		shows up in the next publication of this directory.</i>"""
		self.SuffixFlowables.append(Paragraph(text = RecordRequestTextA, style = self.styles['RegText']))
		self.SuffixFlowables.append(Paragraph(text = RecordRequestTextB, style = self.styles['RegText']))
		myTableData, RowHeights, ColumnWidths, myTableStyle = self._GetRequestForm()
		if rotation == '90':
			myRotatedTable = RotatedTable90(myTableData, colWidths = ColumnWidths, rowHeights = RowHeights, hAlign = 'RIGHT')
		else:
			myRotatedTable = RotatedTable270(myTableData, colWidths = ColumnWidths, rowHeights = RowHeights, hAlign = 'LEFT')
		myRotatedTable.setStyle(myTableStyle)
		self.SuffixFlowables.append(myRotatedTable)
		self.SuffixFlowables.append(Paragraph(text = RecordRequestTextC, style = self.styles['RegText']))
		self.SuffixFlowables.append(PageBreak())

	def _ChangeRequestPage(self, rotation = '90'):
		self.SuffixFlowables.append(Paragraph(text = "Change Request Form", style = self.styles['Subtitle']))
		RecordRequestTextA = """<i>If you notice any incorrect or missing information in this directory, please fill
		out the form below and return it to a member of the Bishopric or the Membership Clerk.</i>"""
		RecordRequestTextB = """<i>We will contact you with any questions.</i>"""
		RecordRequestTextC = """<i>Please note that only one phone number can be displayed in the directory
		per family.  Email addresses can only be changed by you through the ward website.</i>"""
		self.SuffixFlowables.append(Paragraph(text = RecordRequestTextA, style = self.styles['RegText']))
		self.SuffixFlowables.append(Paragraph(text = RecordRequestTextB, style = self.styles['RegText']))
		myTableData, RowHeights, ColumnWidths, myTableStyle = self._GetChangeForm()
		if rotation == '90':
			myRotatedTable = RotatedTable90(myTableData, colWidths = ColumnWidths, rowHeights = RowHeights, hAlign = 'RIGHT')
		else:
			myRotatedTable = RotatedTable270(myTableData, colWidths = ColumnWidths, rowHeights = RowHeights, hAlign = 'LEFT')
		myRotatedTable.setStyle(myTableStyle)
		self.SuffixFlowables.append(myRotatedTable)
		self.SuffixFlowables.append(Paragraph(text = RecordRequestTextC, style = self.styles['RegText']))
		self.SuffixFlowables.append(PageBreak())


	def AddDirectorySuffixData(self):
		self.SuffixFlowables = []

		#Back side of get my records in!!!
		# GET MY RECORDS IN!!!
		self._RecordRequestPage(rotation = '90')

		# GET MY RECORDS IN!!!
		self._ChangeRequestPage(rotation = '270')

		#How to access the ward website
		#self.SuffixFlowables.append(Image(self.ImagesFolder + os.sep + '-001.jpg', width=self.FrameWidth, height=self.FrameHeight))
		Instructions = ["""<para spaceb=10>1 - Go to <b>www.lds.org/units</b>.'</para>""",
						"""<para spaceb=10>2 - Click on "Register or Sign In." </para>""",
						"""<para spaceb=10>3 - If you already have an account, enter your username and password.  If not, click on
						"obtain an account" to set one up.</para>""",
						"""<para spaceb=10>4 - Creating an account: Once you've clicked on 'obtain an account' you will be
						asked to fill out a brief form.  You will need your <b>membership record number</b> and
						your <b>confirmation date</b>.  Both can be found on your Individual Ordinace Summary
						(see below) - if you don't have a copy, please see the Ward Clerk.</para>""",
						"""<para spaceb=10>When creating your account you will create a username and password that you can use to login
						to the website in the future.</para>""",
						"""<para spaceb=10>The information in the membership directory on the website comes straight from church
						records.  So when you move, your profile automatically moves to your new ward.</para>""",
						"""<para spaceb=10>5 - It's that easy!  Just follow the on screen prompts and your account will be setup in
						no time.  When you are ready to login again, return to www.lds.org/units.</para>""",
						"""<para spaceb=10>From the ward website, you will be able to view membership directories for all wards
						in the stake, stake and ward calendars, and lesson schedules.  When creating your
						account, if you enter an email address, you can receive information about
						upcoming stake and ward calendar items in your email inbox.</para>"""]
		ContentParagraphs = []
		for Instruction in Instructions:
			ContentParagraphs.append(Paragraph(text = Instruction, style = self.styles['RegTextL']))
		self.SuffixFlowables.append(Paragraph(text = "Accessing the Ward Website", style = self.styles['QuoteTitle']))
		Web1 = Image(self.ImagesFolder + os.sep + 'wardWeb1.jpg',
									  width = self.FrameWidth,
									  height = 1.0 * inch,
									  kind = 'proportional')
		Web1.hAlign = 'LEFT'
		Web2 = Image(self.ImagesFolder + os.sep + 'wardWeb2.jpg',
									  width = self.FrameWidth,
									  height = 1.5 * inch,
									  kind = 'proportional')
		Web2.hAlign = 'LEFT'
		Web3 = Image(self.ImagesFolder + os.sep + 'wardWeb3.jpg',
									  width = 2.0 * inch,
									  height = 2.0 * inch,
									  kind = 'proportional')
		Web3.hAlign = 'LEFT'
		AccessingSiteContent = ContentParagraphs[:2]
		AccessingSiteContent.extend([Web1, ContentParagraphs[2], Web2, ContentParagraphs[3]])
		AccessingSiteContent.append(ImageAndFlowables(Web3, ContentParagraphs[4:6], imageLeftPadding=0,
													  imageRightPadding=0, imageTopPadding=0, imageBottomPadding=0,
													  imageSide='left'))
		AccessingSiteContent.extend(ContentParagraphs[6:])
		AccessingSiteContent.append(PageBreak())
		self.SuffixFlowables.append(KeepInFrame(maxWidth = self.FrameWidth,
												maxHeight = self.FrameHeight,
												content = AccessingSiteContent,
												mode = 'truncate'))

		##########################################
		## LAST PAGE DATA
		#Here, we'll add our comment and disclaimer data to the end of the document
		self.SuffixFlowables.append(Spacer(width = self.FrameWidth, height = 2.0 * inch))
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
		#############################################
		## END OF SUFFIX DATA

		if self.DEBUG:
			for aFlowable in self.SuffixFlowables:
				if aFlowable.__class__ is Paragraph or aFlowable.__class__ is Spacer:
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
		self.CurrentWardDirectory.append(PageBreak())
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
				print "Total Flowables:", self.TotalFlowables
				print "Total Consumed:", self.FlowablesConsumed
				if self.FlowablesConsumed < self.TotalFlowables:
					raise "PROBLEM!"
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

		FooterRoom = self.ChurchFlowable.wrap(self.FrameWidth, self.FrameHeight)[1] + self.ChurchFlowable.getSpaceBefore()
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
					content = [Paragraph('Page ' + str(MyLeftFrame), self.styles['DaveHeaderLeft'])] + LeftHandle[LeftFrameStartFlowable:LeftFrameStartFlowable + LeftFrameFlowablesConsumed] + [Spacer(width = self.FrameWidth, height = 9 * inch)]
					LeftFrame.add(KeepInFrame(maxWidth = self.FrameWidth,
											  maxHeight = self.FrameHeight - FooterRoom,
											  content = content,
											  mode = 'truncate'), PrintJob[1])
					LeftFrame.add(self.ChurchFlowable, PrintJob[1])
				else:
					LeftFrame.addFromList(LeftHandle[LeftFrameStartFlowable:LeftFrameStartFlowable + LeftFrameFlowablesConsumed], PrintJob[1])

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
					#RightFrame.addFromList(, PrintJob[1])
					content = [Paragraph('Page ' + str(MyRightFrame), self.styles['DaveHeaderRight'])] + RightHandle[RightFrameStartFlowable:RightFrameStartFlowable + RightFrameFlowablesConsumed] + [Spacer(width = self.FrameWidth, height = 9 * inch)]
					RightFrame.add(KeepInFrame(maxWidth = self.FrameWidth,
											   maxHeight = self.FrameHeight - FooterRoom,# 7.355 < x < 7.362
											   content = content,
											   mode = 'truncate'), PrintJob[1])
					RightFrame.add(self.ChurchFlowable, PrintJob[1])
				else:
					RightFrame.addFromList(RightHandle[RightFrameStartFlowable:RightFrameStartFlowable + RightFrameFlowablesConsumed], PrintJob[1])

				PrintJob[1].showPage()
			print "PDF Completed"
			PrintJob[1].save()

	def GetMissingName(self):
		ContactName = self.DictionaryData['missing.missingname']
		CommaIndex = ContactName.index(',')
		ContactName = ContactName[CommaIndex + 2:] + ' ' + ContactName[:CommaIndex]
		return ContactName


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
			FamilyPictureBase = Image(self.ImagesFolder + os.sep + 'Missing.jpg',
								  width = 1.5 * inch,
								  height = 1.125 * inch,
								  kind = 'proportional')
			MissingImageText = Paragraph(text = "Please contact " + self.GetMissingName() + " to have your photograph added", style = self.styles['TextOnImage'])
			FamilyPicture = TextOnImage(P = MissingImageText, I = FamilyPictureBase, xpad = 0, ypad = .05 * inch, side = 'center')
			if self.DEBUG:
				print self.ImagesFolder + os.sep + 'Missing.jpg'

		#########NOTICE THAT SPAN IS WRITTEN BASS ACKWARDS WITH COL,ROW
		self.TheTableStyle = TableStyle([('LEFTPADDING', (0,0), (-1,-1), 3),
										 ('RIGHTPADDING', (0,0), (-1,-1), 3),
										 ('BOTTOMPADDING', (0,0), (-1,-1), 0),
										 ('TOPPADDING', (1,0), (-1,-1), 0),
										 ('SPAN', (0,0), (2,0))
										 ])
		if self.DEBUG:
			self.TheTableStyle.add('INNERGRID', (0,0), (-1,-1), 0.25, colors.black)
			self.TheTableStyle.add('BOX', (0,0), (-1,-1), .25, colors.black)
		self.ImageStyle = TableStyle([('ALIGN', (0,0), (-1, -1), 'CENTER'),
									  ('LEFTPADDING', (0,0), (-1,-1), 0),
									  ('RIGHTPADDING', (0,0), (-1,-1), 0),
									  ('LEADING', (0,0), (-1,-1), 0)])
		self.CombinedStyle = TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'),
										 ('LINEBELOW', (0,0), (-1,-1), 1.0, colors.black),
										 ('LINEABOVE', (0,0), (-1,-1), 1.0, colors.black),
										 ('LEFTPADDING', (0,0), (-1,-1), 0),
										 ('RIGHTPADDING', (0,0), (-1,-1), 0),
										 ('BOTTOMPADDING', (0,0), (-1,-1), 0),
										 ('TOPPADDING', (0,0), (-1,-1), 0),
										 ('LEADING', (0,0), (-1,-1), 0),
										 ('ALIGN', (0,0), (-1, -1), 'CENTER'),
										 ('FONTSIZE', (0,0), (-1,-1), 0),
										 ])
		if self.DEBUG:
			self.CombinedStyle.add('INNERGRID', (0,0), (-1,-1), 0.25, colors.black)
			self.CombinedStyle.add('BOX', (0,0), (-1,-1), 0.25, colors.black)


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
		ImageTable = Table([[FamilyPicture]])
		ImageTable.setStyle(self.ImageStyle)
		CombinedTableData = [[TextTable, ImageTable]]
		MasterTable = Table(CombinedTableData, ['*', 1.6 * inch])
		MasterTable.setStyle(self.CombinedStyle)
		return MasterTable
