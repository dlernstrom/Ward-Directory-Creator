import wx
from ColoredPanel import *
import  wx.lib.filebrowsebutton as filebrowse

class MainPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, wx.BLUE)
		
		#st = wx.StaticText(self, -1,
		#		  "Title/Stuff goes here",
		#		  (10, 10))
		#st.SetForegroundColour(wx.WHITE)
		#st.SetBackgroundColour(wx.GREEN)

		self.gbs = gbs = wx.GridBagSizer(vgap = 5, hgap = 10)

		TitleFont = wx.Font(22, wx.DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, False, "Georgia")
		StandardFont = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Georgia")
		

		StaticHeading = wx.StaticText(self, -1,"Ward Directory Creator " + parent.parent.MajorAppVersion)
		StaticHeading.SetFont(TitleFont)
		gbs.Add(StaticHeading,
				pos = (0,0), span = (1,4), flag = wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_TOP)

		StaticWardName = wx.StaticText(self, -1, "Ward Name:")
		StaticWardName.SetFont(StandardFont)
		gbs.Add(StaticWardName,
				pos = (2,0), span = (1,1), flag = wx.ALIGN_LEFT)

		TXT_WardName = wx.TextCtrl(self, -1, size=(250,35))
		TXT_WardName.SetFont(StandardFont)
		gbs.Add(TXT_WardName,
				pos = (2,1), span = (1,2), flag = wx.ALIGN_LEFT)

		RB_Ward = wx.RadioButton(self, -1, "Ward", style = wx.RB_GROUP)
		RB_Ward.SetFont(StandardFont)
		gbs.Add(RB_Ward,
				pos = (3,0), span = wx.DefaultSpan, flag = wx.ALIGN_CENTER_HORIZONTAL)

		RB_Branch = wx.RadioButton(self, -1, "Branch")
		RB_Branch.SetFont(StandardFont)
		gbs.Add(RB_Branch,
				pos = (3,1), span = wx.DefaultSpan, flag = wx.ALIGN_LEFT)

		StaticStakeName = wx.StaticText(self, -1, "Stake Name:")
		StaticStakeName.SetFont(StandardFont)
		gbs.Add(StaticStakeName,
				pos = (4,0), span = (1,1), flag = wx.ALIGN_LEFT)

		TXT_StakeName = wx.TextCtrl(self, -1, size=(250,35))
		TXT_StakeName.SetFont(StandardFont)
		gbs.Add(TXT_StakeName,
				pos = (4,1), span = (1,2), flag = wx.ALIGN_LEFT)

		CB_UseQuote = wx.CheckBox(self, -1, "Use Quote")
		CB_UseQuote.SetFont(StandardFont)
		gbs.Add(CB_UseQuote,
				pos = (6,0), span = (1,2), flag = wx.ALIGN_LEFT)

		StaticInspQuote = wx.StaticText(self, -1, "Inspirational Quote:")
		StaticInspQuote.SetFont(StandardFont)
		StaticInspQuote.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		gbs.Add(StaticInspQuote,
				pos = (7,0), span = (1,2), flag = wx.ALIGN_LEFT)

		TXT_Quote = wx.TextCtrl(self, -1, size = (350, 105))
		TXT_Quote.SetFont(StandardFont)
		gbs.Add(TXT_Quote,
				pos = (8,0), span = (1,4), flag = wx.ALIGN_LEFT)

		StaticAuthor = wx.StaticText(self, -1, "Author:")
		StaticAuthor.SetFont(StandardFont)
		gbs.Add(StaticAuthor,
				pos = (9,0), span = (1,1), flag = wx.ALIGN_LEFT)

		TXT_Author = wx.TextCtrl(self, -1, size=(250,35))
		TXT_Author.SetFont(StandardFont)
		gbs.Add(TXT_Author,
				pos = (9,1), span = (1,2), flag = wx.ALIGN_LEFT)

		BTN_RestoreQuote = wx.Button(self, -1, "Restore Default")
		BTN_RestoreQuote.SetFont(StandardFont)
		gbs.Add(BTN_RestoreQuote,
				pos = (10,0), span = (1,2), flag = wx.ALIGN_LEFT)

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
				pos = (2,4), span = (5,1), flag = wx.ALIGN_CENTER_HORIZONTAL)
		#gbs.Add((10,0), (14,7))
		#self.gbs.AddGrowableRow(100)
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
