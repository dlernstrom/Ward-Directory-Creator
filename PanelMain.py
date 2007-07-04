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

		StaticWardName = wx.StaticText(self, -1, "Ward Name:")
		StaticWardName.SetFont(self.StandardFont)
		WardBoxSizer.Add(StaticWardName, 0, wx.TOP | wx.LEFT, 10)

		TXT_WardName = wx.TextCtrl(self, -1, size=(250,25))
		TXT_WardName.SetFont(self.TextBoxFont)
		WardBoxSizer.Add(TXT_WardName, 0, wx.TOP | wx.LEFT, 10)

		RB_Ward = wx.RadioButton(self, -1, "Ward", style = wx.RB_GROUP)
		RB_Ward.SetFont(self.StandardFont)
		WardBoxSizer.Add(RB_Ward, 0, wx.TOP | wx.LEFT, 10)

		RB_Branch = wx.RadioButton(self, -1, "Branch")
		RB_Branch.SetFont(self.StandardFont)
		WardBoxSizer.Add(RB_Branch, 0, wx.TOP | wx.LEFT, 10)

		StaticStakeName = wx.StaticText(self, -1, "Stake Name:")
		StaticStakeName.SetFont(self.StandardFont)
		WardBoxSizer.Add(StaticStakeName, 0, wx.TOP | wx.LEFT, 10)

		TXT_StakeName = wx.TextCtrl(self, -1, size=(250,25))
		TXT_StakeName.SetFont(self.TextBoxFont)
		WardBoxSizer.Add(TXT_StakeName, 0, wx.TOP | wx.LEFT, 10)

		############################################################################
		## Quote Configuration Section
		QuoteBox = wx.StaticBox(self, -1, "Quote Configuration")
		QuoteBox.SetFont(self.StandardFont)
		self.QuoteBoxSizer = QuoteBoxSizer = wx.StaticBoxSizer(QuoteBox, wx.VERTICAL)

		CB_UseQuote = wx.CheckBox(self, -1, "Use Quote")
		CB_UseQuote.SetFont(self.StandardFont)
		QuoteBoxSizer.Add(CB_UseQuote, 0, wx.TOP | wx.LEFT, 10)

		StaticInspQuote = wx.StaticText(self, -1, "Inspirational Quote:")
		StaticInspQuote.SetFont(self.StandardFont)
		StaticInspQuote.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		QuoteBoxSizer.Add(StaticInspQuote, 0, wx.TOP | wx.LEFT, 10)

		TXT_Quote = wx.TextCtrl(self, -1, size = (350, 100))
		TXT_Quote.SetFont(self.TextBoxFont)
		QuoteBoxSizer.Add(TXT_Quote, 0, wx.TOP | wx.LEFT, 10)

		StaticAuthor = wx.StaticText(self, -1, "Author:")
		StaticAuthor.SetFont(self.StandardFont)
		QuoteBoxSizer.Add(StaticAuthor, 0, wx.TOP | wx.LEFT, 10)

		TXT_Author = wx.TextCtrl(self, -1, size=(250,25))
		TXT_Author.SetFont(self.TextBoxFont)
		QuoteBoxSizer.Add(TXT_Author, 0, wx.TOP | wx.LEFT, 10)

		BTN_RestoreQuote = wx.Button(self, -1, "Restore Default")
		BTN_RestoreQuote.SetFont(self.StandardFont)
		QuoteBoxSizer.Add(BTN_RestoreQuote, 0, wx.TOP | wx.LEFT, 10)

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
		print "Level 0 - position:",border_level0.GetPosition()
		print "Level 0 - size:",border_level0.GetSize()

		print "Level 1 - Inner Border position:", inside_border_level1.GetPosition()
		print "Level 1 - Inner Border size:", inside_border_level1.GetSize()

		print "Level 2 - Top Title position:", top_level2.GetPosition()
		print "Level 2 - Top Title size:", top_level2.GetSize()

		print "Level 2 - Bottom Content position:", bottom_level2.GetPosition()
		print "Level 2 - Bottom Content size:", bottom_level2.GetSize()

		print "Level 3 - Static Title position:", StaticHeading.GetPosition()
		print "Level 3 - Static Title size:", StaticHeading.GetSize()

		print "Level 3 - Left Content position:", left_level3.GetPosition()
		print "Level 3 - Left Content size:", left_level3.GetSize()

		print "Level 3 - Right Content position:", right_level3.GetPosition()
		print "Level 3 - Right Content size:", right_level3.GetSize()

		print "Level 4 - Ward/Branch position:", self.WardBoxSizer.GetPosition()
		print "Level 4 - Ward/Branch size:", self.WardBoxSizer.GetSize()

		print "Level 4 - LOGO position:", logo.GetPosition()
		print "Level 4 - LOGO size:", logo.GetSize()

		print "Level 4 - Quote position:", self.QuoteBoxSizer.GetPosition()
		print "Level 4 - Quote size:", self.QuoteBoxSizer.GetSize()

		self.Title = "Main"
