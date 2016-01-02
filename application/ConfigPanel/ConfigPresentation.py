# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx
from wx.lib.filebrowsebutton import FileBrowseButton, DirBrowseButton

from application.ColoredPanel import ColoredPanel


class ConfigPresentation(ColoredPanel):
    def __init__(self, parent):
        super(ConfigPresentation, self).__init__(parent, None)
        #######################################################################
        ## File/Folder Configuration
        box = wx.StaticBox(self, -1, "File/Folder Configuration")
        box.SetFont(self.StandardFont)
        folder_box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.memberCsvFile = FileBrowseButton(
            self, -1, size=(700, 30), labelText="Membership File",
            fileMask="*.csv")
        folder_box_sizer.Add(self.memberCsvFile, 0, wx.TOP | wx.LEFT, 10)

        self.nonMemberCsvFile = FileBrowseButton(
            self, -1, size=(700, 30), labelText="Nonmember File",
            fileMask="*.csv")
        folder_box_sizer.Add(self.nonMemberCsvFile, 0, wx.TOP | wx.LEFT, 10)

        self.dwellings_file = FileBrowseButton(
            self, -1, size=(700, 30), labelText="Dwellings File",
            fileMask="*.csv")
        folder_box_sizer.Add(self.dwellings_file, 0, wx.TOP | wx.LEFT, 10)

        self.ImagesDirectory = DirBrowseButton(
            self, -1, size=(700, 30), labelText="Images Directory",
            changeCallback=lambda x:x)
        folder_box_sizer.Add(self.ImagesDirectory, 0, wx.TOP | wx.LEFT, 10)

        self.PDF_Out_Directory = DirBrowseButton(
            self, -1, size=(700, 30), labelText="PDF Output Directory",
            changeCallback=lambda x:x)
        folder_box_sizer.Add(self.PDF_Out_Directory, 0, wx.TOP | wx.LEFT, 10)

        self.Image_Archive_Directory = DirBrowseButton(
            self, -1, size=(700, 30), labelText="Image Archive Directory",
            changeCallback=lambda x:x)
        folder_box_sizer.Add(self.Image_Archive_Directory, 0,
                             wx.TOP | wx.LEFT | wx.BOTTOM, 10)

        #######################################################################
        ## Missing Image Configuration Section
        box = wx.StaticBox(self, -1, "Missing Image Configuration")
        box.SetFont(self.StandardFont)
        missing_box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.StaticName = wx.StaticText(self, -1, "Contact Name:")
        self.StaticName.SetFont(self.StandardFont)
        missing_box_sizer.Add(self.StaticName, 0, wx.TOP | wx.LEFT, 10)

        self.Contact_Dropdown = wx.ComboBox(self, -1, size=(250, -1),
                                            style=wx.CB_READONLY )
        self.Contact_Dropdown.SetFont(self.TextBoxFont)
        missing_box_sizer.Add(self.Contact_Dropdown, 0, wx.TOP | wx.LEFT, 10)

        self.StaticPhone = wx.StaticText(self, -1, "Contact Phone:")
        self.StaticPhone.SetFont(self.StandardFont)
        missing_box_sizer.Add(self.StaticPhone, 0, wx.TOP | wx.LEFT, 10)

        self.TXT_Phone = wx.TextCtrl(self, -1, size=(250,-1))
        self.TXT_Phone.SetFont(self.TextBoxFont)
        missing_box_sizer.Add(self.TXT_Phone, 0, wx.TOP | wx.LEFT, 10)

        self.CB_OverridePhone = wx.CheckBox(self, -1, "Override Phone")
        self.CB_OverridePhone.SetFont(self.StandardFont)
        missing_box_sizer.Add(self.CB_OverridePhone, 0, wx.TOP | wx.LEFT, 10)

        #######################################################################
        ## Email Configuration Section
        email_box = wx.StaticBox(self, -1, "Email Configuration")
        email_box.SetFont(self.StandardFont)
        email_box_sizer = wx.StaticBoxSizer(email_box, wx.VERTICAL)

        self.StaticRecipients = wx.StaticText(self, -1, "Email Recipients")
        self.StaticRecipients.SetFont(self.StandardFont)
        email_box_sizer.Add(self.StaticRecipients, 0, wx.TOP | wx.LEFT, 10)

        self.Email_Dropdown = wx.ComboBox(self, -1, size=(390, 24),
                                          style=wx.CB_READONLY)
        self.Email_Dropdown.SetFont(self.TextBoxFont)
        email_box_sizer.Add(self.Email_Dropdown, 0, wx.TOP | wx.LEFT, 10)

        self.BTN_AddEmail = wx.Button(self, wx.ID_ADD)
        self.BTN_AddEmail.SetFont(self.TextBoxFont)
        email_box_sizer.Add(self.BTN_AddEmail, 0, wx.TOP | wx.LEFT, 10)

        self.EmailList = wx.ListBox(self, -1, size=(390, 151))
        self.EmailList.SetFont(self.TextBoxFont)
        email_box_sizer.Add(self.EmailList, 1, wx.TOP | wx.LEFT, 10)

        self.BTN_RemoveEmail = wx.Button(self, wx.ID_REMOVE)
        self.BTN_RemoveEmail.SetFont(self.TextBoxFont)
        email_box_sizer.Add(self.BTN_RemoveEmail, 0, wx.TOP | wx.LEFT, 10)

        #######################################################################
        ## Non wrapped items
        logo = wx.StaticBitmap(self, -1, self.logo_bmp,
                               (self.logo_bmp.GetWidth(),
                                self.logo_bmp.GetHeight()))

        #######################################################################
        ## Sizer encapsulation section
        bottom_left_level3 = wx.BoxSizer(wx.VERTICAL)
        bottom_left_level3.Add(logo, 0, wx.BOTTOM, 25)
        bottom_left_level3.Add(missing_box_sizer, 1, wx.EXPAND)

        bottom_right_level3 = wx.BoxSizer()
        bottom_right_level3.Add(email_box_sizer, 5, wx.EXPAND)

        bottom_level2 = wx.BoxSizer(wx.HORIZONTAL)
        bottom_level2.Add(bottom_left_level3, 2, wx.EXPAND)
        bottom_level2.Add(bottom_right_level3, 3, wx.EXPAND | wx.LEFT, 25)

        inside_border_level1 = wx.BoxSizer(wx.VERTICAL)
        inside_border_level1.Add(folder_box_sizer, 0, wx.EXPAND | wx.BOTTOM, 25)
        inside_border_level1.Add(bottom_level2, 1, wx.EXPAND)

        border_level0 = wx.BoxSizer()
        border_level0.Add(inside_border_level1, 1, wx.EXPAND | wx.ALL, 25)
        self.SetSizer(border_level0)
        border_level0.SetDimension(0, 0, self.GetSize()[0], self.GetSize()[1])

    def clear_email_selection(self):
        self.Email_Dropdown.SetSelection(wx.NOT_FOUND)
