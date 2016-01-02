# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wx

from ColoredPanel import ColoredPanel


class LeadershipRow(wx.BoxSizer):
    def __init__(self, parent, Description, ShortDesc, NameType='HoH'):
        super(LeadershipRow, self).__init__(wx.HORIZONTAL)
        self.parent = parent
        self.Description = Description
        self.ShortDesc = ShortDesc
        self.NameType = NameType

        self.DescriptionText = wx.StaticText(parent, -1, Description)
        self.DescriptionText.SetFont(parent.TextBoxFont)
        self.Add(self.DescriptionText, 1, wx.ALIGN_CENTER_VERTICAL)

        self.Contact_Dropdown = wx.ComboBox(parent, -1, size=(265, -1),
                                            style=wx.CB_READONLY)
        self.Contact_Dropdown.SetFont(parent.TextBoxFont)
        self.Add(self.Contact_Dropdown, 0,
                 wx.TOP | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)

        self.TXT_Phone = wx.TextCtrl(parent, -1, size=(150, -1))
        self.TXT_Phone.SetFont(parent.TextBoxFont)
        self.Add(self.TXT_Phone, 0,
                 wx.TOP | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)

        self.CB_Override = wx.CheckBox(parent, -1, "Override")
        self.CB_Override.SetFont(parent.TextBoxFont)
        self.Add(self.CB_Override, 0,
                 wx.TOP | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)

        self.CB_Disp = wx.CheckBox(parent, -1, "Display")
        self.CB_Disp.SetFont(parent.TextBoxFont)
        self.Add(self.CB_Disp, 0,
                 wx.TOP | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)


