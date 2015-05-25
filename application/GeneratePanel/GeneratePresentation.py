# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx
from wx.lib.dialogs import ScrolledMessageDialog

from application.ColoredPanel import ColoredPanel


class GeneratePresentation(ColoredPanel):
    def __init__(self, parent):
        super(GeneratePresentation, self).__init__(parent, None)
        #######################################################################
        ## Here's the email config box
        EmailBox = wx.StaticBox(self, -1, "Email Configuration")
        EmailBox.SetFont(self.StandardFont)
        EmailBoxSizer = wx.StaticBoxSizer(EmailBox, wx.VERTICAL)

        self.StaticSMTP = wx.StaticText(self, -1, "SMTP Server")
        self.StaticSMTP.SetFont(self.StandardFont)
        EmailBoxSizer.Add(self.StaticSMTP, 0, wx.TOP | wx.LEFT, 10)

        self.TXT_SMTPAddy = wx.TextCtrl(self, -1, size = (200, -1))
        self.TXT_SMTPAddy.SetFont(self.StandardFont)
        EmailBoxSizer.Add(self.TXT_SMTPAddy, 0, wx.TOP | wx.LEFT, 10)

        self.StaticUser = wx.StaticText(self, -1, "User Name")
        self.StaticUser.SetFont(self.StandardFont)
        EmailBoxSizer.Add(self.StaticUser, 0, wx.TOP | wx.LEFT, 10)

        self.TXT_User = wx.TextCtrl(self, -1, size = (200, -1))
        self.TXT_User.SetFont(self.StandardFont)
        EmailBoxSizer.Add(self.TXT_User, 0, wx.TOP | wx.LEFT, 10)

        self.StaticPass = wx.StaticText(self, -1, "Password")
        self.StaticPass.SetFont(self.StandardFont)
        EmailBoxSizer.Add(self.StaticPass, 0, wx.TOP | wx.LEFT, 10)

        self.TXT_Pass = wx.TextCtrl(self, -1, size=(200, -1),
                                    style=wx.TE_PASSWORD)
        self.TXT_Pass.SetFont(self.StandardFont)
        EmailBoxSizer.Add(self.TXT_Pass, 0, wx.TOP | wx.LEFT, 10)

        #######################################################################
        ## Here's the generate directory box
        StaticBox = wx.StaticBox(self, -1, "Generate Directory")
        StaticBox.SetFont(self.StandardFont)
        GenerateSizer = wx.StaticBoxSizer(StaticBox, wx.VERTICAL)

        self.CB_MissingReport = wx.CheckBox(self, -1,
                                            "View Missing Pictures Report")
        self.CB_MissingReport.SetFont(self.StandardFont)
        GenerateSizer.Add(self.CB_MissingReport, 0, wx.TOP | wx.LEFT, 10)

        self.CB_MissingImages = wx.CheckBox(self, -1, "View Missing Images")
        self.CB_MissingImages.SetFont(self.StandardFont)
        GenerateSizer.Add(self.CB_MissingImages, 0, wx.TOP | wx.LEFT, 10)

        self.CB_SendEmail = wx.CheckBox(self, -1,
                                        "Send Missing Pictures Email")
        self.CB_SendEmail.SetFont(self.StandardFont)
        GenerateSizer.Add(self.CB_SendEmail, 0, wx.TOP | wx.LEFT, 10)

        self.CB_MissingFile = wx.CheckBox(self, -1,
                                          "Generate Missing Pictures File")
        self.CB_MissingFile.SetFont(self.StandardFont)
        GenerateSizer.Add(self.CB_MissingFile, 0, wx.TOP | wx.LEFT, 10)

        self.CB_ExtractMoveOuts = wx.CheckBox(self, -1,
                                              'Archive "Moved-Out" Images')
        self.CB_ExtractMoveOuts.SetFont(self.StandardFont)
        GenerateSizer.Add(self.CB_ExtractMoveOuts, 0, wx.TOP | wx.LEFT, 10)

        self.CB_GenPDF_Full = wx.CheckBox(self, -1, "Generate Full Spread PDF")
        self.CB_GenPDF_Full.SetFont(self.StandardFont)
        GenerateSizer.Add(self.CB_GenPDF_Full, 0, wx.TOP | wx.LEFT, 10)

        self.CB_GenPDF_Booklet = wx.CheckBox(self, -1, "Generate Booklet PDF")
        self.CB_GenPDF_Booklet.SetFont(self.StandardFont)
        GenerateSizer.Add(self.CB_GenPDF_Booklet, 0, wx.TOP | wx.LEFT, 10)

        self.CB_GenPDF_Single2Double = wx.CheckBox(
            self, -1, "Generate Single2Double PDF")
        self.CB_GenPDF_Single2Double.SetFont(self.StandardFont)
        GenerateSizer.Add(self.CB_GenPDF_Single2Double, 0,
                          wx.TOP | wx.LEFT, 10)

        self.BTN_Go = wx.Button(self, -1, "Go!")
        self.BTN_Go.SetFont(self.StandardFont)
        GenerateSizer.Add(self.BTN_Go, 0,
                          wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 10)

        #######################################################################
        ## Here's the outer sizer container stuff
        border_level1_left = wx.BoxSizer(wx.VERTICAL)
        border_level1_left.Add(GenerateSizer, 1, wx.EXPAND | wx.ALL, 25)

        border_level0 = wx.BoxSizer(wx.HORIZONTAL)
        border_level0.Add(border_level1_left, 1, wx.EXPAND | wx.ALL, 25)
        border_level0.Add(EmailBoxSizer, 1, wx.EXPAND | wx.ALL, 25)

        self.SetSizer(border_level0)
        border_level0.SetDimension(0, 0, self.GetSize()[0], self.GetSize()[1])

    def show_report(self, msg):
        dlg = ScrolledMessageDialog(self, msg, caption="Report",
                                    size=(500, 600))
        dlg.ShowModal()
