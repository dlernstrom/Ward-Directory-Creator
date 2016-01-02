# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from application.ColoredPanel import ColoredPanel


class BuildingControl(ColoredPanel):
    def __init__(self, abstraction, presentation, interaction):
        self.abstraction = abstraction
        self.presentation = presentation
        interaction.install(self, presentation)

    def making_active(self):
        # Here's the logic to set up the prevalues from config file
        if self.abstraction.displaysac:
            self.presentation.sac_display_checkbox = True
            self.presentation.SacText.Enable(True)
            self.presentation.SacTime.Enable(True)
            self.presentation.spin1.Enable(True)
        else:
            self.presentation.SacText.Enable(False)
            self.presentation.SacTime.Enable(False)
            self.presentation.spin1.Enable(False)
        if self.abstraction.sacstart != None:
            self.presentation.SacTime.SetValue(self.abstraction.sacstart)
        if self.abstraction.displayss:
            self.presentation.CB_SundaySchoolDisp.SetValue(True)
            self.presentation.SSText.Enable(True)
            self.presentation.SSTime.Enable(True)
            self.presentation.spin2.Enable(True)
        else:
            self.presentation.CB_SundaySchoolDisp.SetValue(False)
            self.presentation.SSText.Enable(False)
            self.presentation.SSTime.Enable(False)
            self.presentation.spin2.Enable(False)
        if self.abstraction.ssstart != None:
            self.presentation.SSTime.SetValue(self.abstraction.ssstart)
        if self.abstraction.display_pr_rs:
            self.presentation.CB_PriesthoodDisp.SetValue(True)
            self.presentation.PriesthoodText.Enable(True)
            self.presentation.PriesthoodTime.Enable(True)
            self.presentation.spin3.Enable(True)
        else:
            self.presentation.CB_PriesthoodDisp.SetValue(False)
            self.presentation.PriesthoodText.Enable(False)
            self.presentation.PriesthoodTime.Enable(False)
            self.presentation.spin3.Enable(False)
        if self.abstraction.pr_rs_start != None:
            self.presentation.PriesthoodTime.SetValue(
                self.abstraction.pr_rs_start)
        if self.abstraction.addy1 != None:
            self.presentation.Addy1.SetValue(self.abstraction.addy1)
        if self.abstraction.addy2 != None:
            self.presentation.Addy2.SetValue(self.abstraction.addy2)
        if self.abstraction.phone != None:
            self.presentation.Phone.SetValue(self.abstraction.phone)

    def show_sac_start_time(self, enable=True):
        self.abstraction.displaysac = enable
        self.presentation.SacText.Enable(enable)
        self.presentation.SacTime.Enable(enable)
        self.presentation.spin1.Enable(enable)

    def show_ss_start_time(self, enable=True):
        self.abstraction.displayss = enable
        self.presentation.SSText.Enable(enable)
        self.presentation.SSTime.Enable(enable)
        self.presentation.spin2.Enable(enable)

    def show_pr_start_time(self, enable=True):
        self.abstraction.display_pr_rs = enable

    def update_sac_time(self, new_val):
        self.abstraction.sacstart = new_val

    def update_ss_time(self, new_val):
        self.abstraction.ssstart = new_val

    def update_pr_time(self, new_val):
        self.abstraction.pr_rs_start = new_val

    def update_building_address_line_1(self, new_val):
        self.abstraction.addy1 = new_val

    def update_building_address_line_2(self, new_val):
        self.abstraction.addy2 = new_val

    def update_building_phone(self, new_val):
        self.abstraction.phone = new_val
