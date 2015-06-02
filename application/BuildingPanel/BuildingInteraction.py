# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx
from wx.lib.masked import EVT_TIMEUPDATE


class BuildingInteraction(object):
    def install(self, control, p):
        self.control = control
        p.Bind(wx.EVT_CHECKBOX, self.on_sac_time_disp_cb, p.CB_SacramentDisp)
        p.Bind(wx.EVT_CHECKBOX, self.on_ss_time_disp_cb, p.CB_SundaySchoolDisp)
        p.Bind(wx.EVT_CHECKBOX, self.on_pr_time_disp_cb, p.CB_PriesthoodDisp)
        p.Bind(EVT_TIMEUPDATE, self.on_sac_time_change, p.SacTime)
        p.Bind(EVT_TIMEUPDATE, self.on_ss_time_change, p.SSTime)
        p.Bind(EVT_TIMEUPDATE, self.on_pr_time_change, p.PriesthoodTime)
        p.Bind(wx.EVT_TEXT, self.on_bldg_addy1_changed, p.Addy1)
        p.Bind(wx.EVT_TEXT, self.on_bldg_addy2_changed, p.Addy2)
        p.Bind(wx.EVT_TEXT, self.on_bldg_phone_changed, p.Phone)

    def on_sac_time_disp_cb(self, evt):
        if evt.Checked():
            self.control.show_sac_start_time()
        else:
            self.control.show_sac_start_time(False)

    def on_ss_time_disp_cb(self, evt):
        if evt.Checked():
            self.control.show_ss_start_time()
        else:
            self.control.show_ss_start_time(False)

    def on_pr_time_disp_cb(self, evt):
        if evt.Checked():
            self.control.show_pr_start_time()
        else:
            self.control.show_pr_start_time(False)

    def on_sac_time_change(self, evt):
        self.control.update_sac_time(evt.GetValue())

    def on_ss_time_change(self, evt):
        self.control.update_ss_time(evt.GetValue())

    def on_pr_time_change(self, evt):
        self.control.update_pr_time(evt.GetValue())

    def on_bldg_addy1_changed(self, evt):
        self.control.update_building_address_line_1(evt.GetString())

    def on_bldg_addy2_changed(self, evt):
        self.control.update_building_address_line_2(evt.GetString())

    def on_bldg_phone_changed(self, evt):
        self.control.update_building_phone(evt.GetString())
