# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class ConfigControl(object):
    def __init__(self, app_handle, presentation, interaction):
        self.app_handle = app_handle
        self.presentation = presentation
        interaction.install(self, presentation)

    def LoadEmails(self):
        if not self.app_handle.get_conf_val('email.recipients') == None:
            r = self.app_handle.get_conf_val('email.recipients').split(',')
            self.presentation.EmailList.Clear()
            self.presentation.EmailList.InsertItems(r, 0)

    def SaveEmails(self):
        AllEmails = ','.join(self.presentation.EmailList.GetStrings())
        self.app_handle.set_conf_val('email.recipients', AllEmails)

    def making_active(self):
        self.LoadEmails()
        if self.app_handle.isValidCSV():
            self.presentation.StaticName.Enable(True)
            self.presentation.Contact_Dropdown.Enable(True)
            self.presentation.StaticPhone.Enable(True)
            self.presentation.StaticRecipients.Enable(True)
            self.presentation.Email_Dropdown.Enable(True)
            self.presentation.BTN_AddEmail.Enable(False)
            self.presentation.EmailList.Enable(True)
            self.presentation.BTN_RemoveEmail.Enable(False)

            # Refresh choices to name list
            self.presentation.Contact_Dropdown.Clear()
            NameList = self.app_handle.GetNameList(
                NameType='Parent')
            for Name in NameList:
                self.presentation.Contact_Dropdown.Append(Name)
            if self.app_handle.get_conf_val('missing.missingname') in NameList:
                self.presentation.Contact_Dropdown.SetStringSelection(
                    self.app_handle.get_conf_val('missing.missingname'))
                self.presentation.CB_OverridePhone.Enable(True)
                if self.app_handle.get_conf_val('missing.overridephone') == '1':
                    self.presentation.TXT_Phone.Enable(True)
                    if self.app_handle.get_conf_val('missing.missingphone'):
                        self.presentation.TXT_Phone.SetValue(
                            self.app_handle.get_conf_val('missing.missingphone'))
                else:
                    self.presentation.TXT_Phone.Enable(False)
                    self.presentation.TXT_Phone.SetValue(
                        self.app_handle.GetPhoneNumber(
                            self.app_handle.get_conf_val('missing.missingname')))
            else:
                if self.app_handle.get_conf_val('missing.missingname'):
                    OldMissingName = self.app_handle.get_conf_val('missing.missingname')
                self.presentation.TXT_Phone.Enable(False)
                self.presentation.CB_OverridePhone.Enable(False)

            # Now let's populate the email addresses
            EmailAddys = self.app_handle.GetMemberEmails()
            self.presentation.Email_Dropdown.Clear()
            for Email in EmailAddys:
                self.presentation.Email_Dropdown.Append(Email)
        else:
            self.presentation.StaticName.Enable(False)
            self.presentation.Contact_Dropdown.Enable(False)
            self.presentation.StaticPhone.Enable(False)
            self.presentation.TXT_Phone.Enable(False)
            self.presentation.CB_OverridePhone.Enable(False)
            self.presentation.StaticRecipients.Enable(False)
            self.presentation.Email_Dropdown.Enable(False)
            self.presentation.BTN_AddEmail.Enable(False)
            self.presentation.EmailList.Enable(False)
            self.presentation.BTN_RemoveEmail.Enable(False)

        #Here's the logic to set up the prevalues from config file
        if self.app_handle.get_conf_val('file.member_csv_location'):
            self.presentation.memberCsvFile.SetValue(
                self.app_handle.get_conf_val('file.member_csv_location'))
        if self.app_handle.get_conf_val('file.nonmember_csv_location'):
            self.presentation.nonMemberCsvFile.SetValue(
                self.app_handle.get_conf_val('file.nonmember_csv_location'))
        if self.app_handle.get_conf_val('file.imagesdirectory'):
            self.presentation.ImagesDirectory.SetValue(
                self.app_handle.get_conf_val('file.imagesdirectory'))
        if self.app_handle.get_conf_val('file.pdf_outdirectory'):
            self.presentation.PDF_Out_Directory.SetValue(
                self.app_handle.get_conf_val('file.pdf_outdirectory'))
        if self.app_handle.get_conf_val('file.imagearchivedir'):
            self.presentation.Image_Archive_Directory.SetValue(
                self.app_handle.get_conf_val('file.imagearchivedir'))
        if self.app_handle.get_conf_val('missing.overridephone') == '1':
            self.presentation.CB_OverridePhone.SetValue(True)
        else:
            self.presentation.CB_OverridePhone.SetValue(False)

    def update_member_csv_file_path(self, new_val):
        self.app_handle.set_conf_val('file.member_csv_location', new_val)
        self.making_active()

    def update_nonmember_csv_file_path(self, new_val):
        self.app_handle.set_conf_val('file.nonmember_csv_location', new_val)
        self.making_active()

    def update_images_directory(self, new_val):
        self.app_handle.set_conf_val('file.imagesdirectory', new_val)

    def update_pdf_directory(self, new_val):
        self.app_handle.set_conf_val('file.pdf_outdirectory', new_val)

    def update_archive_directory(self, new_val):
        self.app_handle.set_conf_val('file.imagearchivedir', new_val)

    def update_missing_picture_contact(self, new_val):
        self.app_handle.set_conf_val('missing.missingname', new_val)
        self.presentation.CB_OverridePhone.SetValue(False)
        self.presentation.CB_OverridePhone.Enable(True)
        phone = self.app_handle.GetPhoneNumber(new_val)
        self.presentation.TXT_Phone.SetValue(phone)
        self.presentation.TXT_Phone.Enable(False)

    def update_missing_picture_contact_phone(self, new_val):
        self.app_handle.set_conf_val('missing.missingphone', new_val)

    def override_missing_picture_contact_phone(self, override):
        if override:
            self.app_handle.set_conf_val('missing.overridephone', '1')
            self.presentation.TXT_Phone.Enable(True)
        else:
            self.app_handle.set_conf_val('missing.overridephone', '0')
            self.presentation.TXT_Phone.Enable(False)
            missing_name = self.app_handle.get_conf_val('missing.missingname')
            phone = self.app_handle.GetPhoneNumber(missing_name)
            self.presentation.TXT_Phone.SetValue(phone)

    def email_address_selected_for_notifications(self):
        self.presentation.BTN_AddEmail.Enable(True)

    def add_email_for_notifications(self):
        self.presentation.BTN_AddEmail.Enable(False)
        self.presentation.EmailList.Append(
            self.presentation.Email_Dropdown.GetStringSelection())
        # Clear for next usage
        self.presentation.clear_email_selection()
        self.SaveEmails()

    def email_address_selected_for_notification_removal(self):
        self.presentation.BTN_RemoveEmail.Enable(True)

    def remove_notification_email_address(self):
        self.presentation.EmailList.Delete(
            self.presentation.EmailList.GetSelection())
        self.presentation.BTN_RemoveEmail.Enable(False)
        self.SaveEmails()
