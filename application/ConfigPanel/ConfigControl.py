# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class ConfigControl(object):
    def __init__(self, abstraction, presentation, interaction):
        self.abstraction = abstraction
        self.presentation = presentation
        interaction.install(self, presentation)

    def LoadEmails(self):
        if len(self.abstraction.email_recipients):
            r = self.abstraction.email_recipients
            self.presentation.EmailList.Clear()
            self.presentation.EmailList.InsertItems(r, 0)

    def SaveEmails(self):
        emails = self.presentation.EmailList.GetStrings()
        self.abstraction.email_recipients = emails

    def making_active(self):
        self.LoadEmails()
        if self.abstraction.is_valid_csv:
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
            NameList = self.abstraction.get_name_list(NameType='Parent')
            for Name in NameList:
                self.presentation.Contact_Dropdown.Append(Name)
            if self.abstraction.missing_missing_name in NameList:
                self.presentation.Contact_Dropdown.SetStringSelection(
                    self.abstraction.missing_missing_name)
                self.presentation.CB_OverridePhone.Enable(True)
                if self.abstraction.overridephone:
                    self.presentation.TXT_Phone.Enable(True)
                    if self.abstraction.missing_missingphone:
                        self.presentation.TXT_Phone.SetValue(
                            self.abstraction.missing_missingphone)
                else:
                    self.presentation.TXT_Phone.Enable(False)
                    phone = self.abstraction.get_missing_contact_default_phone()
                    self.presentation.TXT_Phone.SetValue(phone)
            else:
                self.presentation.TXT_Phone.Enable(False)
                self.presentation.CB_OverridePhone.Enable(False)

            # Now let's populate the email addresses
            EmailAddys = self.abstraction.get_member_emails()
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
        if self.abstraction.member_csv_location:
            self.presentation.memberCsvFile.SetValue(
                self.abstraction.member_csv_location)
        if self.abstraction.nonmember_csv_location:
            self.presentation.nonMemberCsvFile.SetValue(
                self.abstraction.nonmember_csv_location)
        if self.abstraction.file_images_directory:
            self.presentation.ImagesDirectory.SetValue(
                self.abstraction.file_images_directory)
        if self.abstraction.file_pdf_out_directory:
            self.presentation.PDF_Out_Directory.SetValue(
                self.abstraction.file_pdf_out_directory)
        if self.abstraction.file_image_archive_directory:
            self.presentation.Image_Archive_Directory.SetValue(
                self.abstraction.file_image_archive_directory)
        self.presentation.CB_OverridePhone.SetValue(self.abstraction.overridephone)

    def update_member_csv_file_path(self, new_val):
        if not self.abstraction.member_csv_location == new_val:
            self.abstraction.member_csv_location = new_val
            self.making_active()

    def update_nonmember_csv_file_path(self, new_val):
        if not self.abstraction.nonmember_csv_location == new_val:
            self.abstraction.nonmember_csv_location = new_val
            self.making_active()

    def update_dwellings_csv_file_path(self, new_val):
        self.abstraction.file_dwellings_csv_location = new_val

    def update_images_directory(self, new_val):
        self.abstraction.file_images_directory = new_val

    def update_pdf_directory(self, new_val):
        self.abstraction.file_pdf_out_directory = new_val

    def update_archive_directory(self, new_val):
        self.abstraction.file_image_archive_directory = new_val

    def update_missing_picture_contact(self, new_val):
        self.abstraction.missing_missing_name = new_val
        self.presentation.CB_OverridePhone.SetValue(False)
        self.presentation.CB_OverridePhone.Enable(True)
        phone = self.abstraction.get_missing_contact_default_phone()
        self.presentation.TXT_Phone.SetValue(phone)
        self.presentation.TXT_Phone.Enable(False)

    def update_missing_picture_contact_phone(self, new_val):
        self.abstraction.missingphone = new_val

    def override_missing_picture_contact_phone(self, override):
        self.abstraction.overridephone = override
        self.presentation.TXT_Phone.Enable(override)
        if not override:
            ph = self.abstraction.get_missing_contact_default_phone()
            self.presentation.TXT_Phone.SetValue(ph)

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
