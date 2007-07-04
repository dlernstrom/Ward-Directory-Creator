#PanelLeadership.py

import wx
from ColoredPanel import *
import  wx.lib.filebrowsebutton as filebrowse

class LeadershipPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, None)
		
		#st = wx.StaticText(self, -1,
		#		  "Retrieve Leadership Info Here",
		#		  (10, 10))
		#st.SetForegroundColour(wx.WHITE)
		#st.SetBackgroundColour(wx.GREEN)
		self.Title = "Leadership"
