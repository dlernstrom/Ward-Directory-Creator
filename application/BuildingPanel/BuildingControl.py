# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx
from wx.lib.masked import TimeCtrl

from application.ColoredPanel import ColoredPanel


class BuildingControl(ColoredPanel):
    def __init__(self, app_handle, presentation, interaction):
        self.app_handle = app_handle
        self.presentation = presentation
        interaction.install(self, presentation)

    def making_active(self):
        # Here's the logic to set up the prevalues from config file
        if int(self.app_handle.get_conf_val('block.displaysac')):
            self.presentation.CB_SacramentDisp.SetValue(True)
        if int(self.app_handle.get_conf_val('block.displaysac')):
            self.presentation.SacText.Enable(True)
        else:
            self.presentation.SacText.Enable(False)
        if not self.app_handle.get_conf_val('block.sacstart') == None:
            self.presentation.SacTime.SetValue(
                self.app_handle.get_conf_val('block.sacstart'))
        if int(self.app_handle.get_conf_val('block.displaysac')):
            self.presentation.SacTime.Enable(True)
            self.presentation.spin1.Enable(True)
        else:
            self.presentation.SacTime.Enable(False)
            self.presentation.spin1.Enable(False)
        if int(self.app_handle.get_conf_val('block.displayss')):
            self.presentation.CB_SundaySchoolDisp.SetValue(True)
        else:
            self.presentation.CB_SundaySchoolDisp.SetValue(False)
        if int(self.app_handle.get_conf_val('block.displayss')):
            self.presentation.SSText.Enable(True)
        else:
            self.presentation.SSText.Enable(False)
        if not self.app_handle.get_conf_val('block.ssstart') == None:
            self.presentation.SSTime.SetValue(
                self.app_handle.get_conf_val('block.ssstart'))
        if int(self.app_handle.get_conf_val('block.displayss')):
            self.presentation.SSTime.Enable(True)
            self.presentation.spin2.Enable(True)
        else:
            self.presentation.SSTime.Enable(False)
            self.presentation.SSTime.Enable(False)
        if int(self.app_handle.get_conf_val('block.display_pr_rs')):
            self.presentation.CB_PriesthoodDisp.SetValue(True)
        else:
            self.presentation.CB_PriesthoodDisp.SetValue(False)
        if int(self.app_handle.get_conf_val('block.display_pr_rs')):
            self.presentation.PriesthoodText.Enable(True)
        else:
            self.presentation.PriesthoodText.Enable(False)
        if not self.app_handle.get_conf_val('block.pr_rs_start') == None:
            self.presentation.PriesthoodTime.SetValue(
                self.app_handle.get_conf_val('block.pr_rs_start'))
        if int(self.app_handle.get_conf_val('block.display_pr_rs')):
            self.presentation.PriesthoodTime.Enable(True)
            self.presentation.spin3.Enable(True)
        else:
            self.presentation.PriesthoodTime.Enable(False)
            self.presentation.spin3.Enable(False)

        if not self.app_handle.get_conf_val('bldg.addy1') == None:
            self.presentation.Addy1.SetValue(
                self.app_handle.get_conf_val('bldg.addy1'))
        if not self.app_handle.get_conf_val('bldg.addy2') == None:
            self.presentation.Addy2.SetValue(
                self.app_handle.get_conf_val('bldg.addy2'))
        if not self.app_handle.get_conf_val('bldg.phone') == None:
            self.presentation.Phone.SetValue(
                self.app_handle.get_conf_val('bldg.phone'))

    def show_sac_start_time(self, enable=True):
        if enable:
            self.app_handle.set_conf_val('block.displaysac', '1')
        else:
            self.app_handle.set_conf_val('block.displaysac', '0')
        self.presentation.SacText.Enable(enable)
        self.presentation.SacTime.Enable(enable)
        self.presentation.spin1.Enable(enable)

    def show_ss_start_time(self, enable=True):
        if enable:
            self.app_handle.set_conf_val('block.displayss', '1')
        else:
            self.app_handle.set_conf_val('block.displayss', '0')
        self.presentation.SSText.Enable(enable)
        self.presentation.SSTime.Enable(enable)
        self.presentation.spin2.Enable(enable)

    def show_pr_start_time(self, enable=True):
        if enable:
            self.app_handle.set_conf_val('block.display_pr_rs', '1')
        else:
            self.app_handle.set_conf_val('block.display_pr_rs', '0')

    def update_sac_time(self, new_val):
        self.app_handle.set_conf_val('block.sacstart', new_val)

    def update_ss_time(self, new_val):
        self.app_handle.set_conf_val('block.ssstart', new_val)

    def update_pr_time(self, new_val):
        self.app_handle.set_conf_val('block.pr_rs_start', new_val)
