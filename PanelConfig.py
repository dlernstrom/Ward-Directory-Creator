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
			fileMask = "*.csv", changeCallback = self.NewCSVFileCallback
			)
		if self.parent.GetConfigValue('file.csvlocation'):
			self.csvFile.SetValue(self.parent.GetConfigValue('file.csvlocation'))
		FolderBoxSizer.Add(self.csvFile, 0, wx.TOP | wx.LEFT, 10)

		self.ImagesDirectory = filebrowse.DirBrowseButton(
			self, -1, size=(700, 30),
			labelText = "Images Directory", changeCallback = self.NewImagesDirectory
			)
		if self.parent.GetConfigValue('file.imagesdirectory'):
			self.ImagesDirectory.SetValue(self.parent.GetConfigValue('file.imagesdirectory'))
		FolderBoxSizer.Add(self.ImagesDirectory, 0, wx.TOP | wx.LEFT, 10)

		self.PDF_Out_Directory = filebrowse.DirBrowseButton(
			self, -1, size=(700, 30),
			labelText = "PDF Output Directory", changeCallback = self.NewPDFDirectory
			)
		if self.parent.GetConfigValue('file.pdf_outdirectory'):
			self.PDF_Out_Directory.SetValue(self.parent.GetConfigValue('file.pdf_outdirectory'))
		FolderBoxSizer.Add(self.PDF_Out_Directory, 0, wx.TOP | wx.LEFT, 10)

		self.Image_Archive_Directory = filebrowse.DirBrowseButton(
			self, -1, size=(700, 30),
			labelText = "Image Archive Directory", changeCallback = self.NewArchiveDirectory
			)
		if self.parent.GetConfigValue('file.imagearchivedir'):
			self.Image_Archive_Directory.SetValue(self.parent.GetConfigValue('file.imagearchivedir'))
		FolderBoxSizer.Add(self.Image_Archive_Directory, 0, wx.TOP | wx.LEFT | wx.BOTTOM, 10)

		############################################################################
		## Missing Image Configuration Section
		MissingBox = wx.StaticBox(self, -1, "Missing Image Configuration")
		MissingBox.SetFont(self.StandardFont)
		self.MissingBoxSizer = MissingBoxSizer = wx.StaticBoxSizer(MissingBox, wx.VERTICAL)

		self.StaticName = wx.StaticText(self, -1, "Contact Name:")
		self.StaticName.SetFont(self.StandardFont)
		MissingBoxSizer.Add(self.StaticName, 0, wx.TOP | wx.LEFT, 10)

		NameList = self.parent.parent.AppHandle.GetNameList()
		self.Contact_Dropdown = wx.ComboBox(self, -1, choices = NameList)
		self.Contact_Dropdown.SetFont(self.TextBoxFont)
		if self.parent.GetConfigValue('missing.missingname') in NameList:
			self.Contact_Dropdown.SetStringSelection(self.parent.GetConfigValue('missing.missingname'))
		MissingBoxSizer.Add(self.Contact_Dropdown, 0, wx.TOP | wx.LEFT, 10)

		self.StaticPhone = wx.StaticText(self, -1, "Contact Phone:")
		self.StaticPhone.SetFont(self.StandardFont)
		MissingBoxSizer.Add(self.StaticPhone, 0, wx.TOP | wx.LEFT, 10)

		self.TXT_Phone = wx.TextCtrl(self, -1, size=(250,25))
		self.TXT_Phone.SetFont(self.TextBoxFont)
		if self.parent.GetConfigValue('missing.overridephone') == '1':
			self.TXT_Phone.Enable(True)
		else:
			self.TXT_Phone.Enable(False)
		MissingBoxSizer.Add(self.TXT_Phone, 0, wx.TOP | wx.LEFT, 10)

		self.CB_OverridePhone = wx.CheckBox(self, -1, "Override Phone")
		self.CB_OverridePhone.SetFont(self.StandardFont)
		if self.parent.GetConfigValue('missing.overridephone') == '1':
			self.CB_OverridePhone.SetValue(True)
		else:
			self.CB_OverridePhone.SetValue(False)
		MissingBoxSizer.Add(self.CB_OverridePhone, 0, wx.TOP | wx.LEFT, 10)

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

		self.Bind(wx.EVT_CHECKBOX, self.OnOverridePhone, self.CB_OverridePhone)
		self.Bind(wx.EVT_COMBOBOX, self.OnSelectMissing, self.Contact_Dropdown)

		self.Title = "Configuration"

	def NewCSVFileCallback(self, evt):
		self.parent.SetConfigValue('file.csvlocation', evt.GetString())
		#This will call an error if the handler is called prior to init being completed
		try:
			self.makingActive()
		except AttributeError:
			pass

	def NewImagesDirectory(self, evt):
		self.parent.SetConfigValue('file.imagesdirectory', evt.GetString())

	def NewPDFDirectory(self, evt):
		self.parent.SetConfigValue('file.pdf_outdirectory', evt.GetString())

	def NewArchiveDirectory(self, evt):
		self.parent.SetConfigValue('file.imagearchivedir', evt.GetString())

	def OnOverridePhone(self, evt):
		if evt.Checked():
			self.parent.SetConfigValue('missing.overridephone', '1')
			self.TXT_Phone.Enable(True)
		else:
			self.parent.SetConfigValue('missing.overridephone', '1')
			self.TXT_Phone.Enable(False)

	def OnSelectMissing(self, evt):
		self.parent.SetConfigValue('missing.missingname', evt.GetString())

	def makingActive(self):
		if self.parent.isValidCSV():
			self.StaticName.Enable(True)
			self.Contact_Dropdown.Enable(True)
			#Refresh choices to name list
			NameList = self.parent.parent.AppHandle.GetNameList()
			self.Contact_Dropdown.Clear()
			for Name in NameList:
				self.Contact_Dropdown.Append(Name)
			if self.parent.GetConfigValue('missing.missingname') in NameList:
				self.Contact_Dropdown.SetStringSelection(self.parent.GetConfigValue('missing.missingname'))
			self.StaticPhone.Enable(True)
			if self.parent.GetConfigValue('missing.overridephone') == '1':
				self.TXT_Phone.Enable(True)
			self.CB_OverridePhone.Enable(True)
		else:
			self.StaticName.Enable(False)
			self.Contact_Dropdown.Enable(False)
			self.StaticPhone.Enable(False)
			self.TXT_Phone.Enable(False)
			self.CB_OverridePhone.Enable(False)
