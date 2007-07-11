#PanelConfig.py
import wx
from ColoredPanel import *
import  wx.lib.filebrowsebutton as filebrowse

class ConfigPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, None)

		#sizer = wx.BoxSizer(wx.VERTICAL)

		#self.csvFile = filebrowse.FileBrowseButton(
		#	self, -1, size=(450, 30),
		#	labelText = "Membership File",
		#	fileMask = "*.csv"#, changeCallback = self.fbbCallback
		#	)
		#sizer.Add(self.csvFile)

		#self.ImagesFolder = filebrowse.DirBrowseButton(
		#	self, -1, size=(450, 100),
		#	labelText = "Images Folder",
		#	)
		#sizer.Add(self.ImagesFolder)

		#self.SetSizerAndFit(sizer)
		#parent.SetClientSize(self.GetSize())
		############################################################################
		## File/Folder Configuration
		FolderBox = wx.StaticBox(self, -1, "File/Folder Configuration")
		FolderBox.SetFont(self.StandardFont)
		self.FolderBoxSizer = FolderBoxSizer = wx.StaticBoxSizer(FolderBox, wx.VERTICAL)

		self.csvFile = filebrowse.FileBrowseButton(
			self, -1, size=(700, 30),
			labelText = "Membership File",
			fileMask = "*.csv"#, changeCallback = self.fbbCallback
			)
		FolderBoxSizer.Add(self.csvFile, 0, wx.TOP | wx.LEFT, 10)

		self.ImagesDirectory = filebrowse.DirBrowseButton(
			self, -1, size=(700, 30),
			labelText = "Images Directory",
			)
		FolderBoxSizer.Add(self.ImagesDirectory, 0, wx.TOP | wx.LEFT, 10)

		self.PDF_Out_Directory = filebrowse.DirBrowseButton(
			self, -1, size=(700, 30),
			labelText = "PDF Output Directory",
			)
		FolderBoxSizer.Add(self.PDF_Out_Directory, 0, wx.TOP | wx.LEFT, 10)

		self.Image_Archive_Directory = filebrowse.DirBrowseButton(
			self, -1, size=(700, 30),
			labelText = "Image Archive Directory",
			)
		FolderBoxSizer.Add(self.Image_Archive_Directory, 0, wx.TOP | wx.LEFT | wx.BOTTOM, 10)

		############################################################################
		## Missing Image Configuration Section
		MissingBox = wx.StaticBox(self, -1, "Missing Image Configuration")
		MissingBox.SetFont(self.StandardFont)
		self.MissingBoxSizer = MissingBoxSizer = wx.StaticBoxSizer(MissingBox, wx.VERTICAL)

		StaticInspQuote = wx.StaticText(self, -1, "Inspirational Quote:")
		StaticInspQuote.SetFont(self.StandardFont)
		StaticInspQuote.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		MissingBoxSizer.Add(StaticInspQuote, 0, wx.TOP | wx.LEFT, 10)

		StaticAuthor = wx.StaticText(self, -1, "Author:")
		StaticAuthor.SetFont(self.StandardFont)
		MissingBoxSizer.Add(StaticAuthor, 0, wx.TOP | wx.LEFT, 10)

		TXT_Author = wx.TextCtrl(self, -1, size=(250,25))
		TXT_Author.SetFont(self.TextBoxFont)
		MissingBoxSizer.Add(TXT_Author, 0, wx.TOP | wx.LEFT, 10)

		############################################################################
		## Email Configuration Section
		EmailBox = wx.StaticBox(self, -1, "Email Configuration")
		EmailBox.SetFont(self.StandardFont)
		self.EmailBoxSizer = EmailBoxSizer = wx.StaticBoxSizer(EmailBox, wx.VERTICAL)

		StaticInspQuote = wx.StaticText(self, -1, "Inspirational Quote:")
		StaticInspQuote.SetFont(self.StandardFont)
		StaticInspQuote.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
		EmailBoxSizer.Add(StaticInspQuote, 0, wx.TOP | wx.LEFT, 10)

		StaticAuthor = wx.StaticText(self, -1, "Author:")
		StaticAuthor.SetFont(self.StandardFont)
		EmailBoxSizer.Add(StaticAuthor, 0, wx.TOP | wx.LEFT, 10)

		#TXT_Author = wx.TextCtrl(self, -1, size=(250,25))
		#TXT_Author.SetFont(self.TextBoxFont)
		#EmailBoxSizer.Add(TXT_Author, 0, wx.TOP | wx.LEFT, 10)

		#######################################################################
		## Non wrapped items

		logo = wx.StaticBitmap(self, -1, self.logo_bmp, (self.logo_bmp.GetWidth(), self.logo_bmp.GetHeight()))

		#######################################################################
		## Sizer encapsulation section
		#top_left_level3 = wx.BoxSizer()
		#top_left_level3.Add(FolderBoxSizer, 1, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, 25)

		#top_right_level3 = wx.BoxSizer(wx.VERTICAL)
		#top_right_level3.Add(self.EmailBoxSizer, 6, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, 25)

		#top_level2 = wx.BoxSizer(wx.HORIZONTAL)
		#top_level2.Add(top_left_level3, 3, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
		#top_level2.Add(top_right_level3, 2, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)

		bottom_left_level3 = wx.BoxSizer(wx.VERTICAL)
		bottom_left_level3.Add(logo, 0, wx.EXPAND | wx.BOTTOM, 25)
		bottom_left_level3.Add(self.MissingBoxSizer, 1, wx.EXPAND)

		bottom_right_level3 = wx.BoxSizer()
		bottom_right_level3.Add(self.EmailBoxSizer, 5, wx.EXPAND)

		bottom_level2 = wx.BoxSizer(wx.HORIZONTAL)
		bottom_level2.Add(bottom_left_level3, 2, wx.EXPAND)
		bottom_level2.Add(bottom_right_level3, 3, wx.EXPAND | wx.LEFT, 25)

		inside_border_level1 = wx.BoxSizer(wx.VERTICAL)
		inside_border_level1.Add(FolderBoxSizer, 0, wx.EXPAND | wx.BOTTOM, 25)
		inside_border_level1.Add(bottom_level2, 1, wx.EXPAND)

		border_level0 = wx.BoxSizer()
		border_level0.Add(inside_border_level1, 1, wx.EXPAND | wx.ALL, 25)
		self.SetSizer(border_level0)
		border_level0.SetDimension(0, 0, self.GetSize()[0], self.GetSize()[1])

		print "Level 0 - position:",border_level0.GetPosition()
		print "Level 0 - size:",border_level0.GetSize()

		print "Level 1 - Inner Border position:", inside_border_level1.GetPosition()
		print "Level 1 - Inner Border size:", inside_border_level1.GetSize()

		print "FolderBoxSize: ", str(self.FolderBoxSizer.GetSize())
		'''
		print "Level 2 - Top Sizer position:", top_level2.GetPosition()
		print "Level 2 - Top Sizer size:", top_level2.GetSize()

		print "Level 2 - Bottom Sizer position:", bottom_level2.GetPosition()
		print "Level 2 - Bottom Sizer size:", bottom_level2.GetSize()

		print "Level 3 - Top Left Content position:", top_left_level3.GetPosition()
		print "Level 3 - Top Left Content size:", top_left_level3.GetSize()

		print "Level 3 - Top Right Content position:", top_right_level3.GetPosition()
		print "Level 3 - Top Right Content size:", top_right_level3.GetSize()

		print "Level 3 - logo Content position:", logo.GetPosition()
		print "Level 3 - logo Content size:", logo.GetSize()


		print "Level 3 - Bottom Right Content position:", bottom_right_level3.GetPosition()
		print "Level 3 - Bottom Right Content size:", bottom_right_level3.GetSize()
		'''
		self.Title = "Configuration"





