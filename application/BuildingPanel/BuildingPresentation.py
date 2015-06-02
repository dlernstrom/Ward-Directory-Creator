# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx
from wx.lib.masked import TimeCtrl

from application.ColoredPanel import ColoredPanel


class BuildingPresentation(ColoredPanel):
    def __init__(self, parent):
        super(BuildingPresentation, self).__init__(parent, wx.BLUE)
        #######################################################################
        ## Block Schedule Configuration
        box = wx.StaticBox(self, -1, "Block Schedule")
        box.SetFont(self.StandardFont)
        schedule_box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        gbs = wx.GridBagSizer()

        title = wx.StaticText(self, -1, "Display")
        title.SetFont(self.StandardFont)
        gbs.Add(title, (0, 0), span=wx.DefaultSpan,
                flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=10)

        # Sacrament Meeting Row
        self.CB_SacramentDisp = wx.CheckBox(self, -1)
        gbs.Add(self.CB_SacramentDisp, (1, 0), span=wx.DefaultSpan,
                flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        self.SacText = wx.StaticText(self, -1,
                                     "Sacrament Meeting (Start Time)")
        self.SacText.SetFont(self.StandardFont)
        gbs.Add(self.SacText, (1, 1), span=wx.DefaultSpan,
                         flag=wx.ALL, border=10)

        self.SacTime = TimeCtrl(self, -1, display_seconds=False)
        self.SacTime.SetFont(self.StandardFont)
        h = self.SacTime.GetSize().height
        self.spin1 = wx.SpinButton(self, -1, wx.DefaultPosition, (-1, h),
                                   wx.SP_VERTICAL)
        self.SacTime.BindSpinButton(self.spin1)
        gbs.Add(self.SacTime, (1, 2), span=wx.DefaultSpan,
                flag=wx.ALIGN_RIGHT | wx.TOP | wx.LEFT | wx.BOTTOM,
                border=10)
        gbs.Add(self.spin1, (1, 3), span=wx.DefaultSpan,
                flag=wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.BOTTOM,
                border=10)

        # Sunday School Row
        self.CB_SundaySchoolDisp = wx.CheckBox(self, -1)
        gbs.Add(self.CB_SundaySchoolDisp, (2, 0),
                span=wx.DefaultSpan, flag=wx.ALIGN_CENTER | wx.ALL,
                border=10)

        self.SSText = wx.StaticText(self, -1, "SundaySchool (Start Time)")
        self.SSText.SetFont(self.StandardFont)
        gbs.Add(self.SSText, (2, 1), span=wx.DefaultSpan, flag=wx.ALL,
                border=10)

        self.SSTime = TimeCtrl(self, -1, display_seconds=False)
        self.SSTime.SetFont(self.StandardFont)
        h = self.SSTime.GetSize().height
        self.spin2 = wx.SpinButton(self, -1, wx.DefaultPosition, (-1, h),
                                   wx.SP_VERTICAL)
        self.SSTime.BindSpinButton(self.spin2)
        gbs.Add(self.SSTime, (2, 2), span=wx.DefaultSpan,
                flag=wx.ALIGN_RIGHT | wx.TOP | wx.LEFT | wx.BOTTOM,
                border=10)
        gbs.Add(self.spin2, (2, 3), span=wx.DefaultSpan,
                flag=wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.BOTTOM,
                border=10)

        # Priesthood/Relief Society Row
        self.CB_PriesthoodDisp = wx.CheckBox(self, -1)
        gbs.Add(self.CB_PriesthoodDisp, (3, 0), span=wx.DefaultSpan,
                flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        title = "Priesthood/Relief Society (Start Time)"
        self.PriesthoodText = wx.StaticText(self, -1, title)
        self.PriesthoodText.SetFont(self.StandardFont)
        gbs.Add(self.PriesthoodText, (3, 1), span=wx.DefaultSpan,
                         flag=wx.ALL, border=10)

        self.PriesthoodTime = TimeCtrl(self, -1, display_seconds=False)
        self.PriesthoodTime.SetFont(self.StandardFont)
        h = self.PriesthoodTime.GetSize().height
        self.spin3 = wx.SpinButton(self, -1, wx.DefaultPosition, (-1, h),
                                   wx.SP_VERTICAL)
        self.PriesthoodTime.BindSpinButton(self.spin3)
        gbs.Add(self.PriesthoodTime, (3, 2), span=wx.DefaultSpan,
                flag=wx.ALIGN_RIGHT | wx.TOP | wx.LEFT | wx.BOTTOM,
                border=10)
        gbs.Add(self.spin3, (3, 3), span=wx.DefaultSpan,
                flag=wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.BOTTOM,
                border=10)

        schedule_box_sizer.Add(gbs, 0, wx.ALL | 10)

        #######################################################################
        ## Building Contact Information
        box = wx.StaticBox(self, -1, "Building Information")
        box.SetFont(self.StandardFont)
        building_box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        title = wx.StaticText(self, -1, "Building Address")
        title.SetFont(self.StandardFont)
        building_box_sizer.Add(title, 1, wx.ALL, 10)

        self.Addy1 = wx.TextCtrl(self, -1, size=(300, -1))
        self.Addy1.SetFont(self.StandardFont)
        building_box_sizer.Add(self.Addy1, 0, wx.ALL, 10)

        self.Addy2 = wx.TextCtrl(self, -1, size=(300, -1))
        self.Addy2.SetFont(self.StandardFont)
        building_box_sizer.Add(self.Addy2, 0, wx.ALL, 10)

        title = wx.StaticText(self, -1, "Building Phone #")
        title.SetFont(self.StandardFont)
        building_box_sizer.Add(title, 0, wx.ALL, 10)

        self.Phone = wx.TextCtrl(self, -1, size=(200, -1))
        self.Phone.SetFont(self.StandardFont)
        building_box_sizer.Add(self.Phone, 0, wx.ALL, 10)

        #######################################################################
        ## Non wrapped items
        logo = wx.StaticBitmap(self, -1, self.logo_bmp,
                               (self.logo_bmp.GetWidth(),
                                self.logo_bmp.GetHeight()))

        #######################################################################
        ## Sizer encapsulation section
        top_level2 = wx.BoxSizer(wx.HORIZONTAL)
        top_level2.AddStretchSpacer()
        top_level2.Add(schedule_box_sizer, 0)
        top_level2.AddStretchSpacer()

        bottom_level2 = wx.BoxSizer(wx.HORIZONTAL)
        bottom_level2.Add(logo, 0, wx.ALL, 10)
        bottom_level2.Add(building_box_sizer, 3, wx.EXPAND | wx.ALL, 25)

        inside_border_level1 = wx.BoxSizer(wx.VERTICAL)
        inside_border_level1.Add(top_level2, 0, wx.BOTTOM | wx.ALIGN_CENTER, 5)
        inside_border_level1.Add(bottom_level2, 0, wx.TOP | wx.ALIGN_CENTER, 5)

        border_level0 = wx.BoxSizer()
        border_level0.Add(inside_border_level1, 1, wx.EXPAND | wx.ALL, 25)
        self.SetSizer(border_level0)
        border_level0.SetDimension(0, 0, self.GetSize()[0], self.GetSize()[1])
