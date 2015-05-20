# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx

from PanelMain import MainPanel
from PanelConfig import ConfigPanel
from PanelBuilding import BuildingPanel
from PanelLeadership import LeadershipPanel
from PanelGenerate import GeneratePanel


class Notebook(wx.Notebook):
    def __init__(self, parent, AppHandle):
        super(Notebook, self).__init__(parent, -1, size=wx.DefaultSize)
        self.parent = parent
        self.AppHandle = AppHandle
        self.TextBoxFont = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False,
                                   "Georgia")
        self.SetFont(self.TextBoxFont)

        self.myMainPanel = MainPanel(self)
        self.AddPage(self.myMainPanel, self.myMainPanel.Title)

        self.myBuildingPanel = BuildingPanel(self)
        self.AddPage(self.myBuildingPanel, self.myBuildingPanel.Title)

        self.myConfigPanel = ConfigPanel(self)
        self.AddPage(self.myConfigPanel, self.myConfigPanel.Title)

        self.myLeadershipPanel = LeadershipPanel(self)
        self.AddPage(self.myLeadershipPanel, self.myLeadershipPanel.Title)

        self.myGeneratePanel = GeneratePanel(self)
        self.AddPage(self.myGeneratePanel, self.myGeneratePanel.Title)

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
