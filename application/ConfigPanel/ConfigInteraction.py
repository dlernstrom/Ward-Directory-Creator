# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx


class ConfigInteraction(object):
    def install(self, control, p):
        self.control = control

        # These particular widgets do not use the standard Bind call because
        # the widget is an amalgomation of two separate widgets
        p.memberCsvFile.changeCallback = self.on_member_csv_change
        p.nonMemberCsvFile.changeCallback = self.on_nonmember_csv_change
        p.dwellings_file.changeCallback = self.on_dwellings_csv_change
        p.ImagesDirectory.changeCallback = self.on_images_directory_change
        p.PDF_Out_Directory.changeCallback = self.on_pdf_directory_change
        p.Image_Archive_Directory.changeCallback = \
            self.on_archive_directory_change

        p.Bind(wx.EVT_CHECKBOX, self.on_override_phone, p.CB_OverridePhone)
        p.Bind(wx.EVT_COMBOBOX, self.on_select_missing_picture_contact,
               p.Contact_Dropdown)
        p.Bind(wx.EVT_TEXT, self.on_phone_txt_change, p.TXT_Phone)
        p.Bind(wx.EVT_COMBOBOX, self.on_select_email, p.Email_Dropdown)
        p.Bind(wx.EVT_BUTTON, self.on_add_email, p.BTN_AddEmail)
        p.Bind(wx.EVT_LISTBOX, self.on_listbox_clicked, p.EmailList)
        p.Bind(wx.EVT_LISTBOX_DCLICK, self.on_remove_email, p.EmailList)
        p.Bind(wx.EVT_BUTTON, self.on_remove_email, p.BTN_RemoveEmail)

    def on_member_csv_change(self, evt):
        self.control.update_member_csv_file_path(evt.GetString())

    def on_nonmember_csv_change(self, evt):
        self.control.update_nonmember_csv_file_path(evt.GetString())

    def on_dwellings_csv_change(self, evt):
        self.control.update_dwellings_csv_file_path(evt.GetString())

    def on_images_directory_change(self, evt):
        self.control.update_images_directory(evt.GetString())

    def on_pdf_directory_change(self, evt):
        self.control.update_pdf_directory(evt.GetString())

    def on_archive_directory_change(self, evt):
        self.control.update_archive_directory(evt.GetString())

    def on_select_missing_picture_contact(self, evt):
        self.control.update_missing_picture_contact(evt.GetString())

    def on_phone_txt_change(self, evt):
        self.control.update_missing_picture_contact_phone(evt.GetString())

    def on_override_phone(self, evt):
        if evt.Checked():
            self.control.override_missing_picture_contact_phone(True)
        else:
            self.control.override_missing_picture_contact_phone(False)

    def on_select_email(self, evt):
        self.control.email_address_selected_for_notifications()

    def on_add_email(self, evt):
        self.control.add_email_for_notifications()

    def on_listbox_clicked(self, evt):
        self.control.email_address_selected_for_notification_removal()

    def on_remove_email(self, evt):
        self.control.remove_notification_email_address()
