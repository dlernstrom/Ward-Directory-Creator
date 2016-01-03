# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx


class MainInteraction(object):
    def install(self, control, p):
        self.control = control
        p.Bind(wx.EVT_BUTTON, self.cb_about_btn, p.AboutBoxButton)
        p.Bind(wx.EVT_TEXT, self.cb_ward_changed, p.TXT_WardName)
        p.Bind(wx.EVT_RADIOBUTTON, self.cb_ward_type_changed)
        p.Bind(wx.EVT_TEXT, self.cb_stake_changed, p.TXT_StakeName)
        p.Bind(wx.EVT_CHECKBOX, self.cb_use_quote, p.CB_UseQuote)
        p.Bind(wx.EVT_TEXT, self.cb_quote_changed, p.TXT_Quote)
        p.Bind(wx.EVT_TEXT, self.cb_author_changed, p.TXT_Author)
        p.Bind(wx.EVT_BUTTON, self.cb_restore_quote, p.BTN_RestoreQuote)

    def cb_about_btn(self, evt):
        self.control.display_about_dialog()

    def cb_ward_changed(self, evt):
        self.control.update_ward_name(evt.GetString())

    def cb_ward_type_changed(self, evt):
        if evt.GetEventObject().GetLabel() == 'Ward':
            self.control.update_unit_type('Ward')
        else:
            self.control.update_unit_type('Branch')

    def cb_stake_changed(self, evt):
        self.control.update_stake_name(evt.GetString())

    def cb_use_quote(self, evt):
        if evt.Checked():
            self.control.allow_use_quote(True)
        else:
            self.control.allow_use_quote(False)

    def cb_quote_changed(self, evt):
        self.control.update_quote(evt.GetString())

    def cb_author_changed(self, evt):
        self.control.update_author(evt.GetString())

    def cb_restore_quote(self, evt):
        self.control.reset_quote()
