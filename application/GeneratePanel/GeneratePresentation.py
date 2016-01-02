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
        box = wx.StaticBox(self, -1, "Email Configuration")
        box.SetFont(self.StandardFont)
        email_box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        smtp_title = wx.StaticText(self, -1, "SMTP Server")
        smtp_title.SetFont(self.StandardFont)
        email_box_sizer.Add(smtp_title, 0, wx.TOP | wx.LEFT, 10)

        self.TXT_SMTPAddy = wx.TextCtrl(self, -1, size=(200, -1))
        self.TXT_SMTPAddy.SetFont(self.StandardFont)
        email_box_sizer.Add(self.TXT_SMTPAddy, 0, wx.TOP | wx.LEFT, 10)

        username_title = wx.StaticText(self, -1, "User Name")
        username_title.SetFont(self.StandardFont)
        email_box_sizer.Add(username_title, 0, wx.TOP | wx.LEFT, 10)

        self.TXT_User = wx.TextCtrl(self, -1, size=(200, -1))
        self.TXT_User.SetFont(self.StandardFont)
        email_box_sizer.Add(self.TXT_User, 0, wx.TOP | wx.LEFT, 10)

        pass_title = wx.StaticText(self, -1, "Password")
        pass_title.SetFont(self.StandardFont)
        email_box_sizer.Add(pass_title, 0, wx.TOP | wx.LEFT, 10)

        self.TXT_Pass = wx.TextCtrl(self, -1, size=(200, -1),
                                    style=wx.TE_PASSWORD)
        self.TXT_Pass.SetFont(self.StandardFont)
        email_box_sizer.Add(self.TXT_Pass, 0, wx.TOP | wx.LEFT, 10)

        #######################################################################
        ## Here's the generate directory box
        box = wx.StaticBox(self, -1, "Generate Directory")
        box.SetFont(self.StandardFont)
        gen_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.CB_MissingReport = wx.CheckBox(self, -1,
                                            "View Missing Pictures Report")
        self.CB_MissingReport.SetFont(self.StandardFont)
        gen_sizer.Add(self.CB_MissingReport, 0, wx.TOP | wx.LEFT, 10)

        self.CB_MissingImages = wx.CheckBox(self, -1, "View Missing Images")
        self.CB_MissingImages.SetFont(self.StandardFont)
        gen_sizer.Add(self.CB_MissingImages, 0, wx.TOP | wx.LEFT, 10)

        self.CB_SendEmail = wx.CheckBox(self, -1,
                                        "Send Missing Pictures Email")
        self.CB_SendEmail.SetFont(self.StandardFont)
        gen_sizer.Add(self.CB_SendEmail, 0, wx.TOP | wx.LEFT, 10)

        self.CB_MissingFile = wx.CheckBox(self, -1,
                                          "Generate Missing Pictures File")
        self.CB_MissingFile.SetFont(self.StandardFont)
        gen_sizer.Add(self.CB_MissingFile, 0, wx.TOP | wx.LEFT, 10)

        self.CB_ExtractMoveOuts = wx.CheckBox(self, -1,
                                              'Archive "Moved-Out" Images')
        self.CB_ExtractMoveOuts.SetFont(self.StandardFont)
        gen_sizer.Add(self.CB_ExtractMoveOuts, 0, wx.TOP | wx.LEFT, 10)

        self.CB_GenPDF_Full = wx.CheckBox(self, -1, "Generate Full Spread PDF")
        self.CB_GenPDF_Full.SetFont(self.StandardFont)
        gen_sizer.Add(self.CB_GenPDF_Full, 0, wx.TOP | wx.LEFT, 10)

        self.CB_GenPDF_Booklet = wx.CheckBox(self, -1, "Generate Booklet PDF")
        self.CB_GenPDF_Booklet.SetFont(self.StandardFont)
        gen_sizer.Add(self.CB_GenPDF_Booklet, 0, wx.TOP | wx.LEFT, 10)

        self.CB_GenPDF_Single2Double = wx.CheckBox(
            self, -1, "Generate Single2Double PDF")
        self.CB_GenPDF_Single2Double.SetFont(self.StandardFont)
        gen_sizer.Add(self.CB_GenPDF_Single2Double, 0,
                      wx.TOP | wx.LEFT, 10)

        self.BTN_Go = wx.Button(self, -1, "Go!")
        self.BTN_Go.SetFont(self.StandardFont)
        gen_sizer.Add(self.BTN_Go, 0,
                      wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 10)

        #######################################################################
        ## Here's the outer sizer container stuff
        border_level1_left = wx.BoxSizer(wx.VERTICAL)
        border_level1_left.Add(gen_sizer, 1, wx.EXPAND | wx.ALL, 25)

        border_level0 = wx.BoxSizer(wx.HORIZONTAL)
        border_level0.Add(border_level1_left, 1, wx.EXPAND | wx.ALL, 25)
        border_level0.Add(email_box_sizer, 1, wx.EXPAND | wx.ALL, 25)

        self.SetSizer(border_level0)
        border_level0.SetDimension(0, 0, self.GetSize()[0], self.GetSize()[1])

    def show_report(self, msg):
        dlg = ScrolledMessageDialog(self, msg, caption="Report",
                                    size=(500, 600))
        dlg.ShowModal()

    @property
    def smtp_addy(self):
        return self.TXT_SMTPAddy.GetValue()

    @smtp_addy.setter
    def smtp_addy(self, new_val):
        self.TXT_SMTPAddy.SetValue(new_val)

    @property
    def smtp_user(self):
        return self.TXT_User.GetValue()

    @smtp_user.setter
    def smtp_user(self, new_val):
        self.TXT_User.SetValue(new_val)

    @property
    def smtp_pass(self):
        return self.TXT_Pass.GetValue()

    @smtp_pass.setter
    def smtp_pass(self, new_val):
        self.TXT_Pass.SetValue(new_val)

    @property
    def gen_missing_rpt(self):
        return self.CB_MissingReport.GetValue()

    @gen_missing_rpt.setter
    def gen_missing_rpt(self, new_val):
        self.CB_MissingReport.SetValue(new_val)

    @property
    def gen_missing_img_rpt(self):
        return self.CB_MissingImages.GetValue()

    @gen_missing_img_rpt.setter
    def gen_missing_img_rpt(self, new_val):
        self.CB_MissingImages.SetValue(new_val)

    @property
    def send_email(self):
        return self.CB_SendEmail.GetValue()

    @send_email.setter
    def send_email(self, new_val):
        return self.CB_SendEmail.SetValue(new_val)

    @property
    def gen_missing_img_file(self):
        return self.CB_MissingFile.GetValue()

    @gen_missing_img_file.setter
    def gen_missing_img_file(self, new_val):
        self.CB_MissingFile.SetValue(new_val)

    @property
    def extract_move_outs(self):
        return self.CB_ExtractMoveOuts.GetValue()

    @extract_move_outs.setter
    def extract_move_outs(self, new_val):
        self.CB_ExtractMoveOuts.SetValue(new_val)

    @property
    def gen_pdf_full(self):
        return self.CB_GenPDF_Full.GetValue()

    @gen_pdf_full.setter
    def gen_pdf_full(self, new_val):
        self.CB_GenPDF_Full.SetValue(new_val)

    @property
    def gen_pdf_booklet(self):
        return self.CB_GenPDF_Booklet.GetValue()

    @gen_pdf_booklet.setter
    def gen_pdf_booklet(self, new_val):
        self.CB_GenPDF_Booklet.SetValue(new_val)

    @property
    def gen_pdf_single2double(self):
        return self.CB_GenPDF_Single2Double.GetValue()

    @gen_pdf_single2double.setter
    def gen_pdf_single2double(self, new_val):
        self.CB_GenPDF_Single2Double.SetValue(new_val)
