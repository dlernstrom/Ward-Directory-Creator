import wx
from PanelMain import *
from PanelConfig import *
from PanelBuilding import *
from PanelLeadership import *
from PanelGenerate import *
from PanelHelp import *

class Notebook(wx.Notebook):
	def __init__(self, parent, id, AppHandle):
		wx.Notebook.__init__(self, parent, id, size=wx.DefaultSize
							 )
		self.parent = parent
		self.AppHandle = AppHandle
		self.TextBoxFont = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Georgia")
		self.SetFont(self.TextBoxFont)

		self.myMainPanel = MainPanel(self)
		self.AddPage(self.myMainPanel, self.myMainPanel.Title)

		self.myConfigPanel = ConfigPanel(self)
		self.AddPage(self.myConfigPanel, self.myConfigPanel.Title)

		self.myBuildingPanel = BuildingPanel(self)
		self.AddPage(self.myBuildingPanel, self.myBuildingPanel.Title)

		self.myLeadershipPanel = LeadershipPanel(self)
		self.AddPage(self.myLeadershipPanel, self.myLeadershipPanel.Title)

		self.myGeneratePanel = GeneratePanel(self)
		self.AddPage(self.myGeneratePanel, self.myGeneratePanel.Title)

		self.myHelpPanel = HelpPanel(self)
		self.AddPage(self.myHelpPanel, self.myHelpPanel.Title)

		self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
		self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
		self.SetPageSize(self.myMainPanel.GetSize())

	def GetConfigValue(self, DictionaryField):
		return self.AppHandle.GetConfigValue(DictionaryField)

	def SetConfigValue(self, DictionaryField, value):
		self.AppHandle.SetConfigValue(DictionaryField, value)

	def isValidCSV(self):
		return self.AppHandle.isValidCSV()

	def OnPageChanged(self, event):
		old = event.GetOldSelection()
		new = event.GetSelection()
		sel = self.GetSelection()
		self.GetPage(new).makingActive()
		event.Skip()

	def OnPageChanging(self, event):
		old = event.GetOldSelection()
		new = event.GetSelection()
		sel = self.GetSelection()
		event.Skip()
