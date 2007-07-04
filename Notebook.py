import wx
from Panels import *

class Notebook(wx.Notebook):
	def __init__(self, parent, id, AppHandle):
		wx.Notebook.__init__(self, parent, id, size=wx.DefaultSize
							 #style=
							 #wx.NB_TOP # | wx.NB_MULTILINE
							 #wx.NB_BOTTOM
							 #wx.NB_LEFT
							 #wx.NB_RIGHT
							 )
		self.parent = parent
		self.AppHandle = AppHandle

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
		#self.Fit()
		self.SetPageSize(self.myMainPanel.GetSize())


	def OnPageChanged(self, event):
		old = event.GetOldSelection()
		new = event.GetSelection()
		sel = self.GetSelection()
		event.Skip()

	def OnPageChanging(self, event):
		old = event.GetOldSelection()
		new = event.GetSelection()
		sel = self.GetSelection()
		event.Skip()
