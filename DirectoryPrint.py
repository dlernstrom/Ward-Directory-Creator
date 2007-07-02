import wx
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle, Image, Frame, Spacer, Preformatted
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm, inch, pica
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import time
import win32api
import os
import re
from Email import mail
import csv
import datetime
import CSVMembershipParser
import PDFTools

SEND_EMAILS = 0
SMTP_SERVER = 'smtp.forward.email.dupont.com'
#SMTP_SERVER = 'smtp.comcast.net'
APPDATAFOLDER = 'Ward Directory'
DEBUG = 0
MISSING_PEOPLE_EMAILS = ['david.ernstrom@usa.dupont.com', 'tina@ernstrom.net', 'david@ernstrom.net']
DIRECTORY_IMAGES = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\WardPictures\\'
CSV_LOCATION = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\'

class PDFPrint:
	def __init__(self, parent, filename, front, back, test):
		filename = win32api.GetEnvironmentVariable('APPDATA') + os.sep + APPDATAFOLDER + os.sep + filename
		front = win32api.GetEnvironmentVariable('APPDATA') + os.sep + APPDATAFOLDER + os.sep + front
		back = win32api.GetEnvironmentVariable('APPDATA') + os.sep + APPDATAFOLDER + os.sep + back
		test = win32api.GetEnvironmentVariable('APPDATA') + os.sep + APPDATAFOLDER + os.sep + test
		pdf_TEST = Canvas(test, pagesize = landscape(letter))
		pdf_TEST.setAuthor('David Ernstrom')
		pdf_TEST.setTitle('Ward Directory')
		pdf_TEST.setSubject('Subject Line')
		pdf = Canvas(filename, pagesize = landscape(letter))
		pdf.setAuthor('David Ernstrom')
		pdf.setTitle('Ward Directory')
		pdf.setSubject('Subject Line')
		pdf_FRONT = Canvas(front, pagesize = landscape(letter))
		pdf_FRONT.setAuthor('David Ernstrom')
		pdf_FRONT.setTitle('Ward Directory')
		pdf_FRONT.setSubject('Subject Line')
		pdf_BACK = Canvas(back, pagesize = landscape(letter))
		pdf_BACK.setAuthor('David Ernstrom')
		pdf_BACK.setTitle('Ward Directory')
		pdf_BACK.setSubject('Subject Line')
		
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
		CurrentDocument = []
		PDFToolHandle = PDFTools.PDFTools(DEBUG, DIRECTORY_IMAGES)
		#########NOTICE THAT SPAN IS WRITTEN BASS ACKWARDS WITH COL,ROW
		#Here I start adding flowables
		NumberOfMembers = 0
		NumberOfHouseholds = 0
		MissingPictures = []
		MembershipList = CSVMembershipParser.CSVMembershipParser(CSV_LOCATION + "Greenfield Ward member directory.csv")
		for Household in MembershipList.next():
			NumberOfHouseholds += 1
			NumberOfMembers += len(Household[1][0]) + len(Household[1][1])
			MasterTable = PDFToolHandle.TableizeFamily(Household)
			CurrentDocument.append(MasterTable)
			print str(len(CurrentDocument)), Household[0]
			print '------------------------------------------'

		CurrentDocument.append(Paragraph(str(NumberOfHouseholds) + ' Total Families', styles['DaveFooter']))
		CurrentDocument.append(Paragraph(str(NumberOfMembers) + ' Total Individuals', styles['DaveFooter']))

		Margin = .25 * inch
		Bottom = Margin
		FarLeft = Margin
		NotSoFarLeft = landscape(letter)[0]/2 + Margin
		FrameWidth = landscape(letter)[0]/2 - 2 * Margin
		FrameHeight = landscape(letter)[1] - 2 * Margin

		#Let's make some stock flowables for 'FOR CHURCH USE ONLY' and 'PAGE NUMBER'
		ChurchFlowable = Paragraph('For Church Use Only', styles['DaveFooter'])
		CurrentDocument.insert(0, Image(DIRECTORY_IMAGES + '001.jpg', width=FrameWidth, height=FrameHeight))
		CurrentDocument.insert(0, Image(DIRECTORY_IMAGES + '000.jpg', width=FrameWidth, height=FrameHeight))
		CurrentDocument.append(Image(DIRECTORY_IMAGES + '-003.jpg', width=FrameWidth, height=FrameHeight))
		CurrentDocument.append(Image(DIRECTORY_IMAGES + '-002.jpg', width=FrameWidth, height=FrameHeight))
		CurrentDocument.append(Image(DIRECTORY_IMAGES + '-001.jpg', width=FrameWidth, height=FrameHeight))
		CurrentDocument.append(Image(DIRECTORY_IMAGES + '-000.jpg', width=FrameWidth, height=FrameHeight))

		##Make a backup of the current document
		FlowableBackup = []
		for myFlowable in CurrentDocument:
			FlowableBackup.append(myFlowable)

		##THE NEXT LOOP IS TO GET THE COUNTS OF HOW MANY PAGES I'LL END UP WITH AND HOW MANY FLOWABLES WILL FALL ONTO EACH PAGE
		CurrentPage = -1
		FamiliesOnPages = []
		TotalFlowables = len(CurrentDocument)
		while len(CurrentDocument):
			LeftFrame = Frame(FarLeft, Bottom, FrameWidth, FrameHeight, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0, showBoundary = DEBUG)
			RightFrame = Frame(NotSoFarLeft, Bottom, FrameWidth, FrameHeight, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0, showBoundary = DEBUG)
			CurrentPage += 1
			print len(CurrentDocument)
			Start = len(CurrentDocument)
			if CurrentPage >= 2 and len(CurrentDocument) > 4:
				LeftFrame.addFromList([ChurchFlowable], pdf_TEST)
				LeftFrame.addFromList([Paragraph('Page ' + str(CurrentPage), styles['DaveHeaderLeft'])], pdf_TEST)
			LeftFrame.addFromList(CurrentDocument, pdf_TEST)
			FamiliesOnPages.append([CurrentPage, TotalFlowables - Start, Start - len(CurrentDocument), len(CurrentDocument)])

			if len(CurrentDocument) == 0:
				continue

			CurrentPage += 1
			Start = len(CurrentDocument)
			if CurrentPage >= 2 and len(CurrentDocument) > 4:
				RightFrame.addFromList([ChurchFlowable], pdf_TEST)
				RightFrame.addFromList([Paragraph('Page ' + str(CurrentPage), styles['DaveHeaderRight'])], pdf_TEST)
			RightFrame.addFromList(CurrentDocument, pdf_TEST)
			FamiliesOnPages.append([CurrentPage, TotalFlowables - Start, Start - len(CurrentDocument), len(CurrentDocument)])
			pdf_TEST.showPage()

		UsedFaces = CurrentPage + 1
		print str(UsedFaces) + " faces are present"
		Fillers = 4 - UsedFaces % 4
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
			FlowableBackup.insert(-4, Image(DIRECTORY_IMAGES + 'blank.jpg', width=FrameWidth, height=FrameHeight))

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
		FamiliesOnPages = NewPageCounts

		##Recover From Flowable Backup
		CurrentDocument = []
		for myFlowable in FlowableBackup:
			CurrentDocument.append(myFlowable)

		print len(CurrentDocument)

		print "After Flowable Filler Addition"
		for Item in FamiliesOnPages:
			print Item

		##Print to PDF using the correct formats now and the correct page ordering
		FrontPageLayout = []
		BackPageLayout = []
		NormalPageLayout = []
		for pageside in range(PageCount * 2):
			NormalPageLayout.append([pageside*2, pageside*2 + 1])
			if pageside < PageCount:
				FrontPageLayout.append([(PageCount * 4 - 1) - 2 * pageside, pageside * 2])
				BackPageLayout.append([pageside * 2 + 1, PageCount * 4 - 2 - 2 * pageside])
		print FrontPageLayout
		print BackPageLayout
		print NormalPageLayout

		ThingsToPrint = [[NormalPageLayout, pdf],
						 [FrontPageLayout, pdf_FRONT],
						 [BackPageLayout, pdf_BACK]]

		for PrintJob in ThingsToPrint:
			for page in PrintJob[0]:
				LeftFrame = Frame(FarLeft, Bottom, FrameWidth, FrameHeight, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0, showBoundary = DEBUG)
				RightFrame = Frame(NotSoFarLeft, Bottom, FrameWidth, FrameHeight, leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0, showBoundary = DEBUG)

				MyLeftFrame = page[0]
				MyRightFrame = page[1]

				LeftFrameStartFlowable = FamiliesOnPages[MyLeftFrame][1]
				LeftFrameFlowablesConsumed = FamiliesOnPages[MyLeftFrame][2]

				RightFrameStartFlowable = FamiliesOnPages[MyRightFrame][1]
				RightFrameFlowablesConsumed = FamiliesOnPages[MyRightFrame][2]

				if not LeftFrameFlowablesConsumed == 1:
					LeftFrame.addFromList([Paragraph('Page ' + str(MyLeftFrame), styles['DaveHeaderLeft'])], PrintJob[1])

				LeftFrame.addFromList(CurrentDocument[LeftFrameStartFlowable:LeftFrameStartFlowable + LeftFrameFlowablesConsumed], PrintJob[1])

				if not LeftFrameFlowablesConsumed == 1:
					LeftFrame.addFromList([ChurchFlowable], PrintJob[1])


				if not RightFrameFlowablesConsumed == 1:
					RightFrame.addFromList([Paragraph('Page ' + str(MyRightFrame), styles['DaveHeaderRight'])], PrintJob[1])

				RightFrame.addFromList(CurrentDocument[RightFrameStartFlowable:RightFrameStartFlowable + RightFrameFlowablesConsumed], PrintJob[1])

				if not RightFrameFlowablesConsumed == 1:
					RightFrame.addFromList([ChurchFlowable], PrintJob[1])

				#page[0] is the left side
				if page[0] == 0:
					CurrentDateString = datetime.date.today().strftime("%d %B %Y")
					print CurrentDateString
					PrintJob[1].drawString(FarLeft + FrameWidth/2, 75, CurrentDateString)
				if page[1] == 0:
					CurrentDateString = datetime.date.today().strftime("%d %B %Y")
					print CurrentDateString
					PrintJob[1].drawString(NotSoFarLeft + FrameWidth/2, 75, CurrentDateString)
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
		message = "The following " + str(len(MissingPictures)) + " people are missing pictures\n\n"
		for Name in MissingPictures:
			message += Name + '\n'
		print message
		if SEND_EMAILS:
			for ToAddy in MISSING_PEOPLE_EMAILS:
				mail(SMTP_SERVER, 'David@Ernstrom.net', ToAddy, 'Missing Picture', message)
		Handle = open(CSV_LOCATION + "Needed.txt", 'w')
		Handle.write(message)
		Handle.close()
		os.system('\"' + filename + '\"')

