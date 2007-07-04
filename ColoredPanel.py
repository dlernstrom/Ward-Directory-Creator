import wx
import images

class ColoredPanel(wx.Window):
	def __init__(self, parent, color):
		self.id = wx.NewId()
		wx.Window.__init__(self, parent, self.id, style = wx.SIMPLE_BORDER)
		#if not color == None:
		#	self.SetBackgroundColour(color)

		# Just for style points, we'll use this as a background image.
		self.bg_bmp = images.getNotebookBKGDBitmap()
		self.SetSize((self.bg_bmp.GetWidth(), self.bg_bmp.GetHeight()))

		# This could also be done by getting the window's default font;
		# either way, we need to have a font loaded for later on.
		#self.SetBackgroundColour("WHITE")
		#self.font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)

		# Create drawing area and set its font
		#dc = wx.ClientDC(self)
		#dc.SetFont(self.font)

		self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
	#	self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
		#print "ColoredPanel:",self.GetSize()
		self.TitleFont = wx.Font(22, wx.DEFAULT, wx.NORMAL, wx.FONTWEIGHT_BOLD, False, "Georgia")
		self.StandardFont = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Georgia")

		WardBox = wx.StaticBox(self, -1, "Ward/Branch Configuration")
		WardBox.SetFont(self.StandardFont)
		self.WardBoxSizer = WardBoxSizer = wx.StaticBoxSizer(WardBox, wx.VERTICAL)

		StaticWardName = wx.StaticText(self, -1, "Ward Name:")
		StaticWardName.SetFont(self.StandardFont)
		#gbs.Add(StaticWardName,
		#		pos = (2,0), span = (1,1), flag = wx.ALIGN_LEFT)
		WardBoxSizer.Add(StaticWardName, 0, wx.TOP | wx.LEFT, 10)

		TXT_WardName = wx.TextCtrl(self, -1, size=(250,35))
		TXT_WardName.SetFont(self.StandardFont)
		#gbs.Add(TXT_WardName,
		#		pos = (2,1), span = (1,2), flag = wx.ALIGN_LEFT)
		WardBoxSizer.Add(TXT_WardName, 0, wx.TOP | wx.LEFT, 10)

		RB_Ward = wx.RadioButton(self, -1, "Ward", style = wx.RB_GROUP)
		RB_Ward.SetFont(self.StandardFont)
		#gbs.Add(RB_Ward,
		#		pos = (3,0), span = wx.DefaultSpan, flag = wx.ALIGN_CENTER_HORIZONTAL)
		WardBoxSizer.Add(RB_Ward, 0, wx.TOP | wx.LEFT, 10)

		RB_Branch = wx.RadioButton(self, -1, "Branch")
		RB_Branch.SetFont(self.StandardFont)
		#gbs.Add(RB_Branch,
		#		pos = (3,1), span = wx.DefaultSpan, flag = wx.ALIGN_LEFT)
		WardBoxSizer.Add(RB_Branch, 0, wx.TOP | wx.LEFT, 10)

		StaticStakeName = wx.StaticText(self, -1, "Stake Name:")
		StaticStakeName.SetFont(self.StandardFont)
		#gbs.Add(StaticStakeName,
		#		pos = (4,0), span = (1,1), flag = wx.ALIGN_LEFT)
		WardBoxSizer.Add(StaticStakeName, 0, wx.TOP | wx.LEFT, 10)

		TXT_StakeName = wx.TextCtrl(self, -1, size=(250,35))
		TXT_StakeName.SetFont(self.StandardFont)
		#gbs.Add(TXT_StakeName,
		#		pos = (4,1), span = (1,2), flag = wx.ALIGN_LEFT)
		WardBoxSizer.Add(TXT_StakeName, 0, wx.TOP | wx.LEFT, 10)

		QuoteBox = wx.StaticBox(self, -1, "Quote Configuration")
		QuoteBox.SetFont(self.StandardFont)
		self.QuoteBoxSizer = QuoteBoxSizer = wx.StaticBoxSizer(QuoteBox, wx.VERTICAL)

		CB_UseQuote = wx.CheckBox(self, -1, "Use Quote")
		CB_UseQuote.SetFont(self.StandardFont)
		#gbs.Add(CB_UseQuote,
		#		pos = (6,0), span = (1,2), flag = wx.ALIGN_LEFT)
		QuoteBoxSizer.Add(CB_UseQuote, 0, wx.TOP | wx.LEFT, 10)

		StaticInspQuote = wx.StaticText(self, -1, "Inspirational Quote:")
		StaticInspQuote.SetFont(self.StandardFont)
		StaticInspQuote.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		#gbs.Add(StaticInspQuote,
		#		pos = (7,0), span = (1,2), flag = wx.ALIGN_LEFT)
		QuoteBoxSizer.Add(StaticInspQuote, 0, wx.TOP | wx.LEFT, 10)

		TXT_Quote = wx.TextCtrl(self, -1, size = (350, 105))
		TXT_Quote.SetFont(self.StandardFont)
		#gbs.Add(TXT_Quote,
		#		pos = (8,0), span = (1,4), flag = wx.ALIGN_LEFT)
		QuoteBoxSizer.Add(TXT_Quote, 0, wx.TOP | wx.LEFT, 10)

		StaticAuthor = wx.StaticText(self, -1, "Author:")
		StaticAuthor.SetFont(self.StandardFont)
		#gbs.Add(StaticAuthor,
		#		pos = (9,0), span = (1,1), flag = wx.ALIGN_LEFT)
		QuoteBoxSizer.Add(StaticAuthor, 0, wx.TOP | wx.LEFT, 10)

		TXT_Author = wx.TextCtrl(self, -1, size=(250,35))
		TXT_Author.SetFont(self.StandardFont)
		#gbs.Add(TXT_Author,
		#		pos = (9,1), span = (1,2), flag = wx.ALIGN_LEFT)
		QuoteBoxSizer.Add(TXT_Author, 0, wx.TOP | wx.LEFT, 10)

		BTN_RestoreQuote = wx.Button(self, -1, "Restore Default")
		BTN_RestoreQuote.SetFont(self.StandardFont)
		#gbs.Add(BTN_RestoreQuote,
		#		pos = (10,0), span = (1,2), flag = wx.ALIGN_LEFT)
		QuoteBoxSizer.Add(BTN_RestoreQuote, 0, wx.TOP | wx.LEFT, 10)




	# tile the background bitmap loaded in __init__()
	def DrawBackground(self, dc):
		dc.DrawBitmap(self.bg_bmp, 0, 0)

	# Redraw the background over a 'damaged' area.
	def OnEraseBackground(self, evt):
		dc = evt.GetDC()

		if not dc:
			dc = wx.ClientDC(self)
			rect = self.GetUpdateRegion().GetBox()
			dc.SetClippingRect(rect)
		self.DrawBackground(dc)

	#def OnPaint(self, evt):
	#	#dc = wx.PaintDC(self)
	#	#self.PrepareDC(dc)
	#	dc = wx.BufferedPaintDC(self, self.bg_bmp)
	#	print dir(evt)
	#	print "Paint"
