#PanelLeadership.py

import wx
from ColoredPanel import *
import  wx.lib.filebrowsebutton as filebrowse

HoH = 1
Parent = 2
All = 4

class LeadershipRow(wx.BoxSizer):
	def __init__(self, parent, Description, NameType = HoH):
		wx.BoxSizer.__init__(self, wx.HORIZONTAL)
		self.parent = parent

		DescriptionText = wx.StaticText(parent, -1, Description)
		DescriptionText.SetFont(parent.StandardFont)
		self.Add(DescriptionText, 1, wx.ALIGN_CENTER_VERTICAL)

		NameList = self.parent.parent.parent.AppHandle.GetNameList()
		Contact_Dropdown = wx.ComboBox(parent, -1, choices = NameList)
		Contact_Dropdown.SetFont(parent.TextBoxFont)
		self.Add(Contact_Dropdown, 0, wx.TOP | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)

		TXT_Phone = wx.TextCtrl(parent, -1, size = (150, -1))
		TXT_Phone.SetFont(parent.TextBoxFont)
		self.Add(TXT_Phone, 0, wx.TOP | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)

		CB_Override = wx.CheckBox(parent, -1, "Override")
		CB_Override.SetFont(parent.TextBoxFont)
		self.Add(CB_Override, 0, wx.TOP | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)

		CB_Disp = wx.CheckBox(parent, -1, "Display")
		CB_Disp.SetFont(parent.TextBoxFont)
		self.Add(CB_Disp, 0, wx.TOP | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 10)

class LeadershipPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, None)
		self.parent = parent

		############################################################################
		## Leadership Name Configuration
		self.Bishop = LeadershipRow(self, "Bishop", HoH)
		self.First = LeadershipRow(self, "1st Counselor", HoH)
		self.Second = LeadershipRow(self, "2nd Counselor", HoH)
		self.WardClerk = LeadershipRow(self, "Ward Clerk", HoH)
		self.Financial = LeadershipRow(self, "Financial Clerk", HoH)
		self.Membership = LeadershipRow(self, "Membership Clerk", HoH)
		self.EQ = LeadershipRow(self, "Elders Quorum", HoH)
		self.HP = LeadershipRow(self, "High Priests", HoH)
		self.RS = LeadershipRow(self, "Relief Society", HoH)
		self.YM = LeadershipRow(self, "Young Mens", HoH)
		self.YW = LeadershipRow(self, "Young Womens", HoH)
		self.Primary = LeadershipRow(self, "Primary", HoH)
		self.WM = LeadershipRow(self, "Ward Mission Leader", HoH)
		self.Act = LeadershipRow(self, "Activities Committee", HoH)
		self.Newsletter = LeadershipRow(self, "Ward Newsletter", HoH)
		self.Directory = LeadershipRow(self, "Ward Directory", HoH)

		#######################################################################
		## Non wrapped items
		#logo = wx.StaticBitmap(self, -1, self.logo_bmp, (self.logo_bmp.GetWidth(), self.logo_bmp.GetHeight()))

		#######################################################################
		## Sizer encapsulation section

		inside_border_level1 = wx.BoxSizer(wx.VERTICAL)
		inside_border_level1.Add(self.Bishop, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)
		inside_border_level1.Add(self.First, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)
		inside_border_level1.Add(self.Second, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)
		inside_border_level1.Add(self.WardClerk, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)
		inside_border_level1.Add(self.Financial, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)
		inside_border_level1.Add(self.Membership, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)
		inside_border_level1.Add(self.EQ, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)
		inside_border_level1.Add(self.HP, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)
		inside_border_level1.Add(self.RS, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)
		inside_border_level1.Add(self.YM, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)
		inside_border_level1.Add(self.YW, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)
		inside_border_level1.Add(self.Primary, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)
		inside_border_level1.Add(self.WM, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)
		inside_border_level1.Add(self.Act, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)
		inside_border_level1.Add(self.Newsletter, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)
		inside_border_level1.Add(self.Directory, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 2)

		border_level0 = wx.BoxSizer()
		border_level0.Add(inside_border_level1, 1, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 25)
		self.SetSizer(border_level0)
		border_level0.SetDimension(0, 0, self.GetSize()[0], self.GetSize()[1])

		self.Title = "Leadership"

	def makingActive(self):
		return

