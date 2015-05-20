# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time

import wx

import Notebook
import __version__
from Engine import Application

DEBUG = 0


class MyFrame(wx.Frame):
    def __init__(self):
        super(MyFrame, self).__init__(
            None, -1, "Ward Directory Creator",
            style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | \
                  wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)

        self.AppHandle = Application.Application(self, DEBUG)

        self.SetTitle("Ward Directory Creator v." + __version__.__version__)
        self.StatusBar = wx.StatusBar(self, -1)
        self.StatusBar.SetStatusText("Version " + __version__.__version__)
        self.myNotebook = Notebook.Notebook(self, -1, self.AppHandle)

        self.Fit()

    def OnCloseWindow(self, event):
        self.Destroy()

    def OnDoPrint(self, event):
        self.AppHandle.InitiatePDF()
