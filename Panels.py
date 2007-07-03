import wx
from ColoredPanel import *
import  wx.lib.filebrowsebutton as filebrowse

class MainPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, wx.BLUE)
		
		st = wx.StaticText(self, -1,
				  "Title/Stuff goes here",
				  (10, 10))
		st.SetForegroundColour(wx.WHITE)
		st.SetBackgroundColour(wx.GREEN)
		self.Title = "Main"

class ConfigPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, None)

		sizer = wx.BoxSizer(wx.VERTICAL)

		self.csvFile = filebrowse.FileBrowseButton(
			self, -1, size=(450, 30),
			labelText = "Membership File",
			fileMask = "*.csv"#, changeCallback = self.fbbCallback
			)
		sizer.Add(self.csvFile)

		self.ImagesFolder = filebrowse.DirBrowseButton(
			self, -1, size=(450, 100),
			labelText = "Images Folder",
			)
		sizer.Add(self.ImagesFolder)

		self.SetSizerAndFit(sizer)
		#parent.SetClientSize(self.GetSize())

		self.Title = "Configuration"

class BuildingPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, wx.BLUE)
		
		st = wx.StaticText(self, -1,
				  "Facilities Info here",
				  (10, 10))
		st.SetForegroundColour(wx.WHITE)
		st.SetBackgroundColour(wx.GREEN)
		self.Title = "Building"

class LeadershipPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, None)
		
		st = wx.StaticText(self, -1,
				  "Retrieve Leadership Info Here",
				  (10, 10))
		st.SetForegroundColour(wx.WHITE)
		st.SetBackgroundColour(wx.GREEN)
		self.Title = "Leadership"

class HelpPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, wx.BLUE)
		
		st = wx.StaticText(self, -1,
				  "Help will go here",
				  (10, 10))
		st.SetForegroundColour(wx.WHITE)
		st.SetBackgroundColour(wx.GREEN)
		self.Title = "Help"
