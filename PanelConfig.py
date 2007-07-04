#PanelConfig.py
import wx
from ColoredPanel import *
import  wx.lib.filebrowsebutton as filebrowse

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
