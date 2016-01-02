# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx

from .BuildingPanel.BuildingAbstraction import BuildingAbstraction
from .BuildingPanel.BuildingControl import BuildingControl
from .BuildingPanel.BuildingInteraction import BuildingInteraction
from .BuildingPanel.BuildingPresentation import BuildingPresentation
from .ConfigPanel.ConfigAbstraction import ConfigAbstraction
from .ConfigPanel.ConfigControl import ConfigControl
from .ConfigPanel.ConfigInteraction import ConfigInteraction
from .ConfigPanel.ConfigPresentation import ConfigPresentation
from .MainPanel.MainControl import MainControl
from .MainPanel.MainInteraction import MainInteraction
from .MainPanel.MainPresentation import MainPresentation
from .PanelLeadership import LeadershipPanel
from .GeneratePanel.GenerateControl import GenerateControl
from .GeneratePanel.GenerateInteraction import GenerateInteraction
from .GeneratePanel.GeneratePresentation import GeneratePresentation
from Engine.Application import Application
from __version__ import __version__

DEBUG = 0


class MyFrame(wx.Frame):
    def __init__(self):
        super(MyFrame, self).__init__(
            None, -1, "Ward Directory Creator",
            style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | \
                  wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)

        self.app_handle = Application(self, DEBUG)
        status_bar = wx.StatusBar(self, -1)
        status_bar.SetStatusText("Version: %s" % __version__)
        self.TextBoxFont = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False,
                                   "Georgia")
        self.SetFont(self.TextBoxFont)
        self.nb = wx.Notebook(self, -1)

        main_presentation = MainPresentation(self.nb)
        main_interaction = MainInteraction()
        self.main_control = MainControl(self.app_handle, main_presentation,
                                        main_interaction)
        self.nb.AddPage(main_presentation, 'Main')

        bldg_abstraction = BuildingAbstraction(self.app_handle)
        bldg_presentation = BuildingPresentation(self.nb)
        bldg_interaction = BuildingInteraction()
        self.building_control = BuildingControl(bldg_abstraction,
                                                bldg_presentation,
                                                bldg_interaction)
        self.nb.AddPage(bldg_presentation, "Building")

        config_abstraction = ConfigAbstraction(self.app_handle)
        config_presentation = ConfigPresentation(self.nb)
        config_interaction = ConfigInteraction()
        self.config_control = ConfigControl(config_abstraction,
                                            config_presentation,
                                            config_interaction)
        self.nb.AddPage(config_presentation, "Configuration")

        leadership_panel = LeadershipPanel(self.nb, self.app_handle)
        self.nb.AddPage(leadership_panel, leadership_panel.Title)

        generate_panel = GeneratePresentation(self.nb)
        generate_interaction = GenerateInteraction()
        self.generate_control = GenerateControl(self.app_handle,
                                                generate_panel,
                                                generate_interaction)
        self.nb.AddPage(generate_panel, "Generate")

        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_page_changed)
        self.nb.SetPageSize(main_presentation.GetSize())
        self.Fit()
        self.main_control.making_active()

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
