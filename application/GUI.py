# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time

import wx

from Engine.Application import Application
from PanelMain import MainPanel
from PanelConfig import ConfigPanel
from PanelBuilding import BuildingPanel
from PanelLeadership import LeadershipPanel
from GeneratePanel.GenerateControl import GenerateControl
from GeneratePanel.GenerateInteraction import GenerateInteraction
from GeneratePanel.GeneratePresentation import GeneratePresentation
from __version__ import __version__

DEBUG = 0


class MyFrame(wx.Frame):
    def __init__(self):
        super(MyFrame, self).__init__(
            None, -1, "Ward Directory Creator",
            style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | \
                  wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)

        self.app_handle = Application(self, DEBUG)
        self.StatusBar = wx.StatusBar(self, -1)
        self.StatusBar.SetStatusText("Version: %s" % __version__)
        self.TextBoxFont = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False,
                                   "Georgia")
        self.SetFont(self.TextBoxFont)
        self.nb = wx.Notebook(self, -1)

        main = MainPanel(self.nb, self.app_handle)
        self.nb.AddPage(main, main.Title)

        panels = [BuildingPanel, ConfigPanel, LeadershipPanel]
        for panel in panels:
            p = panel(self.nb, self.app_handle)
            self.nb.AddPage(p, p.Title)

        p = GeneratePresentation(self.nb)
        i = GenerateInteraction()
        self.generate_control = GenerateControl(self.app_handle, p, i)
        self.nb.AddPage(p, "Generate")

        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_page_changed)
        self.nb.SetPageSize(main.GetSize())
        self.Fit()

    def on_page_changed(self, event):
        new = event.GetSelection()
        if isinstance(self.nb.GetPage(new), GeneratePresentation):
            self.generate_control.making_active()
        else:
            self.nb.GetPage(new).making_active()
        event.Skip()
