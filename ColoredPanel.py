import wx

class ColoredPanel(wx.Window):
	def __init__(self, parent, color):
		self.id = wx.NewId()
		wx.Window.__init__(self, parent, self.id, style = wx.SIMPLE_BORDER)
		if not color == None:
			self.SetBackgroundColour(color)

		def OnCPSize(evt):
			self.SetSize(evt.GetSize())

		self.Bind(wx.EVT_SIZE, OnCPSize)