class MyFrame(wx.Frame):
	def __init__(
			self, parent, ID, title, pos=wx.DefaultPosition,
			size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE
			):
		wx.Frame.__init__(self, parent, ID, title, pos, size, style)

		panel = wx.Panel(self, -1, style = wx.TAB_TRAVERSAL
						 | wx.CLIP_CHILDREN
						 | wx.FULL_REPAINT_ON_RESIZE
						 )

		gbs = self.gbs = wx.GridBagSizer(15, 6)

		Title = wx.StaticText(panel, -1, "Ward Photo Directory Printing Tool")
		Title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		gbs.Add( Title, (0,0), (1,6), wx.ALIGN_CENTER, wx.ALL, 5)

		PrintButton = wx.Button(panel, -1, "Print")
		gbs.Add(PrintButton, (5, 5))

		gbs.AddGrowableRow(14)
		gbs.AddGrowableCol(0)
		gbs.AddGrowableCol(5)

		panel.SetSizerAndFit(gbs)
		self.SetClientSize(panel.GetSize())

		self.Bind(wx.EVT_BUTTON, self.OnDoPrint, PrintButton)
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)


	def OnCloseWindow(self, event):
		self.Destroy()

	def OnDoPrint(self, event):
		#print self.TableData
		PDFPrint(self, 'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '.pdf',
				 'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '_FRONT.pdf',
				 'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '_BACK.pdf',
				 'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '_TEST.pdf'
				 )

class MyApp(wx.App):
	def OnInit(self):
		win = MyFrame(None, -1, "Ward Photo Directory Printing/Configuration Utility", size=wx.DefaultSize,
				style = wx.DEFAULT_FRAME_STYLE)
		win.Show(True)
		return True

if __name__ == '__main__':
	app = MyApp(False)
	app.MainLoop()

