#PanelBuilding.py

import wx
from ColoredPanel import *
import  wx.lib.filebrowsebutton as filebrowse

class BuildingPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, wx.BLUE)
		
		#st = wx.StaticText(self, -1,
		#		  "Facilities Info here",
		#		  (10, 10))
		#st.SetForegroundColour(wx.WHITE)
		#st.SetBackgroundColour(wx.GREEN)
		self.Title = "Building"
