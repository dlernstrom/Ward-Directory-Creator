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


		StaticHeading = wx.StaticText(self, -1,"Ward Directory Creator " + parent.parent.MajorAppVersion)
		StaticHeading.SetFont(self.TitleFont)
		gbs.Add(StaticHeading,
				pos = (0,0), span = (1,3), flag = wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_TOP)


		gbs.Add(self.WardBoxSizer,
				pos = (1,0), span = (6,1), flag = wx.ALIGN_LEFT)

		gbs.Add(self.QuoteBoxSizer,
				pos = (1,1), span = (8,2), flag = wx.ALIGN_CENTER_HORIZONTAL)


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

class GeneratePanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, None)
		StaticBox = wx.StaticBox(self, -1, "Generate Directory")

		StaticBox.SetFont(self.StandardFont)
		StaticBoxSizer = wx.StaticBoxSizer(StaticBox, wx.VERTICAL)

		CB_SendEmail = wx.CheckBox(self, -1, "Send Missing Email")
		CB_SendEmail.SetFont(self.StandardFont)
		StaticBoxSizer.Add(CB_SendEmail, 0, wx.TOP | wx.LEFT, 10)

		CB_MissingReport = wx.CheckBox(self, -1, "Generate Missing Report")
		CB_MissingReport.SetFont(self.StandardFont)
		StaticBoxSizer.Add(CB_MissingReport, 0, wx.TOP | wx.LEFT, 10)

		CB_ExtractMoveOuts = wx.CheckBox(self, -1, "Extract Move Out Images")
		CB_ExtractMoveOuts.SetFont(self.StandardFont)
		StaticBoxSizer.Add(CB_ExtractMoveOuts, 0, wx.TOP | wx.LEFT, 10)

		CB_GenPDF_Full = wx.CheckBox(self, -1, "Gen. Full Spread PDF")
		CB_GenPDF_Full.SetFont(self.StandardFont)
		StaticBoxSizer.Add(CB_GenPDF_Full, 0, wx.TOP | wx.LEFT, 10)

		CB_GenPDF_Booklet = wx.CheckBox(self, -1, "Gen. Booklet PDF")
		CB_GenPDF_Booklet.SetFont(self.StandardFont)
		StaticBoxSizer.Add(CB_GenPDF_Booklet, 0, wx.TOP | wx.LEFT, 10)

		BTN_Go = wx.Button(self, -1, "Go!")
		BTN_Go.SetFont(self.StandardFont)
		StaticBoxSizer.Add(BTN_Go, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 10)

		#gbs.Add(StaticBoxSizer,
		#		pos = (7,0), span = (5,1), flag = wx.ALIGN_CENTER_HORIZONTAL)
		self.Title = "Generate"


class HelpPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, wx.BLUE)
		
		#st = wx.StaticText(self, -1,
		#		  "Help will go here",
		#		  (10, 10))
		#st.SetForegroundColour(wx.WHITE)
		#st.SetBackgroundColour(wx.GREEN)
		self.Title = "Help"
