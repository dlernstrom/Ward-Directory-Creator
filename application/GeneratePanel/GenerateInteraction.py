# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx


class GenerateInteraction(object):
    def install(self, control, p):
        self.control = control
        p.Bind(wx.EVT_BUTTON, self.OnGoButton, p.BTN_Go)
        p.Bind(wx.EVT_CHECKBOX, self.OnCheckMissingReport, p.CB_MissingReport)
        p.Bind(wx.EVT_CHECKBOX, self.OnCheckMissingImages, p.CB_MissingImages)
        p.Bind(wx.EVT_CHECKBOX, self.OnCheckSendEmail, p.CB_SendEmail)
        p.Bind(wx.EVT_CHECKBOX, self.OnCheckMissingFile, p.CB_MissingFile)
        p.Bind(wx.EVT_CHECKBOX, self.OnCheckExtractMoveOuts,
               p.CB_ExtractMoveOuts)
        p.Bind(wx.EVT_CHECKBOX, self.OnCheckGenFull, p.CB_GenPDF_Full)
        p.Bind(wx.EVT_CHECKBOX, self.OnCheckGenBooklet,
               p.CB_GenPDF_Booklet)
        p.Bind(wx.EVT_CHECKBOX, self.OnCheckGenSing2Doub,
               p.CB_GenPDF_Single2Double)
        p.Bind(wx.EVT_TEXT, self.OnSMTPChanged, p.TXT_SMTPAddy)
        p.Bind(wx.EVT_TEXT, self.OnUserChanged, p.TXT_User)
        p.Bind(wx.EVT_TEXT, self.OnPassChanged, p.TXT_Pass)

    def OnSMTPChanged(self, evt):
        self.control.set_smtp(evt.GetString())

    def OnUserChanged(self, evt):
        self.control.set_smtp_user(evt.GetString())

    def OnPassChanged(self, evt):
        self.control.set_smtp_pass(evt.GetString())

    def OnCheckMissingReport(self, evt):
        if evt.Checked():
            self.control.set_miss_report('1')
        else:
            self.control.set_miss_report('0')

    def OnCheckMissingImages(self, evt):
        if evt.Checked():
            self.control.set_miss_images('1')
        else:
            self.control.set_miss_images('0')

    def OnCheckSendEmail(self, evt):
        if evt.Checked():
            self.control.set_send_email('1')
        else:
            self.control.set_send_email('0')

    def OnCheckMissingFile(self, evt):
        if evt.Checked():
            self.control.set_gen_miss_file('1')
        else:
            self.control.set_gen_miss_file('0')

    def OnCheckExtractMoveOuts(self, evt):
        if evt.Checked():
            self.control.set_extract_move_outs('1')
        else:
            self.control.set_extract_move_outs('0')

    def OnCheckGenFull(self, evt):
        if evt.Checked():
            self.control.set_gen_full('1')
        else:
            self.control.set_gen_full('0')

    def OnCheckGenBooklet(self, evt):
        if evt.Checked():
            self.control.set_gen_booklet('1')
        else:
            self.control.set_gen_booklet('0')

    def OnCheckGenSing2Doub(self, evt):
        if evt.Checked():
            self.control.set_gen_single2double('1')
        else:
            self.control.set_gen_single2double('0')

    def OnGoButton(self, evt):
        self.control.go()
