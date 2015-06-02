# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class BuildingAbstraction(object):
    def __init__(self, app_handle):
        self.app_handle = app_handle

    @property
    def displaysac(self):
        return int(self.app_handle.get_conf_val('block.displaysac'))

    @displaysac.setter
    def displaysac(self, new_val):
        if new_val:
            self.app_handle.set_conf_val('block.displaysac', '1')
        else:
            self.app_handle.set_conf_val('block.displaysac', '0')

    @property
    def sacstart(self):
        return self.app_handle.get_conf_val('block.sacstart')

    @sacstart.setter
    def sacstart(self, new_val):
        self.app_handle.set_conf_val('block.sacstart', new_val)

    @property
    def displayss(self):
        return int(self.app_handle.get_conf_val('block.displayss'))

    @displayss.setter
    def displayss(self, new_val):
        if new_val:
            self.app_handle.set_conf_val('block.displayss', '1')
        else:
            self.app_handle.set_conf_val('block.displayss', '0')

    @property
    def ssstart(self):
        return self.app_handle.get_conf_val('block.ssstart')

    @ssstart.setter
    def ssstart(self, new_val):
        self.app_handle.set_conf_val('block.ssstart', new_val)

    @property
    def display_pr_rs(self):
        return int(self.app_handle.get_conf_val('block.display_pr_rs'))

    @display_pr_rs.setter
    def display_pr_rs(self, new_val):
        if new_val:
            self.app_handle.set_conf_val('block.display_pr_rs', '1')
        else:
            self.app_handle.set_conf_val('block.display_pr_rs', '0')

    @property
    def pr_rs_start(self):
        return self.app_handle.get_conf_val('block.pr_rs_start')

    @pr_rs_start.setter
    def pr_rs_start(self, new_val):
        self.app_handle.set_conf_val('block.pr_rs_start', new_val)

    @property
    def addy1(self):
        return self.app_handle.get_conf_val('bldg.addy1')

    @addy1.setter
    def addy1(self, new_val):
        self.app_handle.set_conf_val('bldg.addy1', new_val)

    @property
    def addy2(self):
        return self.app_handle.get_conf_val('bldg.addy2')

    @addy2.setter
    def addy2(self, new_val):
        self.app_handle.set_conf_val('bldg.addy2', new_val)

    @property
    def phone(self):
        return self.app_handle.get_conf_val('bldg.phone')

    @phone.setter
    def phone(self, new_val):
        self.app_handle.set_conf_val('bldg.phone', new_val)
