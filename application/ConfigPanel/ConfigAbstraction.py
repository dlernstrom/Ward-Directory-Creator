# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class ConfigAbstraction(object):
    def __init__(self, app_handle):
        self.app_handle = app_handle

    @property
    def email_recipients(self):
        email_recipients = self.app_handle.get_conf_val('email.recipients')
        if email_recipients:
            return email_recipients.split(',')
        return []

    @email_recipients.setter
    def email_recipients(self, email_list):
        email_string = ','.join(email_list)
        self.app_handle.set_conf_val('email.recipients', email_string)

    @property
    def is_valid_csv(self):
        return self.app_handle.isValidCSV()

    def get_name_list(self, *args, **kwargs):
        return self.app_handle.GetNameList(*args, **kwargs)

    def get_member_emails(self, *args, **kwargs):
        return self.app_handle.GetMemberEmails(*args, **kwargs)

    @property
    def missingname(self):
        return self.app_handle.get_conf_val('missing.missingname')

    @property
    def overridephone(self):
        return self.app_handle.get_conf_val('missing.overridephone') == '1'

    @overridephone.setter
    def overridephone(self, new_val):
        if new_val:
            self.app_handle.set_conf_val('missing.overridephone', '1')
        else:
            self.app_handle.set_conf_val('missing.overridephone', '0')

    @property
    def missingname(self):
        return self.app_handle.get_conf_val('missing.missingname')

    @missingname.setter
    def missingname(self, new_val):
        self.app_handle.set_conf_val('missing.missingname', new_val)

    @property
    def missingphone(self):
        return self.app_handle.get_conf_val('missing.missingphone')

    @missingphone.setter
    def missingphone(self, new_val):
        self.app_handle.set_conf_val('missing.missingphone', new_val)

    def get_default_phone_number(self):
        return self.app_handle.GetPhoneNumber(self.missingname)

    @property
    def member_csv_location(self):
        return self.app_handle.get_conf_val('file.member_csv_location')

    @member_csv_location.setter
    def member_csv_location(self, new_val):
        self.app_handle.set_conf_val('file.member_csv_location', new_val)

    @property
    def nonmember_csv_location(self):
        return self.app_handle.get_conf_val('file.nonmember_csv_location')

    @nonmember_csv_location.setter
    def nonmember_csv_location(self, new_val):
        self.app_handle.set_conf_val('file.nonmember_csv_location', new_val)

    @property
    def imagesdirectory(self):
        return self.app_handle.get_conf_val('file.imagesdirectory')

    @imagesdirectory.setter
    def imagesdirectory(self, new_val):
        self.app_handle.set_conf_val('file.imagesdirectory', new_val)

    @property
    def pdf_outdirectory(self):
        return self.app_handle.get_conf_val('file.pdf_outdirectory')

    @pdf_outdirectory.setter
    def pdf_outdirectory(self, new_val):
        self.app_handle.set_conf_val('file.pdf_outdirectory', new_val)

    @property
    def imagearchivedir(self):
        return self.app_handle.get_conf_val('file.imagearchivedir')

    @imagearchivedir.setter
    def imagearchivedir(self, new_val):
        self.app_handle.set_conf_val('file.imagearchivedir', new_val)
