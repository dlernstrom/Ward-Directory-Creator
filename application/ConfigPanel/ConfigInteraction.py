# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx


class ConfigInteraction(object):
    def install(self, control, p):
        self.control = control
        p.Bind(wx.EVT_CHECKBOX, self.OnOverridePhone, p.CB_OverridePhone)
        p.Bind(wx.EVT_COMBOBOX, self.OnSelectMissing, p.Contact_Dropdown)
        p.Bind(wx.EVT_TEXT, self.OnPhoneText, p.TXT_Phone)
        p.Bind(wx.EVT_COMBOBOX, self.OnSelectEmail, p.Email_Dropdown)
        p.Bind(wx.EVT_BUTTON, self.OnAddEmail, p.BTN_AddEmail)
        p.Bind(wx.EVT_LISTBOX, self.ListboxClicked, p.EmailList)
        p.Bind(wx.EVT_LISTBOX_DCLICK, self.OnRemoveEmail, p.EmailList)
        p.Bind(wx.EVT_BUTTON, self.OnRemoveEmail, p.BTN_RemoveEmail)

    def new_member_csv_file_callback(self, evt):
        self.app_handle.set_conf_val('file.member_csv_location',
                                     evt.GetString())
        # This will call an error if the handler
        # is called prior to init being completed
        try:
            self.control.making_active()
        except AttributeError:
            pass

    def new_nonmember_csv_file_callback(self, evt):
        self.app_handle.set_conf_val('file.nonmember_csv_location',
                                     evt.GetString())
        # This will call an error if the handler
        # is called prior to init being completed
        try:
            self.control.making_active()
        except AttributeError:
            pass

    def NewImagesDirectory(self, evt):
        self.app_handle.set_conf_val('file.imagesdirectory', evt.GetString())

    def NewPDFDirectory(self, evt):
        self.app_handle.set_conf_val('file.pdf_outdirectory',
                                     evt.GetString())

    def NewArchiveDirectory(self, evt):
        self.app_handle.set_conf_val('file.imagearchivedir', evt.GetString())

    def OnSelectMissing(self, evt):
        self.app_handle.set_conf_val('missing.missingname', evt.GetString())
        self.presentation.CB_OverridePhone.SetValue(False)
        self.presentation.CB_OverridePhone.Enable(True)
        NameInQuestion = self.app_handle.get_conf_val('missing.missingname')
        Phone = self.app_handle.GetPhoneNumber(NameInQuestion)
        self.presentation.TXT_Phone.SetValue(Phone)
        self.presentation.TXT_Phone.Enable(False)

    def OnPhoneText(self, evt):
        self.app_handle.set_conf_val('missing.missingphone', evt.GetString())

    def OnOverridePhone(self, evt):
        if evt.Checked():
            self.app_handle.set_conf_val('missing.overridephone', '1')
            self.presentation.TXT_Phone.Enable(True)
        else:
            self.app_handle.set_conf_val('missing.overridephone', '0')
            self.presentation.TXT_Phone.Enable(False)
            NameInQuestion = self.app_handle.get_conf_val('missing.missingname')
            Phone = self.app_handle.GetPhoneNumber(NameInQuestion)
            self.presentation.TXT_Phone.SetValue(Phone)

    def OnSelectEmail(self, evt):
        self.presentation.BTN_AddEmail.Enable(True)

    def OnAddEmail(self, evt):
        # TODO: Remove the entry from the list of choices...
        self.presentation.BTN_AddEmail.Enable(False)
        self.presentation.EmailList.Append(
            self.presentation.Email_Dropdown.GetStringSelection())
        # Clear for next usage
        self.presentation.Email_Dropdown.SetSelection(wx.NOT_FOUND)
        self.control.SaveEmails()

    def ListboxClicked(self, evt):
        self.presentation.BTN_RemoveEmail.Enable(True)

    def OnRemoveEmail(self, evt):
        self.presentation.EmailList.Delete(
            self.presentation.EmailList.GetSelection())
        self.presentation.BTN_RemoveEmail.Enable(False)
        self.control.SaveEmails()
