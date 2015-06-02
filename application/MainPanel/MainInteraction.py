# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx


class MainInteraction(object):
    def install(self, control, p):
        self.control = control
        p.Bind(wx.EVT_BUTTON, self.OnAboutButton, p.AboutBoxButton)
        p.Bind(wx.EVT_TEXT, self.OnWardChanged, p.TXT_WardName)
        p.Bind(wx.EVT_RADIOBUTTON, self.OnWardTypeChanged)
        p.Bind(wx.EVT_TEXT, self.OnStakeChanged, p.TXT_StakeName)
        p.Bind(wx.EVT_CHECKBOX, self.OnUseQuote, p.CB_UseQuote)
        p.Bind(wx.EVT_TEXT, self.OnQuoteChanged, p.TXT_Quote)
        p.Bind(wx.EVT_TEXT, self.OnAuthorChanged, p.TXT_Author)
        p.Bind(wx.EVT_BUTTON, self.OnRestoreQuote, p.BTN_RestoreQuote)

    def OnAboutButton(self, evt):
        self.control.display_about_dialog()

    def OnWardChanged(self, evt):
        self.control.update_ward_name(evt.GetString())

    def OnWardTypeChanged(self, evt):
        if evt.GetId() == self.RB_Ward.GetId():
            self.control.update_unit_type('Ward')
        else:
            self.control.update_unit_type('Branch')

    def OnStakeChanged(self, evt):
        self.control.update_stake_name(evt.GetString())

    def OnUseQuote(self, evt):
        if evt.Checked():
            self.control.allow_use_quote(True)
        else:
            self.control.allow_use_quote(False)

    def OnQuoteChanged(self, evt):
        self.control.update_quote(evt.GetString())

    def OnAuthorChanged(self, evt):
        self.control.update_author(evt.GetString())

    def OnRestoreQuote(self, evt):
        self.control.reset_quote()
