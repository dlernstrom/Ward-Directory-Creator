# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class MainControl(object):
    def __init__(self, app_handle, presentation, interaction):
        self.app_handle = app_handle
        self.presentation = presentation
        interaction.install(self, presentation)

    def making_active(self):
        # Here's the logic to set up the prevalues from config file
        if self.app_handle.get_conf_val('unit.unitname'):
            self.presentation.TXT_WardName.SetValue(
                self.app_handle.get_conf_val('unit.unitname'))
        if self.app_handle.get_conf_val('unit.unit_type') == 'Ward':
            self.presentation.RB_Ward.SetValue(True)
        elif self.app_handle.get_conf_val('unit.unit_type') == 'Branch':
            self.presentation.RB_Branch.SetValue(True)
        if self.app_handle.get_conf_val('unit.stakename'):
            self.presentation.TXT_StakeName.SetValue(
                self.app_handle.get_conf_val('unit.stakename'))
        if int(self.app_handle.get_conf_val('quote.usequote')):
            self.presentation.CB_UseQuote.SetValue(True)
        if int(self.app_handle.get_conf_val('quote.usequote')):
            self.presentation.StaticInspQuote.Enable(True)
        else:
            self.presentation.StaticInspQuote.Enable(False)
        if int(self.app_handle.get_conf_val('quote.usequote')):
            self.presentation.TXT_Quote.Enable(True)
        else:
            self.presentation.TXT_Quote.Enable(False)
        if not self.app_handle.get_conf_val('quote.quotecontent') == None:
            self.presentation.TXT_Quote.SetValue(
                self.app_handle.get_conf_val('quote.quotecontent'))
        if int(self.app_handle.get_conf_val('quote.usequote')):
            self.presentation.StaticAuthor.Enable(True)
        else:
            self.presentation.StaticAuthor.Enable(False)
        if int(self.app_handle.get_conf_val('quote.usequote')):
            self.presentation.TXT_Author.Enable(True)
        else:
            self.presentation.TXT_Author.Enable(False)
        if not self.app_handle.get_conf_val('quote.quoteauthor') == None:
            self.presentation.TXT_Author.SetValue(
                self.app_handle.get_conf_val('quote.quoteauthor'))
        if int(self.app_handle.get_conf_val('quote.usequote')):
            self.presentation.BTN_RestoreQuote.Enable(True)
        else:
            self.presentation.BTN_RestoreQuote.Enable(False)

    def display_about_dialog(self):
        self.presentation.display_about_box()

    def update_ward_name(self, new_val):
        self.app_handle.set_conf_val('unit.unitname', new_val)

    def update_unit_type(self, new_val):
        self.app_handle.set_conf_val('unit.unit_type', new_val)

    def update_stake_name(self, new_val):
        self.app_handle.set_conf_val('unit.stakename', new_val)

    def allow_use_quote(self, allow):
        if allow:
            self.app_handle.set_conf_val('quote.usequote', 1)
            self.presentation.StaticInspQuote.Enable(True)
            self.presentation.TXT_Quote.Enable(True)
            self.presentation.StaticAuthor.Enable(True)
            self.presentation.TXT_Author.Enable(True)
            self.presentation.BTN_RestoreQuote.Enable(True)
        else:
            self.app_handle.set_conf_val('quote.usequote', 0)
            self.presentation.StaticInspQuote.Enable(False)
            self.presentation.TXT_Quote.Enable(False)
            self.presentation.StaticAuthor.Enable(False)
            self.presentation.TXT_Author.Enable(False)
            self.presentation.BTN_RestoreQuote.Enable(False)

    def update_quote(self, new_val):
        self.app_handle.set_conf_val('quote.quotecontent', new_val)

    def update_author(self, new_val):
        self.app_handle.set_conf_val('quote.quoteauthor', new_val)

    def reset_quote(self):
        self.presentation.TXT_Quote.SetValue(
            self.app_handle.ConfigDefaults['quote.quotecontent'])
        self.presentation.TXT_Author.SetValue(
            self.app_handle.ConfigDefaults['quote.quoteauthor'])
