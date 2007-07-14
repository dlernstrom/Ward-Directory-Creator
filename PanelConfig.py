#PanelConfig.py
import wx
from ColoredPanel import *
import  wx.lib.filebrowsebutton as filebrowse

class ConfigPanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, None)
		self.parent = parent

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

		StaticName = wx.StaticText(self, -1, "Contact Name:")
		StaticName.SetFont(self.StandardFont)
		MissingBoxSizer.Add(StaticName, 0, wx.TOP | wx.LEFT, 10)

		self.NamePhoneList = self.parent.parent.AppHandle.GetNamePhoneList()
		NameList = map(lambda x: x[0], self.NamePhoneList)
		Contact_Dropdown = wx.ComboBox(self, -1, choices = NameList)
		Contact_Dropdown.SetFont(self.TextBoxFont)
		MissingBoxSizer.Add(Contact_Dropdown, 0, wx.TOP | wx.LEFT, 10)

		StaticPhone = wx.StaticText(self, -1, "Contact Phone:")
		StaticPhone.SetFont(self.StandardFont)
		MissingBoxSizer.Add(StaticPhone, 0, wx.TOP | wx.LEFT, 10)

		TXT_Author = wx.TextCtrl(self, -1, size=(250,25))
		TXT_Author.SetFont(self.TextBoxFont)
		MissingBoxSizer.Add(TXT_Author, 0, wx.TOP | wx.LEFT, 10)

		CB_OverridePhone = wx.CheckBox(self, -1, "Override Phone")
		CB_OverridePhone.SetFont(self.StandardFont)
		MissingBoxSizer.Add(CB_OverridePhone, 0, wx.TOP | wx.LEFT, 10)

		############################################################################
		## Email Configuration Section
		EmailBox = wx.StaticBox(self, -1, "Email Configuration")
		EmailBox.SetFont(self.StandardFont)
		self.EmailBoxSizer = EmailBoxSizer = wx.StaticBoxSizer(EmailBox, wx.VERTICAL)

		StaticInspQuote = wx.StaticText(self, -1, "Email Recipients")
		StaticInspQuote.SetFont(self.StandardFont)
		EmailBoxSizer.Add(StaticInspQuote, 0, wx.TOP | wx.LEFT, 10)

		self.EmailList = self.parent.parent.AppHandle.GetMemberEmails()
		Email_Dropdown = wx.ComboBox(self, -1, size = (390, 24),
									 choices = self.EmailList, style = wx.CB_READONLY)
		Email_Dropdown.SetFont(self.TextBoxFont)
		EmailBoxSizer.Add(Email_Dropdown, 0, wx.TOP | wx.LEFT, 10)

		self.BTN_AddEmail = wx.Button(self, wx.ID_ADD)
		self.BTN_AddEmail.SetFont(self.TextBoxFont)
		EmailBoxSizer.Add(self.BTN_AddEmail, 0, wx.TOP | wx.LEFT, 10)

		self.EmailList = wx.ListBox(self, -1, size = (390, 151))
		self.EmailList.SetFont(self.TextBoxFont)
		EmailBoxSizer.Add(self.EmailList, 1, wx.TOP | wx.LEFT, 10)

		self.BTN_RemoveEmail = wx.Button(self, wx.ID_REMOVE)
		self.BTN_RemoveEmail.SetFont(self.TextBoxFont)
		EmailBoxSizer.Add(self.BTN_RemoveEmail, 0, wx.TOP | wx.LEFT, 10)

		#######################################################################
		## Non wrapped items
		logo = wx.StaticBitmap(self, -1, self.logo_bmp, (self.logo_bmp.GetWidth(), self.logo_bmp.GetHeight()))

		#######################################################################
		## Sizer encapsulation section
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

		self.Title = "Configuration"





