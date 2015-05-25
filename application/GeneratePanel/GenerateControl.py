# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class GenerateControl(object):
    def __init__(self, app_handle, presentation, interaction):
        self.app_handle = app_handle
        self.presentation = presentation
        interaction.install(self, presentation)

    def making_active(self):
        # Here's the logic to set up the prevalues from config file
        if self.app_handle.get_conf_val('email.smtp'):
            self.presentation.smtp_addy = \
                self.app_handle.get_conf_val('email.smtp')
        if self.app_handle.get_conf_val('email.username'):
            self.presentation.smtp_user = \
                self.app_handle.get_conf_val('email.username')
        if self.app_handle.get_conf_val('email.pass'):
            self.presentation.smtp_pass = \
                self.app_handle.get_conf_val('email.pass')
        if self.app_handle.get_conf_val('task.missreport') == '1':
            self.presentation.gen_missing_rpt = True
        if self.app_handle.get_conf_val('task.missimages') == '1':
            self.presentation.gen_missing_img_rpt = True
        if self.app_handle.get_conf_val('task.sendemail') == '1':
            self.presentation.send_email = True
        if self.app_handle.get_conf_val('task.genmissfile') == '1':
            self.presentation.gen_missing_img_file = True
        if self.app_handle.get_conf_val('task.extract_moveouts') == '1':
            self.presentation.extract_move_outs = True
        if self.app_handle.get_conf_val('task.genfull') == '1':
            self.presentation.gen_pdf_full = True
        if self.app_handle.get_conf_val('task.genbooklet') == '1':
            self.presentation.gen_pdf_booklet = True
        if self.app_handle.get_conf_val('task.gensingle2double') == '1':
            self.presentation.gen_pdf_single2double = True

    def set_smtp(self, new_val):
        self.app_handle.set_conf_val('email.smtp', new_val)

    def set_smtp_user(self, new_val):
        self.app_handle.set_conf_val('email.username', new_val)

    def set_smtp_pass(self, new_val):
        self.app_handle.set_conf_val('email.pass', new_val)

    def set_miss_report(self, new_val):
        self.app_handle.set_conf_val('task.missreport', new_val)

    def set_miss_images(self, new_val):
        self.app_handle.set_conf_val('task.missimages', new_val)

    def set_send_email(self, new_val):
        self.app_handle.set_conf_val('task.sendemail', new_val)

    def set_gen_miss_file(self, new_val):
        self.app_handle.set_conf_val('task.genmissfile', new_val)

    def set_extract_move_outs(self, new_val):
        self.app_handle.set_conf_val('task.extract_moveouts', new_val)

    def set_gen_full(self, new_val):
        self.app_handle.set_conf_val('task.genfull', new_val)

    def set_gen_booklet(self, new_val):
        self.app_handle.set_conf_val('task.genbooklet', new_val)

    def set_gen_single2double(self, new_val):
        self.app_handle.set_conf_val('task.gensingle2double', new_val)

    def go(self):
        # Here, I need to check each of the (7) things to do and do them
        if self.app_handle.get_conf_val('task.sendemail') == '1':
            print "Sending Emails"
            self.app_handle.SendEmails()
        if self.app_handle.get_conf_val('task.genmissfile') == '1':
            print "Generating Missing File"
        if self.app_handle.get_conf_val('task.extract_moveouts') == '1':
            print "Extracting Move-Outs"
            LiveFolder = self.app_handle.get_conf_val('file.imagesdirectory')
            ArchiveFolder = self.app_handle.get_conf_val('file.imagearchivedir')
            self.app_handle.MoveSuperflousImages(LiveFolder, ArchiveFolder)

        # Generate PDF Stuff Here
        Full = 0
        if self.app_handle.get_conf_val('task.genfull') == '1':
            print "Generating Full PDF"
            Full = 1

        Single2Double = 0
        if self.app_handle.get_conf_val('task.gensingle2double') == '1':
            print "Generating Single2Double PDF"
            Single2Double = 1

        Booklet = 0
        if self.app_handle.get_conf_val('task.genbooklet') == '1':
            print "Generating Booklet PDF"
            Booklet = 1
        if Full or Booklet or Single2Double:
            OutputFolder = self.app_handle.get_conf_val('file.pdf_outdirectory')
            dict_data = None
            self.app_handle.InitiatePDF(OutputFolder, Full, Booklet,
                                        Single2Double)

        # Generate Missing Image Report
        if self.app_handle.get_conf_val('task.missreport') == '1':
            print "Generating missing report"
            LiveFolder = self.app_handle.get_conf_val('file.imagesdirectory')
            msg = self.app_handle.GetReportMsg()
            self.presentation.show_report(msg)
        if self.app_handle.get_conf_val('task.missimages') == '1':
            print "Generating missing images report"
            LiveFolder = self.app_handle.get_conf_val('file.imagesdirectory')
            msg = self.app_handle.GetImagesReportMsg()
            self.presentation.show_report(msg)
