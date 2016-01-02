# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class ConfigAbstraction(object):
    def __init__(self, app_handle):
        self.app_handle = app_handle

    @property
    def email_recipients(self):
        email_recipients = self.app_handle.email_recipients
        if email_recipients:
            return email_recipients.split(',')
        return []

    @email_recipients.setter
    def email_recipients(self, email_list):
        email_string = ','.join(email_list)
        self.app_handle.email_recipients = email_string

    @property
    def is_valid_csv(self):
        return self.app_handle.isValidCSV()

    def get_name_list(self, *args, **kwargs):
        return self.app_handle.GetNameList(*args, **kwargs)

    def get_member_emails(self, *args, **kwargs):
        return self.app_handle.GetMemberEmails(*args, **kwargs)

    @property
    def overridephone(self):
        return self.app_handle.missing_overridephone == '1'

    @overridephone.setter
    def overridephone(self, new_val):
        if new_val:
            self.app_handle.missing_overridephone = '1'
        else:
            self.app_handle.missing_overridephone = '0'

    @property
    def missing_missing_name(self):
        return self.app_handle.missing_missing_name

    @missing_missing_name.setter
    def missing_missing_name(self, new_val):
        self.app_handle.missing_missing_name = new_val

    @property
    def missing_missingphone(self):
        return self.app_handle.missing_missingphone

    @missing_missingphone.setter
    def missing_missingphone(self, new_val):
        self.app_handle.missing_missingphone = new_val

    def get_missing_contact_default_phone(self):
        return self.app_handle.GetPhoneNumber(self.missing_missing_name)

    @property
    def member_csv_location(self):
        return self.app_handle.file_member_csv_location

    @member_csv_location.setter
    def member_csv_location(self, new_val):
        self.app_handle.file_member_csv_location = new_val
        self.app_handle.GetMembershipList()
        self.app_handle.SetLists()

    @property
    def nonmember_csv_location(self):
        return self.app_handle.file_nonmember_csv_location

    @nonmember_csv_location.setter
    def nonmember_csv_location(self, new_val):
        self.app_handle.file_nonmember_csv_location = new_val
        self.app_handle.GetMembershipList()
        self.app_handle.SetLists()

    @property
    def file_dwellings_csv_location(self):
        return self.app_handle.file_dwellings_csv_location

    @file_dwellings_csv_location.setter
    def file_dwellings_csv_location(self, new_val):
        self.app_handle.file_dwellings_csv_location = new_val

    @property
    def file_images_directory(self):
        return self.app_handle.file_images_directory

    @file_images_directory.setter
    def file_images_directory(self, new_val):
        self.app_handle.file_images_directory = new_val

    @property
    def file_pdf_out_directory(self):
        return self.app_handle.file_pdf_out_directory

    @file_pdf_out_directory.setter
    def file_pdf_out_directory(self, new_val):
        self.app_handle.file_pdf_out_directory = new_val

    @property
    def file_image_archive_directory(self):
        return self.app_handle.file_image_archive_directory

    @file_image_archive_directory.setter
    def file_image_archive_directory(self, new_val):
        self.app_handle.file_image_archive_directory = new_val
