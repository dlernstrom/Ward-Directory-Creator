# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx
from wx.lib.wordwrap import wordwrap

from application.ColoredPanel import ColoredPanel
from __version__ import __version__


BLOB = """The Ward Directory Creator application was
    designed to simplify the process of creating folded directories for Wards
    and Branches of the Church of Jesus Christ of Latter Day Saints. This
    application is neither created, nor endorsed by the church.\n\n
    The Ward Directory Creator uses the comma seperated values (csv) file,
    available on your ward's website, for its membership data. This eliminates
    the need to maintain two seperate databases of your ward members, providing
    a more accurate directory listing. For best results, download a new copy of
    the csv file each time you generate a directory.
    """
LICENSE_TEXT = """By using this application, you agree not to reverse engineer,
modify, pirate, disassemble, or otherwise use the application in ways not
intended by the author(s)."""


class MainPresentation(ColoredPanel):
    def __init__(self, parent):
        super(MainPresentation, self).__init__(parent, None)
        #######################################################################
        ## Ward/Branch Configuration Section
        ward_box = wx.StaticBox(self, -1, "Ward/Branch Configuration")
        ward_box.SetFont(self.StandardFont)
        ward_box_sizer = wx.StaticBoxSizer(ward_box, wx.VERTICAL)

        static_ward_name = wx.StaticText(self, -1, "Unit Name:")
        static_ward_name.SetFont(self.StandardFont)
        ward_box_sizer.Add(static_ward_name, 0, wx.TOP | wx.LEFT, 10)

        self.TXT_WardName = wx.TextCtrl(self, -1, size=(250, 25))
        self.TXT_WardName.SetFont(self.TextBoxFont)
        ward_box_sizer.Add(self.TXT_WardName, 0, wx.TOP | wx.LEFT, 10)

        self.RB_Ward = wx.RadioButton(self, -1, "Ward", style=wx.RB_GROUP)
        self.RB_Ward.SetFont(self.StandardFont)
        ward_box_sizer.Add(self.RB_Ward, 0, wx.TOP | wx.LEFT, 10)

        self.RB_Branch = wx.RadioButton(self, -1, "Branch")
        self.RB_Branch.SetFont(self.StandardFont)
        ward_box_sizer.Add(self.RB_Branch, 0, wx.TOP | wx.LEFT, 10)

        static_stake_name = wx.StaticText(self, -1, "Stake Name:")
        static_stake_name.SetFont(self.StandardFont)
        ward_box_sizer.Add(static_stake_name, 0, wx.TOP | wx.LEFT, 10)

        self.TXT_StakeName = wx.TextCtrl(self, -1, size=(250, 25))
        self.TXT_StakeName.SetFont(self.TextBoxFont)
        ward_box_sizer.Add(self.TXT_StakeName, 0, wx.TOP | wx.LEFT, 10)

        #######################################################################
        ## Quote Configuration Section
        quote_box = wx.StaticBox(self, -1, "Quote Configuration")
        quote_box.SetFont(self.StandardFont)
        quote_box_sizer = wx.StaticBoxSizer(quote_box, wx.VERTICAL)

        self.CB_UseQuote = wx.CheckBox(self, -1, "Use Quote")
        self.CB_UseQuote.SetFont(self.StandardFont)
        quote_box_sizer.Add(self.CB_UseQuote, 0, wx.TOP | wx.LEFT, 10)

        self.StaticInspQuote = wx.StaticText(self, -1, "Inspirational Quote:")
        self.StaticInspQuote.SetFont(self.StandardFont)
        quote_box_sizer.Add(self.StaticInspQuote, 0, wx.TOP | wx.LEFT, 10)

        self.TXT_Quote = wx.TextCtrl(self, -1, size=(350, 100),
                                     style=wx.PROCESS_ENTER | wx.TE_MULTILINE)
        self.TXT_Quote.SetFont(self.TextBoxFont)
        quote_box_sizer.Add(self.TXT_Quote, 0, wx.TOP | wx.LEFT, 10)

        self.StaticAuthor = wx.StaticText(self, -1, "Author:")
        self.StaticAuthor.SetFont(self.StandardFont)
        quote_box_sizer.Add(self.StaticAuthor, 0, wx.TOP | wx.LEFT, 10)

        self.TXT_Author = wx.TextCtrl(self, -1, size=(250, 25))
        self.TXT_Author.SetFont(self.TextBoxFont)
        quote_box_sizer.Add(self.TXT_Author, 0, wx.TOP | wx.LEFT, 10)

        self.BTN_RestoreQuote = wx.Button(self, -1, "Restore Default")
        self.BTN_RestoreQuote.SetFont(self.StandardFont)
        quote_box_sizer.Add(self.BTN_RestoreQuote, 0, wx.TOP | wx.LEFT, 10)

        #######################################################################
        ## Non wrapped items
        static_heading = wx.StaticText(self, -1, "Ward Directory Creator",
                                       style=wx.ALIGN_CENTRE)
        static_heading.SetFont(self.TitleFont)

        logo = wx.StaticBitmap(self, -1, self.logo_bmp,
                               (self.logo_bmp.GetWidth(),
                                self.logo_bmp.GetHeight()))

        self.AboutBoxButton = wx.Button(self, -1, "About WDC")
        self.AboutBoxButton.SetFont(self.StandardFont)

        #######################################################################
        ## Sizer encapsulation section
        left_level3 = wx.BoxSizer(wx.VERTICAL)
        left_level3.Add(ward_box_sizer, 6,
                        wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, 25)
        left_level3.Add(logo, 0, wx.TOP | wx.BOTTOM | wx.LEFT, 25)

        right_level3 = wx.BoxSizer(wx.VERTICAL)
        right_level3.Add(quote_box_sizer, 5, wx.EXPAND | wx.ALL, 25)
        right_level3.Add(self.AboutBoxButton, 1, wx.ALL | wx.ALIGN_CENTRE, 25)

        top_level2 = wx.BoxSizer(wx.HORIZONTAL)
        top_level2.Add(static_heading, 1,
                       wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)

        bottom_level2 = wx.BoxSizer(wx.HORIZONTAL)
        bottom_level2.Add(left_level3, 2, wx.EXPAND)
        bottom_level2.Add(right_level3, 3, wx.EXPAND)

        inside_border_level1 = wx.BoxSizer(wx.VERTICAL)
        inside_border_level1.Add(top_level2, 0, wx.EXPAND | wx.ALL, 25)
        inside_border_level1.Add(bottom_level2, 1, wx.EXPAND)

        border_level0 = wx.BoxSizer()
        border_level0.Add(inside_border_level1, 1, wx.EXPAND | wx.ALL, 25)
        self.SetSizer(border_level0)
        border_level0.SetDimension(0, 0, self.GetSize()[0], self.GetSize()[1])

    def display_about_box(self):
        info = wx.AboutDialogInfo()
        info.Name = "Ward Directory Creator"
        info.Version = __version__
        info.Copyright = "(C) 2007-2015 David Ernstrom"
        info.Description = wordwrap(BLOB, 350, wx.ClientDC(self))
        info.WebSite = ("http://directory.ernstrom.net",
                        "Ward Directory Creator")
        info.Developers = ["David Ernstrom", "Tina Ernstrom"]
        info.License = wordwrap(LICENSE_TEXT, 500, wx.ClientDC(self))
        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)
