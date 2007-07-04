import wx
from ColoredPanel import *
import  wx.lib.filebrowsebutton as filebrowse

class DaveStaticBox(wx.StaticBox):
	def __init__(self, parent, id, Title):
		wx.StaticBox.__init__(self, parent, id, Title)
		self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		self.bg_bmp = parent.bg_bmp
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
		self.Bind(wx.EVT_PAINT, self.OnPaint)

	def OnPaint(self, evt):
		print "I'm painting"
		dc = wx.BufferedPaintDC(self, self.bg_bmp)

	# tile the background bitmap loaded in __init__()
	def DrawBackground(self, dc):
		dc.DrawBitmap(self.bg_bmp, 0, 0)

	# Redraw the background over a 'damaged' area.
	def OnEraseBackground(self, evt):
		print "I'm erasing"
		dc = evt.GetDC()

		if not dc:
			print "Not DC"
			dc = wx.ClientDC(self)
			rect = self.GetUpdateRegion().GetBox()
			dc.SetClippingRect(rect)
		self.DrawBackground(dc)

class MainPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, wx.BLUE)
		
		#st = wx.StaticText(self, -1,
		#		  "Title/Stuff goes here",
		#		  (10, 10))
		#st.SetForegroundColour(wx.WHITE)
		#st.SetBackgroundColour(wx.GREEN)

		self.gbs = gbs = wx.GridBagSizer(vgap = 5, hgap = 40)

		TitleFont = wx.Font(22, wx.DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, False, "Georgia")
		StandardFont = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Georgia")
		

		StaticHeading = wx.StaticText(self, -1,"Ward Directory Creator " + parent.parent.MajorAppVersion)
		StaticHeading.SetFont(TitleFont)
		gbs.Add(StaticHeading,
				pos = (0,0), span = (1,3), flag = wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_TOP)

		WardBox = wx.StaticBox(self, -1, "Ward/Branch Configuration")
		WardBox.SetFont(StandardFont)
		WardBoxSizer = wx.StaticBoxSizer(WardBox, wx.VERTICAL)

		StaticWardName = wx.StaticText(self, -1, "Ward Name:")
		StaticWardName.SetFont(StandardFont)
		#gbs.Add(StaticWardName,
		#		pos = (2,0), span = (1,1), flag = wx.ALIGN_LEFT)
		WardBoxSizer.Add(StaticWardName, 0, wx.TOP | wx.LEFT, 10)

		TXT_WardName = wx.TextCtrl(self, -1, size=(250,35))
		TXT_WardName.SetFont(StandardFont)
		#gbs.Add(TXT_WardName,
		#		pos = (2,1), span = (1,2), flag = wx.ALIGN_LEFT)
		WardBoxSizer.Add(TXT_WardName, 0, wx.TOP | wx.LEFT, 10)

		RB_Ward = wx.RadioButton(self, -1, "Ward", style = wx.RB_GROUP)
		RB_Ward.SetFont(StandardFont)
		#gbs.Add(RB_Ward,
		#		pos = (3,0), span = wx.DefaultSpan, flag = wx.ALIGN_CENTER_HORIZONTAL)
		WardBoxSizer.Add(RB_Ward, 0, wx.TOP | wx.LEFT, 10)

		RB_Branch = wx.RadioButton(self, -1, "Branch")
		RB_Branch.SetFont(StandardFont)
		#gbs.Add(RB_Branch,
		#		pos = (3,1), span = wx.DefaultSpan, flag = wx.ALIGN_LEFT)
		WardBoxSizer.Add(RB_Branch, 0, wx.TOP | wx.LEFT, 10)

		StaticStakeName = wx.StaticText(self, -1, "Stake Name:")
		StaticStakeName.SetFont(StandardFont)
		#gbs.Add(StaticStakeName,
		#		pos = (4,0), span = (1,1), flag = wx.ALIGN_LEFT)
		WardBoxSizer.Add(StaticStakeName, 0, wx.TOP | wx.LEFT, 10)

		TXT_StakeName = wx.TextCtrl(self, -1, size=(250,35))
		TXT_StakeName.SetFont(StandardFont)
		#gbs.Add(TXT_StakeName,
		#		pos = (4,1), span = (1,2), flag = wx.ALIGN_LEFT)
		WardBoxSizer.Add(TXT_StakeName, 0, wx.TOP | wx.LEFT, 10)

		gbs.Add(WardBoxSizer,
				pos = (1,0), span = (6,1), flag = wx.ALIGN_LEFT)

		QuoteBox = wx.StaticBox(self, -1, "Quote Configuration")
		QuoteBox.SetFont(StandardFont)
		QuoteBoxSizer = wx.StaticBoxSizer(QuoteBox, wx.VERTICAL)

		CB_UseQuote = wx.CheckBox(self, -1, "Use Quote")
		CB_UseQuote.SetFont(StandardFont)
		#gbs.Add(CB_UseQuote,
		#		pos = (6,0), span = (1,2), flag = wx.ALIGN_LEFT)
		QuoteBoxSizer.Add(CB_UseQuote, 0, wx.TOP | wx.LEFT, 10)

		StaticInspQuote = wx.StaticText(self, -1, "Inspirational Quote:")
		StaticInspQuote.SetFont(StandardFont)
		StaticInspQuote.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		#gbs.Add(StaticInspQuote,
		#		pos = (7,0), span = (1,2), flag = wx.ALIGN_LEFT)
		QuoteBoxSizer.Add(StaticInspQuote, 0, wx.TOP | wx.LEFT, 10)

		TXT_Quote = wx.TextCtrl(self, -1, size = (350, 105))
		TXT_Quote.SetFont(StandardFont)
		#gbs.Add(TXT_Quote,
		#		pos = (8,0), span = (1,4), flag = wx.ALIGN_LEFT)
		QuoteBoxSizer.Add(TXT_Quote, 0, wx.TOP | wx.LEFT, 10)

		StaticAuthor = wx.StaticText(self, -1, "Author:")
		StaticAuthor.SetFont(StandardFont)
		#gbs.Add(StaticAuthor,
		#		pos = (9,0), span = (1,1), flag = wx.ALIGN_LEFT)
		QuoteBoxSizer.Add(StaticAuthor, 0, wx.TOP | wx.LEFT, 10)

		TXT_Author = wx.TextCtrl(self, -1, size=(250,35))
		TXT_Author.SetFont(StandardFont)
		#gbs.Add(TXT_Author,
		#		pos = (9,1), span = (1,2), flag = wx.ALIGN_LEFT)
		QuoteBoxSizer.Add(TXT_Author, 0, wx.TOP | wx.LEFT, 10)

		BTN_RestoreQuote = wx.Button(self, -1, "Restore Default")
		BTN_RestoreQuote.SetFont(StandardFont)
		#gbs.Add(BTN_RestoreQuote,
		#		pos = (10,0), span = (1,2), flag = wx.ALIGN_LEFT)
		QuoteBoxSizer.Add(BTN_RestoreQuote, 0, wx.TOP | wx.LEFT, 10)

		gbs.Add(QuoteBoxSizer,
				pos = (1,1), span = (8,2), flag = wx.ALIGN_CENTER_HORIZONTAL)

		StaticBox = wx.StaticBox(self, -1, "Generate Directory")
		StaticBox.SetFont(StandardFont)
		StaticBoxSizer = wx.StaticBoxSizer(StaticBox, wx.VERTICAL)

		CB_SendEmail = wx.CheckBox(self, -1, "Send Missing Email")
		CB_SendEmail.SetFont(StandardFont)
		StaticBoxSizer.Add(CB_SendEmail, 0, wx.TOP | wx.LEFT, 10)

		CB_MissingReport = wx.CheckBox(self, -1, "Generate Missing Report")
		CB_MissingReport.SetFont(StandardFont)
		StaticBoxSizer.Add(CB_MissingReport, 0, wx.TOP | wx.LEFT, 10)

		CB_ExtractMoveOuts = wx.CheckBox(self, -1, "Extract Move Out Images")
		CB_ExtractMoveOuts.SetFont(StandardFont)
		StaticBoxSizer.Add(CB_ExtractMoveOuts, 0, wx.TOP | wx.LEFT, 10)

		CB_GenPDF_Full = wx.CheckBox(self, -1, "Gen. Full Spread PDF")
		CB_GenPDF_Full.SetFont(StandardFont)
		StaticBoxSizer.Add(CB_GenPDF_Full, 0, wx.TOP | wx.LEFT, 10)

		CB_GenPDF_Booklet = wx.CheckBox(self, -1, "Gen. Booklet PDF")
		CB_GenPDF_Booklet.SetFont(StandardFont)
		StaticBoxSizer.Add(CB_GenPDF_Booklet, 0, wx.TOP | wx.LEFT, 10)

		BTN_Go = wx.Button(self, -1, "Go!")
		BTN_Go.SetFont(StandardFont)
		StaticBoxSizer.Add(BTN_Go, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 10)

		gbs.Add(StaticBoxSizer,
				pos = (7,0), span = (5,1), flag = wx.ALIGN_CENTER_HORIZONTAL)

		self.gbs.AddGrowableCol(1)
		border = wx.BoxSizer()
		border.Add(gbs, 1, wx.EXPAND | wx.ALL, 25)
		self.SetSizer(border)
		border.SetDimension(0,0,self.GetSize()[0], self.GetSize()[1])
		print border.GetSize()
		print self.gbs.GetSize()
		self.Title = "Main"


class ConfigPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, None)

		#sizer = wx.BoxSizer(wx.VERTICAL)

		#self.csvFile = filebrowse.FileBrowseButton(
		#	self, -1, size=(450, 30),
		#	labelText = "Membership File",
		#	fileMask = "*.csv"#, changeCallback = self.fbbCallback
		#	)
		#sizer.Add(self.csvFile)

		#self.ImagesFolder = filebrowse.DirBrowseButton(
		#	self, -1, size=(450, 100),
		#	labelText = "Images Folder",
		#	)
		#sizer.Add(self.ImagesFolder)

		#self.SetSizerAndFit(sizer)
		#parent.SetClientSize(self.GetSize())

		self.Title = "Configuration"

class BuildingPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, wx.BLUE)
		
		#st = wx.StaticText(self, -1,
		#		  "Facilities Info here",
		#		  (10, 10))
		#st.SetForegroundColour(wx.WHITE)
		#st.SetBackgroundColour(wx.GREEN)
		self.Title = "Building"

class LeadershipPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, None)
		
		#st = wx.StaticText(self, -1,
		#		  "Retrieve Leadership Info Here",
		#		  (10, 10))
		#st.SetForegroundColour(wx.WHITE)
		#st.SetBackgroundColour(wx.GREEN)
		self.Title = "Leadership"

class HelpPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, wx.BLUE)
		
		#st = wx.StaticText(self, -1,
		#		  "Help will go here",
		#		  (10, 10))
		#st.SetForegroundColour(wx.WHITE)
		#st.SetBackgroundColour(wx.GREEN)
		self.Title = "Help"
