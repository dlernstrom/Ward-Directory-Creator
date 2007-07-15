#PanelMain.py
import wx
from ColoredPanel import *
import  wx.lib.filebrowsebutton as filebrowse

class MainPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, wx.BLUE)

		#########################################################################
		## Ward/Branch Configuration Section
		WardBox = wx.StaticBox(self, -1, "Ward/Branch Configuration")
		WardBox.SetFont(self.StandardFont)
		self.WardBoxSizer = WardBoxSizer = wx.StaticBoxSizer(WardBox, wx.VERTICAL)

		StaticWardName = wx.StaticText(self, -1, "Unit Name:")
		StaticWardName.SetFont(self.StandardFont)
		WardBoxSizer.Add(StaticWardName, 0, wx.TOP | wx.LEFT, 10)

		TXT_WardName = wx.TextCtrl(self, -1, size=(250,25))
		TXT_WardName.SetFont(self.TextBoxFont)
		if self.parent.GetConfigValue('unit.unitname'):
			TXT_WardName.SetValue(self.parent.GetConfigValue('unit.unitname'))
		WardBoxSizer.Add(TXT_WardName, 0, wx.TOP | wx.LEFT, 10)

		self.RB_Ward = wx.RadioButton(self, -1, "Ward", style = wx.RB_GROUP)
		self.RB_Ward.SetFont(self.StandardFont)
		if self.parent.GetConfigValue('unit.unit_type') == 'Ward':
			self.RB_Ward.SetValue(True)
		WardBoxSizer.Add(self.RB_Ward, 0, wx.TOP | wx.LEFT, 10)

		self.RB_Branch = wx.RadioButton(self, -1, "Branch")
		self.RB_Branch.SetFont(self.StandardFont)
		if self.parent.GetConfigValue('unit.unit_type') == 'Branch':
			self.RB_Branch.SetValue(True)
		WardBoxSizer.Add(self.RB_Branch, 0, wx.TOP | wx.LEFT, 10)

		StaticStakeName = wx.StaticText(self, -1, "Stake Name:")
		StaticStakeName.SetFont(self.StandardFont)
		WardBoxSizer.Add(StaticStakeName, 0, wx.TOP | wx.LEFT, 10)

		TXT_StakeName = wx.TextCtrl(self, -1, size=(250,25))
		TXT_StakeName.SetFont(self.TextBoxFont)
		if self.parent.GetConfigValue('unit.stakename'):
			TXT_StakeName.SetValue(self.parent.GetConfigValue('unit.stakename'))
		WardBoxSizer.Add(TXT_StakeName, 0, wx.TOP | wx.LEFT, 10)

		############################################################################
		## Quote Configuration Section
		QuoteBox = wx.StaticBox(self, -1, "Quote Configuration")
		QuoteBox.SetFont(self.StandardFont)
		self.QuoteBoxSizer = QuoteBoxSizer = wx.StaticBoxSizer(QuoteBox, wx.VERTICAL)

		self.CB_UseQuote = wx.CheckBox(self, -1, "Use Quote")
		self.CB_UseQuote.SetFont(self.StandardFont)
		if int(self.parent.GetConfigValue('quote.usequote')):
			self.CB_UseQuote.SetValue(True)
		QuoteBoxSizer.Add(self.CB_UseQuote, 0, wx.TOP | wx.LEFT, 10)

		self.StaticInspQuote = wx.StaticText(self, -1, "Inspirational Quote:")
		self.StaticInspQuote.SetFont(self.StandardFont)
		if int(self.parent.GetConfigValue('quote.usequote')):
			self.StaticInspQuote.Enable(True)
		else:
			self.StaticInspQuote.Enable(False)
		QuoteBoxSizer.Add(self.StaticInspQuote, 0, wx.TOP | wx.LEFT, 10)

		self.TXT_Quote = wx.TextCtrl(self, -1, size = (350, 100), style = wx.PROCESS_ENTER | wx.TE_MULTILINE )
		self.TXT_Quote.SetFont(self.TextBoxFont)
		if int(self.parent.GetConfigValue('quote.usequote')):
			self.TXT_Quote.Enable(True)
		else:
			self.TXT_Quote.Enable(False)
		if not self.parent.GetConfigValue('quote.quotecontent') == None:
			self.TXT_Quote.SetValue(self.parent.GetConfigValue('quote.quotecontent'))
		QuoteBoxSizer.Add(self.TXT_Quote, 0, wx.TOP | wx.LEFT, 10)

		self.StaticAuthor = wx.StaticText(self, -1, "Author:")
		self.StaticAuthor.SetFont(self.StandardFont)
		if int(self.parent.GetConfigValue('quote.usequote')):
			self.StaticAuthor.Enable(True)
		else:
			self.StaticAuthor.Enable(False)
		QuoteBoxSizer.Add(self.StaticAuthor, 0, wx.TOP | wx.LEFT, 10)

		self.TXT_Author = wx.TextCtrl(self, -1, size=(250,25))
		self.TXT_Author.SetFont(self.TextBoxFont)
		if int(self.parent.GetConfigValue('quote.usequote')):
			self.TXT_Author.Enable(True)
		else:
			self.TXT_Author.Enable(False)
		if not self.parent.GetConfigValue('quote.quoteauthor') == None:
			self.TXT_Author.SetValue(self.parent.GetConfigValue('quote.quoteauthor'))
		QuoteBoxSizer.Add(self.TXT_Author, 0, wx.TOP | wx.LEFT, 10)

		self.BTN_RestoreQuote = wx.Button(self, -1, "Restore Default")
		self.BTN_RestoreQuote.SetFont(self.StandardFont)
		if int(self.parent.GetConfigValue('quote.usequote')):
			self.BTN_RestoreQuote.Enable(True)
		else:
			self.BTN_RestoreQuote.Enable(False)
		QuoteBoxSizer.Add(self.BTN_RestoreQuote, 0, wx.TOP | wx.LEFT, 10)

		#######################################################################
		## Non wrapped items
		StaticHeading = wx.StaticText(self,
									  -1,
									  "Ward Directory Creator " + parent.parent.MajorAppVersion,
									  style = wx.ALIGN_CENTRE)
		StaticHeading.SetFont(self.TitleFont)

		logo = wx.StaticBitmap(self, -1, self.logo_bmp, (self.logo_bmp.GetWidth(), self.logo_bmp.GetHeight()))

		#######################################################################
		## Sizer encapsulation section
		left_level3 = wx.BoxSizer(wx.VERTICAL)
		left_level3.Add(self.WardBoxSizer, 6, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, 25)
		left_level3.Add(logo, 3, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, 25)

		right_level3 = wx.BoxSizer()
		right_level3.Add(self.QuoteBoxSizer, 5, wx.EXPAND | wx.ALL, 25)

		top_level2 = wx.BoxSizer(wx.HORIZONTAL)
		top_level2.Add(StaticHeading, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)

		bottom_level2 = wx.BoxSizer(wx.HORIZONTAL)
		bottom_level2.Add(left_level3, 2, wx.EXPAND)
		bottom_level2.Add(right_level3, 3, wx.EXPAND)
		#bottom_level2.Hide(left_level3)

		inside_border_level1 = wx.BoxSizer(wx.VERTICAL)
		inside_border_level1.Add(top_level2, 0, wx.EXPAND | wx.ALL, 25)
		inside_border_level1.Add(bottom_level2, 1, wx.EXPAND)

		border_level0 = wx.BoxSizer()
		border_level0.Add(inside_border_level1, 1, wx.EXPAND | wx.ALL, 25)
		self.SetSizer(border_level0)
		border_level0.SetDimension(0, 0, self.GetSize()[0], self.GetSize()[1])

		self.Bind(wx.EVT_TEXT, self.OnWardChanged, TXT_WardName)
		self.Bind(wx.EVT_RADIOBUTTON, self.OnWardTypeChanged)
		self.Bind(wx.EVT_TEXT, self.OnStakeChanged, TXT_StakeName)
		self.Bind(wx.EVT_CHECKBOX, self.OnUseQuote, self.CB_UseQuote)
		self.Bind(wx.EVT_TEXT, self.OnQuoteChanged, self.TXT_Quote)
		self.Bind(wx.EVT_TEXT, self.OnAuthorChanged, self.TXT_Author)
		self.Bind(wx.EVT_BUTTON, self.OnRestoreQuote, self.BTN_RestoreQuote)

		self.Title = "Main"

	def OnWardChanged(self, evt):
		self.parent.SetConfigValue('unit.unitname', evt.GetString())

	def OnWardTypeChanged(self, evt):
		if evt.GetId() == self.RB_Ward.GetId():
			self.parent.SetConfigValue('unit.unit_type', 'Ward')
		else:
			self.parent.SetConfigValue('unit.unit_type', 'Branch')

	def OnStakeChanged(self, evt):
		self.parent.SetConfigValue('unit.stakename', evt.GetString())

	def OnUseQuote(self, evt):
		if evt.Checked():
			self.parent.SetConfigValue('quote.usequote', 1)
			self.StaticInspQuote.Enable(True)
			self.TXT_Quote.Enable(True)
			self.StaticAuthor.Enable(True)
			self.TXT_Author.Enable(True)
			self.BTN_RestoreQuote.Enable(True)
		else:
			self.parent.SetConfigValue('quote.usequote', 0)
			self.StaticInspQuote.Enable(False)
			self.TXT_Quote.Enable(False)
			self.StaticAuthor.Enable(False)
			self.TXT_Author.Enable(False)
			self.BTN_RestoreQuote.Enable(False)

	def OnQuoteChanged(self, evt):
		self.parent.SetConfigValue('quote.quotecontent', evt.GetString())

	def OnAuthorChanged(self, evt):
		self.parent.SetConfigValue('quote.quoteauthor', evt.GetString())

	def OnRestoreQuote(self, evt):
		self.TXT_Quote.SetValue(self.parent.AppHandle.ConfigDefaults['quote.quotecontent'])
		self.TXT_Author.SetValue(self.parent.AppHandle.ConfigDefaults['quote.quoteauthor'])

	def makingActive(self):
		return