class LeadershipPanel(ColoredPanel):
    def __init__(self, parent, app_handle):
        super(LeadershipPanel, self).__init__(parent, None, app_handle)
        #######################################################################
        ## Leadership Name Configuration
        self.Bishop = LeadershipRow(self, "Bishop",
                                    ShortDesc='bish')
        self.First = LeadershipRow(self, "1st Counselor",
                                   ShortDesc='first')
        self.Second = LeadershipRow(self, "2nd Counselor",
                                    ShortDesc='second')
        self.Exec = LeadershipRow(self, "Executive Secretary",
                                  ShortDesc='exec')
        self.WardClerk = LeadershipRow(self, "Ward Clerk",
                                       ShortDesc='clerk')
        self.Financial = LeadershipRow(self, "Financial Clerk",
                                       ShortDesc='fin')
        self.Membership = LeadershipRow(self, "Membership Clerk",
                                        ShortDesc='mem')
        self.EQ = LeadershipRow(self, "Elders Quorum",
                                ShortDesc='eq')
        self.HP = LeadershipRow(self, "High Priests",
                                ShortDesc='hp')
        self.RS = LeadershipRow(self, "Relief Society",
                                ShortDesc='rs', NameType='Parent')
        self.YM = LeadershipRow(self, "Young Mens",
                                ShortDesc='ym')
        self.YW = LeadershipRow(self, "Young Womens",
                                ShortDesc='yw', NameType='Parent')
        self.Primary = LeadershipRow(self, "Primary",
                                     ShortDesc='primary',
                                     NameType='Parent')
        self.WM = LeadershipRow(self, "Ward Mission Leader",
                                ShortDesc='wml')
        self.SS = LeadershipRow(self, "Sunday School President",
                                ShortDesc='ss')
        self.Newsletter = LeadershipRow(self, "Ward Newsletter",
                                        ShortDesc='news',
                                        NameType='Parent')

        self.PageRows = [self.Bishop, self.First, self.Second, self.Exec,
                         self.WardClerk, self.Financial, self.Membership,
                         self.EQ, self.HP, self.RS, self.YM, self.YW,
                         self.Primary, self.WM, self.SS, self.Newsletter]

        #######################################################################
        ## Sizer encapsulation section
        inside_border_level1 = wx.BoxSizer(wx.VERTICAL)
        for Row in self.PageRows:
            inside_border_level1.Add(Row, 0, wx.ALIGN_RIGHT)

        border_level0 = wx.BoxSizer()
        border_level0.Add(inside_border_level1, 1,
                          wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 15)
        self.SetSizer(border_level0)
        border_level0.SetDimension(0, 0, self.GetSize()[0], self.GetSize()[1])

        self.Bind(wx.EVT_TEXT, self.OnChange)
        self.Bind(wx.EVT_CHECKBOX, self.OnChange)

        self.Title = "Leadership"

    def OnChange(self, evt):
        for Row in self.PageRows:
            if Row.Contact_Dropdown.GetId() == evt.GetId():
                self.DropdownChange(Row, evt.GetString())
                return
            elif Row.CB_Override.GetId() == evt.GetId():
                self.OverrideChange(Row, evt.Checked())
                return
            elif Row.TXT_Phone.GetId() == evt.GetId():
                self.PhoneNumberChange(Row, evt.GetString())
                return
            elif Row.CB_Disp.GetId() == evt.GetId():
                self.DispChange(Row, evt.Checked())
                return
        raise Exception('problem')

    def DropdownChange(self, Row, NewValue):
        #Save the new value
        setattr(self.app_handle, 'leadership_' + Row.ShortDesc + 'name',
                NewValue)
        #Uncheck the override box
        Row.CB_Override.SetValue(False)
        #Save the override box status
        setattr(self.app_handle, 'leadership_' + Row.ShortDesc + 'overph', '0')
        #Enable(True) the override box
        Row.CB_Override.Enable(True)
        #Load the phone number from CSV
        phone = self.app_handle.GetPhoneNumber(NewValue)
        Row.TXT_Phone.SetValue(phone)
        #Check the display box
        Row.CB_Disp.SetValue(True)
        #Save the CB_Disp value
        setattr(self.app_handle, 'leadership_' + Row.ShortDesc + 'disp', '1')
        #Enable(True) the display box
        Row.CB_Disp.Enable(True)

    def OverrideChange(self, Row, Checked):
        if Checked:
            # save the new value
            setattr(self.app_handle, 'leadership_' + Row.ShortDesc + 'overph',
                    '1')
            # Enable the phone field
            Row.TXT_Phone.Enable(True)
        else:
            # save the new value
            setattr(self.app_handle, 'leadership_' + Row.ShortDesc + 'overph',
                    '0')
            # Disable the phone field
            Row.TXT_Phone.Enable(False)
            # Reset the values for the phone field to CSV like
            phone = self.app_handle.GetPhoneNumber(
                getattr(self.app_handle,
                        'leadership_' + Row.ShortDesc + 'name'))
            Row.TXT_Phone.SetValue(phone)

    def PhoneNumberChange(self, Row, NewNumber):
        setattr(self.app_handle, 'leadership_' + Row.ShortDesc + 'phone',
                NewNumber)

    def DispChange(self, Row, NewStatus):
        if NewStatus:
            setattr(self.app_handle, 'leadership_' + Row.ShortDesc + 'disp',
                    '1')
        else:
            setattr(self.app_handle, 'leadership_' + Row.ShortDesc + 'disp',
                    '0')

    def making_active(self):
        if not self.app_handle.isValidCSV():
            self.disable_all()
            return

        name_type = None
        # optimized for repeat searches
        for page_row in self.PageRows:
            # Setup the dropdown lists
            if page_row.NameType != name_type:
                name_type = page_row.NameType
                name_list = self.app_handle.GetNameList(name_type)
            page_row.Contact_Dropdown.Clear()
            for Name in name_list:
                page_row.Contact_Dropdown.Append(Name)
            # Enable things
            page_row.DescriptionText.Enable(True)
            page_row.Contact_Dropdown.Enable(True)
            # What else can I enable?
            leader_name = getattr(self.app_handle,
                                  'leadership_' + page_row.ShortDesc + 'name')
            if leader_name in name_list:
                # The name is in the list, I may as well set the data
                page_row.Contact_Dropdown.SetStringSelection(
                    leader_name)
                leader_disp = getattr(
                    self.app_handle,
                    'leadership_' + page_row.ShortDesc + 'disp')
                if leader_disp == '1':
                    page_row.CB_Disp.SetValue(True)
                else:
                    page_row.CB_Disp.SetValue(False)
                page_row.CB_Override.Enable(True)
                leader_over_phone = getattr(
                    self.app_handle,
                    'leadership_' + page_row.ShortDesc + 'overph')
                if leader_over_phone == '1':
                    page_row.CB_Override.SetValue(True)
                    page_row.TXT_Phone.Enable(True)
                    leader_phone = getattr(
                        self.app_handle,
                        'leadership_' + page_row.ShortDesc + 'phone')
                    page_row.TXT_Phone.SetValue(leader_phone)
                else:
                    page_row.CB_Override.SetValue(False)
                    page_row.TXT_Phone.Enable(False)
                    phone = self.app_handle.GetPhoneNumber(
                        leader_name)
                    page_row.TXT_Phone.SetValue(phone)
                page_row.CB_Disp.Enable(True)
            else:
                if leader_name:
                    # Name not in list
                    nm = leader_name
                    print nm + " Not in list"
                    setattr(self.app_handle,
                            'leadership_' + page_row.ShortDesc + 'disp', '0')
                page_row.TXT_Phone.Enable(False)
                page_row.CB_Override.Enable(False)
                page_row.CB_Override.SetValue(False)
                page_row.CB_Disp.Enable(False)
                page_row.CB_Disp.SetValue(False)

    def disable_all(self):
        for row in self.PageRows:
            row.Contact_Dropdown.Enable(False)
            row.DescriptionText.Enable(False)
            row.TXT_Phone.Enable(False)
            row.CB_Override.Enable(False)
            row.CB_Disp.Enable(False)
