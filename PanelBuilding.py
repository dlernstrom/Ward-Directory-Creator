#PanelBuilding.py

import wx
import wx.lib
import wx.lib.masked
from ColoredPanel import *
import  wx.lib.filebrowsebutton as filebrowse

class BuildingPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, wx.BLUE)

		self.parent = parent

		############################################################################
		## Block Schedule Configuration
		ScheduleBox = wx.StaticBox(self, -1, "Block Schedule")
		ScheduleBox.SetFont(self.StandardFont)
		self.ScheduleBoxSizer = ScheduleBoxSizer = wx.StaticBoxSizer(ScheduleBox, wx.VERTICAL)

		#I need a flex grid sizer in the ScheduleBoxSizer
		ScheduleGrid = wx.GridBagSizer()

		DisplayWord = wx.StaticText(self, -1, "Display")
		DisplayWord.SetFont(self.StandardFont)
		ScheduleGrid.Add(DisplayWord, (0,0), span = wx.DefaultSpan, flag = wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border = 10)

		#Sacrament Meeting Row
		CB_SacramentDisp = wx.CheckBox(self, -1)
		ScheduleGrid.Add(CB_SacramentDisp, (1,0), span = wx.DefaultSpan, flag = wx.ALIGN_CENTER | wx.ALL, border = 10)

		SacText = wx.StaticText(self, -1, "Sacrament Meeting (Start Time)")
		SacText.SetFont(self.StandardFont)
		ScheduleGrid.Add(SacText, (1,1), span = wx.DefaultSpan, flag = wx.ALL, border = 10)

		self.SacTime = wx.lib.masked.TimeCtrl(self, -1, display_seconds = False)
		self.SacTime.SetFont(self.StandardFont)
		h = self.SacTime.GetSize().height
		spin1 = wx.SpinButton( self, -1, wx.DefaultPosition, (-1,h), wx.SP_VERTICAL)
		self.SacTime.BindSpinButton(spin1)
		ScheduleGrid.Add(self.SacTime, (1,2), span = wx.DefaultSpan, flag = wx.ALIGN_RIGHT | wx.TOP | wx.LEFT | wx.BOTTOM, border = 10)
		ScheduleGrid.Add(spin1, (1,3), span = wx.DefaultSpan, flag = wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.BOTTOM, border = 10)

		#Sunday School Row
		CB_SundaySchoolDisp = wx.CheckBox(self, -1)
		ScheduleGrid.Add(CB_SundaySchoolDisp, (2,0), span = wx.DefaultSpan, flag = wx.ALIGN_CENTER | wx.ALL, border = 10)

		SSText = wx.StaticText(self, -1, "SundaySchool (Start Time)")
		SSText.SetFont(self.StandardFont)
		ScheduleGrid.Add(SSText, (2,1), span = wx.DefaultSpan, flag = wx.ALL, border = 10)

		self.SSTime = wx.lib.masked.TimeCtrl(self, -1, display_seconds = False)
		self.SSTime.SetFont(self.StandardFont)
		h = self.SSTime.GetSize().height
		spin2 = wx.SpinButton( self, -1, wx.DefaultPosition, (-1,h), wx.SP_VERTICAL)
		self.SSTime.BindSpinButton(spin2)
		ScheduleGrid.Add(self.SSTime, (2,2), span = wx.DefaultSpan, flag = wx.ALIGN_RIGHT | wx.TOP | wx.LEFT | wx.BOTTOM, border = 10)
		ScheduleGrid.Add(spin2, (2,3), span = wx.DefaultSpan, flag = wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.BOTTOM, border = 10)

		#Priesthood/Relief Society Row
		CB_PriesthoodDisp = wx.CheckBox(self, -1)
		ScheduleGrid.Add(CB_PriesthoodDisp, (3,0), span = wx.DefaultSpan, flag = wx.ALIGN_CENTER | wx.ALL, border = 10)

		PriesthoodText = wx.StaticText(self, -1, "Priesthood/Relief Society (Start Time)")
		PriesthoodText.SetFont(self.StandardFont)
		ScheduleGrid.Add(PriesthoodText, (3,1), span = wx.DefaultSpan, flag = wx.ALL, border = 10)

		self.PriesthoodTime = wx.lib.masked.TimeCtrl(self, -1, display_seconds = False)
		self.PriesthoodTime.SetFont(self.StandardFont)
		h = self.PriesthoodTime.GetSize().height
		spin3 = wx.SpinButton( self, -1, wx.DefaultPosition, (-1,h), wx.SP_VERTICAL)
		self.PriesthoodTime.BindSpinButton(spin3)
		ScheduleGrid.Add(self.PriesthoodTime, (3,2), span = wx.DefaultSpan, flag = wx.ALIGN_RIGHT | wx.TOP | wx.LEFT | wx.BOTTOM, border = 10)
		ScheduleGrid.Add(spin3, (3,3), span = wx.DefaultSpan, flag = wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.BOTTOM, border = 10)

		ScheduleBoxSizer.Add(ScheduleGrid, 0, wx.ALL | 10)

		############################################################################
		## Building Contact Information
		BuildingBox = wx.StaticBox(self, -1, "Building Information")
		BuildingBox.SetFont(self.StandardFont)
		self.BuildingBoxSizer = BuildingBoxSizer = wx.StaticBoxSizer(BuildingBox, wx.VERTICAL)

		AddressStatic = wx.StaticText(self, -1, "Building Address")
		AddressStatic.SetFont(self.StandardFont)
		BuildingBoxSizer.Add(AddressStatic, 1, wx.ALL, 10)

		Addy1 = wx.TextCtrl(self, -1, size = (300,-1))
		Addy1.SetFont(self.StandardFont)
		BuildingBoxSizer.Add(Addy1, 0, wx.ALL, 10)

		Addy2 = wx.TextCtrl(self, -1, size = (300, -1))
		Addy2.SetFont(self.StandardFont)
		BuildingBoxSizer.Add(Addy2, 0, wx.ALL, 10)

		PhoneStatic = wx.StaticText(self, -1, "Building Phone #")
		PhoneStatic.SetFont(self.StandardFont)
		BuildingBoxSizer.Add(PhoneStatic, 0, wx.ALL, 10)

		Phone = wx.TextCtrl(self, -1, size = (200, -1))
		Phone.SetFont(self.StandardFont)
		BuildingBoxSizer.Add(Phone, 0, wx.ALL, 10)

		#######################################################################
		## Non wrapped items
		logo = wx.StaticBitmap(self, -1, self.logo_bmp, (self.logo_bmp.GetWidth(), self.logo_bmp.GetHeight()))

		#######################################################################
		## Sizer encapsulation section
		top_level2 = wx.BoxSizer(wx.HORIZONTAL)
		top_level2.AddStretchSpacer()
		top_level2.Add(ScheduleBoxSizer, 0)
		top_level2.AddStretchSpacer()

		bottom_level2 = wx.BoxSizer(wx.HORIZONTAL)
		bottom_level2.Add(logo, 2, wx.EXPAND)
		bottom_level2.Add(BuildingBoxSizer, 3, wx.EXPAND | wx.ALL, 25)

		inside_border_level1 = wx.BoxSizer(wx.VERTICAL)
		inside_border_level1.Add(top_level2, 0, wx.BOTTOM | wx.ALIGN_CENTER, 5)
		inside_border_level1.Add(bottom_level2, 0, wx.TOP | wx.ALIGN_CENTER, 5)

		border_level0 = wx.BoxSizer()
		border_level0.Add(inside_border_level1, 1, wx.EXPAND | wx.ALL, 25)
		self.SetSizer(border_level0)
		border_level0.SetDimension(0, 0, self.GetSize()[0], self.GetSize()[1])

		self.Title = "Building"
