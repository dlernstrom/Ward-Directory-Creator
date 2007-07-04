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

		StaticHeading = wx.StaticText(self,
									  -1,
									  "Ward Directory Creator " + parent.parent.MajorAppVersion,
									  style = wx.ALIGN_CENTRE)
		StaticHeading.SetFont(self.TitleFont)

		logo = wx.StaticBitmap(self, -1, self.logo_bmp, (self.logo_bmp.GetWidth(), self.logo_bmp.GetHeight()))

		left_level3 = wx.BoxSizer(wx.VERTICAL)
		left_level3.Add(self.WardBoxSizer, 6, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, 25)
		left_level3.Add(logo, 3, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, 25)

		right_level3 = wx.BoxSizer()
		right_level3.Add(self.QuoteBoxSizer, 5, wx.EXPAND | wx.ALL, 25)

		top_level2 = wx.BoxSizer(wx.HORIZONTAL)
		top_level2.Add(StaticHeading, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)

		bottom_level2 = wx.BoxSizer(wx.HORIZONTAL)
		bottom_level2.Add(left_level3, 2, wx.EXPAND)
		bottom_level2.Add(right_level3, 3, wx.EXPAND)

		inside_border_level1 = wx.BoxSizer(wx.VERTICAL)
		inside_border_level1.Add(top_level2, 0, wx.EXPAND | wx.ALL, 25)
		inside_border_level1.Add(bottom_level2, 1, wx.EXPAND)

		border_level0 = wx.BoxSizer()
		border_level0.Add(inside_border_level1, 1, wx.EXPAND | wx.ALL, 25)
		self.SetSizer(border_level0)
		border_level0.SetDimension(0, 0, self.GetSize()[0], self.GetSize()[1])
		print "Level 0 - position:",border_level0.GetPosition()
		print "Level 0 - size:",border_level0.GetSize()

		print "Level 1 - Inner Border position:", inside_border_level1.GetPosition()
		print "Level 1 - Inner Border size:", inside_border_level1.GetSize()

		print "Level 2 - Top Title position:", top_level2.GetPosition()
		print "Level 2 - Top Title size:", top_level2.GetSize()

		print "Level 2 - Bottom Content position:", bottom_level2.GetPosition()
		print "Level 2 - Bottom Content size:", bottom_level2.GetSize()

		print "Level 3 - Static Title position:", StaticHeading.GetPosition()
		print "Level 3 - Static Title size:", StaticHeading.GetSize()

		print "Level 3 - Left Content position:", left_level3.GetPosition()
		print "Level 3 - Left Content size:", left_level3.GetSize()

		print "Level 3 - Right Content position:", right_level3.GetPosition()
		print "Level 3 - Right Content size:", right_level3.GetSize()

		print "Level 4 - Ward/Branch position:", self.WardBoxSizer.GetPosition()
		print "Level 4 - Ward/Branch size:", self.WardBoxSizer.GetSize()

		print "Level 4 - LOGO position:", logo.GetPosition()
		print "Level 4 - LOGO size:", logo.GetSize()

		print "Level 4 - Quote position:", self.QuoteBoxSizer.GetPosition()
		print "Level 4 - Quote size:", self.QuoteBoxSizer.GetSize()

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
