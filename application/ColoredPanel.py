# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx

import images


class ColoredPanel(wx.Window):
    def __init__(self, parent, color):
        self.parent = parent
        self.id = wx.NewId()
        wx.Window.__init__(self, parent, self.id, style = wx.SIMPLE_BORDER)

        # Just for style points, we'll use this as a background image.
        self.bg_bmp = images.getNotebookBKGDBitmap()
        self.logo_bmp = images.getWDCBitmap()
        self.SetSize((self.bg_bmp.GetWidth(), self.bg_bmp.GetHeight()))

        self.TitleFont = wx.Font(22, wx.DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, False, "Georgia")
        self.StandardFont = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Georgia")
        self.TextBoxFont = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Georgia")
