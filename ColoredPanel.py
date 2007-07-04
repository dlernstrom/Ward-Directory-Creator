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
