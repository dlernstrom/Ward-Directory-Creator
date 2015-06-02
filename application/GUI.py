# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time

import wx

from BuildingPanel.BuildingAbstraction import BuildingAbstraction
from BuildingPanel.BuildingControl import BuildingControl
from BuildingPanel.BuildingInteraction import BuildingInteraction
from BuildingPanel.BuildingPresentation import BuildingPresentation
from ConfigPanel.ConfigControl import ConfigControl
from ConfigPanel.ConfigInteraction import ConfigInteraction
from ConfigPanel.ConfigPresentation import ConfigPresentation
from Engine.Application import Application
from MainPanel.MainControl import MainControl
from MainPanel.MainInteraction import MainInteraction
from MainPanel.MainPresentation import MainPresentation
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

        p = MainPresentation(self.nb)
        i = MainInteraction()
        self.main_control = MainControl(self.app_handle, p, i)
        self.nb.AddPage(p, 'Main')

        a = BuildingAbstraction(self.app_handle)
        p = BuildingPresentation(self.nb)
        i = BuildingInteraction()
        self.building_control = BuildingControl(a, p, i)
        self.nb.AddPage(p, "Building")

        p = ConfigPresentation(self.nb)
        i = ConfigInteraction()
        self.config_control = ConfigControl(self.app_handle, p, i)
        self.nb.AddPage(p, "Configuration")

        p = LeadershipPanel(self.nb, self.app_handle)
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
        page = self.nb.GetPage(new)
        if isinstance(page, BuildingPresentation):
            self.building_control.making_active()
        elif isinstance(page, ConfigPresentation):
            self.config_control.making_active()
        elif isinstance(page, GeneratePresentation):
            self.generate_control.making_active()
        elif isinstance(page, MainPresentation):
            self.main_control.making_active()
        else:
            page.making_active()
        event.Skip()
