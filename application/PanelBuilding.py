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
		self.CB_SacramentDisp = wx.CheckBox(self, -1)
		if int(self.parent.GetConfigValue('block.displaysac')):
			self.CB_SacramentDisp.SetValue(True)
		ScheduleGrid.Add(self.CB_SacramentDisp, (1,0), span = wx.DefaultSpan,
						 flag = wx.ALIGN_CENTER | wx.ALL, border = 10)

		self.SacText = wx.StaticText(self, -1, "Sacrament Meeting (Start Time)")
		self.SacText.SetFont(self.StandardFont)
		if int(self.parent.GetConfigValue('block.displaysac')):
			self.SacText.Enable(True)
		else:
			self.SacText.Enable(False)
		ScheduleGrid.Add(self.SacText, (1,1), span = wx.DefaultSpan, flag = wx.ALL, border = 10)

		self.SacTime = wx.lib.masked.TimeCtrl(self, -1, display_seconds = False)
		self.SacTime.SetFont(self.StandardFont)
		if not self.parent.GetConfigValue('block.sacstart') == None:
			self.SacTime.SetValue(self.parent.GetConfigValue('block.sacstart'))
		h = self.SacTime.GetSize().height
		self.spin1 = wx.SpinButton( self, -1, wx.DefaultPosition, (-1,h), wx.SP_VERTICAL)
		self.SacTime.BindSpinButton(self.spin1)
		if int(self.parent.GetConfigValue('block.displaysac')):
			self.SacTime.Enable(True)
			self.spin1.Enable(True)
		else:
			self.SacTime.Enable(False)
			self.spin1.Enable(False)
		ScheduleGrid.Add(self.SacTime, (1,2), span = wx.DefaultSpan, flag = wx.ALIGN_RIGHT | wx.TOP | wx.LEFT | wx.BOTTOM, border = 10)
		ScheduleGrid.Add(self.spin1, (1,3), span = wx.DefaultSpan, flag = wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.BOTTOM, border = 10)

		#Sunday School Row
		self.CB_SundaySchoolDisp = wx.CheckBox(self, -1)
		if int(self.parent.GetConfigValue('block.displayss')):
			self.CB_SundaySchoolDisp.SetValue(True)
		else:
			self.CB_SundaySchoolDisp.SetValue(False)
		ScheduleGrid.Add(self.CB_SundaySchoolDisp, (2,0), span = wx.DefaultSpan, flag = wx.ALIGN_CENTER | wx.ALL, border = 10)

		self.SSText = wx.StaticText(self, -1, "SundaySchool (Start Time)")
		self.SSText.SetFont(self.StandardFont)
		if int(self.parent.GetConfigValue('block.displayss')):
			self.SSText.Enable(True)
		else:
			self.SSText.Enable(False)
		ScheduleGrid.Add(self.SSText, (2,1), span = wx.DefaultSpan, flag = wx.ALL, border = 10)

		self.SSTime = wx.lib.masked.TimeCtrl(self, -1, display_seconds = False)
		self.SSTime.SetFont(self.StandardFont)
		if not self.parent.GetConfigValue('block.ssstart') == None:
			self.SSTime.SetValue(self.parent.GetConfigValue('block.ssstart'))
		h = self.SSTime.GetSize().height
		self.spin2 = wx.SpinButton( self, -1, wx.DefaultPosition, (-1,h), wx.SP_VERTICAL)
		self.SSTime.BindSpinButton(self.spin2)
		if int(self.parent.GetConfigValue('block.displayss')):
			self.SSTime.Enable(True)
			self.spin2.Enable(True)
		else:
			self.SSTime.Enable(False)
			self.SSTime.Enable(False)
		ScheduleGrid.Add(self.SSTime, (2,2), span = wx.DefaultSpan, flag = wx.ALIGN_RIGHT | wx.TOP | wx.LEFT | wx.BOTTOM, border = 10)
		ScheduleGrid.Add(self.spin2, (2,3), span = wx.DefaultSpan, flag = wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.BOTTOM, border = 10)

		#Priesthood/Relief Society Row
		self.CB_PriesthoodDisp = wx.CheckBox(self, -1)
		if int(self.parent.GetConfigValue('block.display_pr_rs')):
			self.CB_PriesthoodDisp.SetValue(True)
		else:
			self.CB_PriesthoodDisp.SetValue(False)
		ScheduleGrid.Add(self.CB_PriesthoodDisp, (3,0), span = wx.DefaultSpan, flag = wx.ALIGN_CENTER | wx.ALL, border = 10)

		self.PriesthoodText = wx.StaticText(self, -1, "Priesthood/Relief Society (Start Time)")
		self.PriesthoodText.SetFont(self.StandardFont)
		if int(self.parent.GetConfigValue('block.display_pr_rs')):
			self.PriesthoodText.Enable(True)
		else:
			self.PriesthoodText.Enable(False)
		ScheduleGrid.Add(self.PriesthoodText, (3,1), span = wx.DefaultSpan, flag = wx.ALL, border = 10)

		self.PriesthoodTime = wx.lib.masked.TimeCtrl(self, -1, display_seconds = False)
		self.PriesthoodTime.SetFont(self.StandardFont)
		if not self.parent.GetConfigValue('block.pr_rs_start') == None:
			self.PriesthoodTime.SetValue(self.parent.GetConfigValue('block.pr_rs_start'))
		h = self.PriesthoodTime.GetSize().height
		self.spin3 = wx.SpinButton( self, -1, wx.DefaultPosition, (-1,h), wx.SP_VERTICAL)
		self.PriesthoodTime.BindSpinButton(self.spin3)
		if int(self.parent.GetConfigValue('block.display_pr_rs')):
			self.PriesthoodTime.Enable(True)
			self.spin3.Enable(True)
		else:
			self.PriesthoodTime.Enable(False)
			self.spin3.Enable(False)
		ScheduleGrid.Add(self.PriesthoodTime, (3,2), span = wx.DefaultSpan, flag = wx.ALIGN_RIGHT | wx.TOP | wx.LEFT | wx.BOTTOM, border = 10)
		ScheduleGrid.Add(self.spin3, (3,3), span = wx.DefaultSpan, flag = wx.ALIGN_LEFT | wx.TOP | wx.RIGHT | wx.BOTTOM, border = 10)

		ScheduleBoxSizer.Add(ScheduleGrid, 0, wx.ALL | 10)

		############################################################################
		## Building Contact Information
		BuildingBox = wx.StaticBox(self, -1, "Building Information")
		BuildingBox.SetFont(self.StandardFont)
		self.BuildingBoxSizer = BuildingBoxSizer = wx.StaticBoxSizer(BuildingBox, wx.VERTICAL)

		AddressStatic = wx.StaticText(self, -1, "Building Address")
		AddressStatic.SetFont(self.StandardFont)
		BuildingBoxSizer.Add(AddressStatic, 1, wx.ALL, 10)

		self.Addy1 = wx.TextCtrl(self, -1, size = (300,-1))
		self.Addy1.SetFont(self.StandardFont)
		if not self.parent.GetConfigValue('bldg.addy1') == None:
			self.Addy1.SetValue(self.parent.GetConfigValue('bldg.addy1'))
		BuildingBoxSizer.Add(self.Addy1, 0, wx.ALL, 10)

		self.Addy2 = wx.TextCtrl(self, -1, size = (300, -1))
		self.Addy2.SetFont(self.StandardFont)
		if not self.parent.GetConfigValue('bldg.addy2') == None:
			self.Addy2.SetValue(self.parent.GetConfigValue('bldg.addy2'))
		BuildingBoxSizer.Add(self.Addy2, 0, wx.ALL, 10)

		PhoneStatic = wx.StaticText(self, -1, "Building Phone #")
		PhoneStatic.SetFont(self.StandardFont)
		BuildingBoxSizer.Add(PhoneStatic, 0, wx.ALL, 10)

		self.Phone = wx.TextCtrl(self, -1, size = (200, -1))
		self.Phone.SetFont(self.StandardFont)
		if not self.parent.GetConfigValue('bldg.phone') == None:
			self.Phone.SetValue(self.parent.GetConfigValue('bldg.phone'))
		BuildingBoxSizer.Add(self.Phone, 0, wx.ALL, 10)

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
		bottom_level2.Add(logo, 0, wx.ALL, 10)
		bottom_level2.Add(BuildingBoxSizer, 3, wx.EXPAND | wx.ALL, 25)

		inside_border_level1 = wx.BoxSizer(wx.VERTICAL)
		inside_border_level1.Add(top_level2, 0, wx.BOTTOM | wx.ALIGN_CENTER, 5)
		inside_border_level1.Add(bottom_level2, 0, wx.TOP | wx.ALIGN_CENTER, 5)

		border_level0 = wx.BoxSizer()
		border_level0.Add(inside_border_level1, 1, wx.EXPAND | wx.ALL, 25)
		self.SetSizer(border_level0)
		border_level0.SetDimension(0, 0, self.GetSize()[0], self.GetSize()[1])

		self.Bind(wx.EVT_CHECKBOX, self.OnSacDisp, self.CB_SacramentDisp)
		self.Bind(wx.EVT_CHECKBOX, self.OnSSDisp, self.CB_SundaySchoolDisp)
		self.Bind(wx.EVT_CHECKBOX, self.OnPrDisp, self.CB_PriesthoodDisp)
		self.Bind(wx.lib.masked.EVT_TIMEUPDATE, self.OnSacTimeChange, self.SacTime)
		self.Bind(wx.lib.masked.EVT_TIMEUPDATE, self.OnSSTimeChange, self.SSTime)
		self.Bind(wx.lib.masked.EVT_TIMEUPDATE, self.OnPrTimeChange, self.PriesthoodTime)
		self.Bind(wx.EVT_TEXT, self.OnAddy1Changed, self.Addy1)
		self.Bind(wx.EVT_TEXT, self.OnAddy2Changed, self.Addy2)
		self.Bind(wx.EVT_TEXT, self.OnPhoneChanged, self.Phone)

		self.Title = "Building"

	def OnSacDisp(self, evt):
		if evt.Checked():
			self.parent.SetConfigValue('block.displaysac', '1')
			self.SacText.Enable(True)
			self.SacTime.Enable(True)
			self.spin1.Enable(True)
		else:
			self.parent.SetConfigValue('block.displaysac', '0')
			self.SacText.Enable(False)
			self.SacTime.Enable(False)
			self.spin1.Enable(False)

	def OnSSDisp(self, evt):
		if evt.Checked():
			self.parent.SetConfigValue('block.displayss', '1')
			self.SSText.Enable(True)
			self.SSTime.Enable(True)
			self.spin2.Enable(True)
		else:
			self.parent.SetConfigValue('block.displayss', '0')
			self.SSText.Enable(False)
			self.SSTime.Enable(False)
			self.spin2.Enable(False)

	def OnPrDisp(self, evt):
		if evt.Checked():
			self.parent.SetConfigValue('block.display_pr_rs', '1')
			self.PriesthoodText.Enable(True)
			self.PriesthoodTime.Enable(True)
			self.spin3.Enable(True)
		else:
			self.parent.SetConfigValue('block.display_pr_rs', '0')
			self.PriesthoodText.Enable(False)
			self.PriesthoodTime.Enable(False)
			self.spin3.Enable(False)

	def OnSacTimeChange(self, evt):
		self.parent.SetConfigValue('block.sacstart', evt.GetValue())

	def OnSSTimeChange(self, evt):
		self.parent.SetConfigValue('block.ssstart', evt.GetValue())

	def OnPrTimeChange(self, evt):
		self.parent.SetConfigValue('block.pr_rs_start', evt.GetValue())

	def OnAddy1Changed(self, evt):
		self.parent.SetConfigValue('bldg.addy1', evt.GetString())

	def OnAddy2Changed(self, evt):
		self.parent.SetConfigValue('bldg.addy2', evt.GetString())

	def OnPhoneChanged(self, evt):
		self.parent.SetConfigValue('bldg.phone', evt.GetString())

	def makingActive(self):
		return
