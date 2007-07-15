#PanelGenerate.py

import wx
from ColoredPanel import *
import  wx.lib.filebrowsebutton as filebrowse

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

	def makingActive(self):
		return

