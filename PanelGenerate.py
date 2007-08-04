#PanelGenerate.py

import wx
import wx.lib
import wx.lib.dialogs
from ColoredPanel import *
import  wx.lib.filebrowsebutton as filebrowse

class GeneratePanel(ColoredPanel):
	def __init__(self, parent):
		ColoredPanel.__init__(self, parent, None)
		self.parent = parent
		self.AppHandle = self.parent.parent.AppHandle

		##################################################
		## Here's the email config box
		EmailBox = wx.StaticBox(self, -1, "Email Configuration")
		EmailBox.SetFont(self.StandardFont)
		EmailBoxSizer = wx.StaticBoxSizer(EmailBox, wx.VERTICAL)

		self.StaticSMTP = wx.StaticText(self, -1, "SMTP Server")
		self.StaticSMTP.SetFont(self.StandardFont)
		EmailBoxSizer.Add(self.StaticSMTP, 0, wx.TOP | wx.LEFT, 10)

		self.TXT_SMTPAddy = wx.TextCtrl(self, -1, size = (200, -1))
		self.TXT_SMTPAddy.SetFont(self.StandardFont)
		EmailBoxSizer.Add(self.TXT_SMTPAddy, 0, wx.TOP | wx.LEFT, 10)

		self.StaticUser = wx.StaticText(self, -1, "User Name")
		self.StaticUser.SetFont(self.StandardFont)
		EmailBoxSizer.Add(self.StaticUser, 0, wx.TOP | wx.LEFT, 10)

		self.TXT_User = wx.TextCtrl(self, -1, size = (200, -1))
		self.TXT_User.SetFont(self.StandardFont)
		EmailBoxSizer.Add(self.TXT_User, 0, wx.TOP | wx.LEFT, 10)

		self.StaticPass = wx.StaticText(self, -1, "Password")
		self.StaticPass.SetFont(self.StandardFont)
		EmailBoxSizer.Add(self.StaticPass, 0, wx.TOP | wx.LEFT, 10)

		self.TXT_Pass = wx.TextCtrl(self, -1, size = (200, -1), style = wx.TE_PASSWORD)
		self.TXT_Pass.SetFont(self.StandardFont)
		EmailBoxSizer.Add(self.TXT_Pass, 0, wx.TOP | wx.LEFT, 10)

		#################################################
		## Here's the generate directory box
		StaticBox = wx.StaticBox(self, -1, "Generate Directory")
		StaticBox.SetFont(self.StandardFont)
		StaticBoxSizer = wx.StaticBoxSizer(StaticBox, wx.VERTICAL)

		self.CB_MissingReport = wx.CheckBox(self, -1, "View Missing Pictures Report")
		self.CB_MissingReport.SetFont(self.StandardFont)
		StaticBoxSizer.Add(self.CB_MissingReport, 0, wx.TOP | wx.LEFT, 10)

		self.CB_SendEmail = wx.CheckBox(self, -1, "Send Missing Pictures Email")
		self.CB_SendEmail.SetFont(self.StandardFont)
		StaticBoxSizer.Add(self.CB_SendEmail, 0, wx.TOP | wx.LEFT, 10)

		self.CB_MissingFile = wx.CheckBox(self, -1, "Generate Missing Pictures File")
		self.CB_MissingFile.SetFont(self.StandardFont)
		StaticBoxSizer.Add(self.CB_MissingFile, 0, wx.TOP | wx.LEFT, 10)

		self.CB_ExtractMoveOuts = wx.CheckBox(self, -1, 'Archive "Moved-Out" Images')
		self.CB_ExtractMoveOuts.SetFont(self.StandardFont)
		StaticBoxSizer.Add(self.CB_ExtractMoveOuts, 0, wx.TOP | wx.LEFT, 10)

		self.CB_GenPDF_Full = wx.CheckBox(self, -1, "Generate Full Spread PDF")
		self.CB_GenPDF_Full.SetFont(self.StandardFont)
		StaticBoxSizer.Add(self.CB_GenPDF_Full, 0, wx.TOP | wx.LEFT, 10)

		self.CB_GenPDF_Booklet = wx.CheckBox(self, -1, "Generate Booklet PDF")
		self.CB_GenPDF_Booklet.SetFont(self.StandardFont)
		StaticBoxSizer.Add(self.CB_GenPDF_Booklet, 0, wx.TOP | wx.LEFT, 10)

		self.BTN_Go = wx.Button(self, -1, "Go!")
		self.BTN_Go.SetFont(self.StandardFont)
		StaticBoxSizer.Add(self.BTN_Go, 0, wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, 10)

		##############################################
		## Here's the outer sizer container stuff
		border_level0 = wx.BoxSizer()
		border_level0.Add(StaticBoxSizer, 1, wx.EXPAND | wx.ALL, 25)
		border_level0.Add(EmailBoxSizer, 1, wx.EXPAND | wx.ALL, 25)

		self.Bind(wx.EVT_BUTTON, self.OnGoButton, self.BTN_Go)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckMissingReport, self.CB_MissingReport)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckSendEmail, self.CB_SendEmail)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckMissingFile, self.CB_MissingFile)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckExtractMoveOuts, self.CB_ExtractMoveOuts)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckGenFull, self.CB_GenPDF_Full)
		self.Bind(wx.EVT_CHECKBOX, self.OnCheckGenBooklet, self.CB_GenPDF_Booklet)
		self.Bind(wx.EVT_TEXT, self.OnSMTPChanged, self.TXT_SMTPAddy)
		self.Bind(wx.EVT_TEXT, self.OnUserChanged, self.TXT_User)
		self.Bind(wx.EVT_TEXT, self.OnPassChanged, self.TXT_Pass)

		self.SetSizer(border_level0)
		border_level0.SetDimension(0, 0, self.GetSize()[0], self.GetSize()[1])

		#Here's the logic to set up the prevalues from config file
		if self.parent.GetConfigValue('email.smtp'):
			self.TXT_SMTPAddy.SetValue(self.parent.GetConfigValue('email.smtp'))
		if self.parent.GetConfigValue('email.username'):
			self.TXT_User.SetValue(self.parent.GetConfigValue('email.username'))
		if self.parent.GetConfigValue('email.pass'):
			self.TXT_Pass.SetValue(self.parent.GetConfigValue('email.pass'))

		self.Title = "Generate"

	def OnSMTPChanged(self, evt):
		self.parent.SetConfigValue('email.smtp', evt.GetString())

	def OnUserChanged(self, evt):
		self.parent.SetConfigValue('email.username', evt.GetString())

	def OnPassChanged(self, evt):
		self.parent.SetConfigValue('email.pass', evt.GetString())

	def OnCheckMissingReport(self, evt):
		if evt.Checked():
			self.parent.SetConfigValue('task.missreport', '1')
		else:
			self.parent.SetConfigValue('task.missreport', '0')

	def OnCheckSendEmail(self, evt):
		if evt.Checked():
			self.parent.SetConfigValue('task.sendemail', '1')
		else:
			self.parent.SetConfigValue('task.sendemail', '0')

	def OnCheckMissingFile(self, evt):
		if evt.Checked():
			self.parent.SetConfigValue('task.genmissfile', '1')
		else:
			self.parent.SetConfigValue('task.genmissfile', '0')

	def OnCheckExtractMoveOuts(self, evt):
		if evt.Checked():
			self.parent.SetConfigValue('task.extract_moveouts', '1')
		else:
			self.parent.SetConfigValue('task.extract_moveouts', '0')

	def OnCheckGenFull(self, evt):
		if evt.Checked():
			self.parent.SetConfigValue('task.genfull', '1')
		else:
			self.parent.SetConfigValue('task.genfull', '0')

	def OnCheckGenBooklet(self, evt):
		if evt.Checked():
			self.parent.SetConfigValue('task.genbooklet', '1')
		else:
			self.parent.SetConfigValue('task.genbooklet', '0')

	def OnGoButton(self, evt):
		#Here, I need to check each of the (7) things to do and do them
		if self.parent.GetConfigValue('task.sendemail') == '1':
			print "Sending Emails"
			self.AppHandle.SendEmails()
		if self.parent.GetConfigValue('task.genmissfile') == '1':
			print "Generating Missing File"
		if self.parent.GetConfigValue('task.extract_moveouts') == '1':
			print "Extracting Move-Outs"
			LiveFolder = self.parent.GetConfigValue('file.imagesdirectory')
			ArchiveFolder = self.parent.GetConfigValue('file.imagearchivedir')
			self.AppHandle.MoveSuperflousImages(LiveFolder, ArchiveFolder)

		#Generate PDF Stuff Here
		Full = 0
		if self.parent.GetConfigValue('task.genfull') == '1':
			print "Generating Full PDF"
			Full = 1

		Booklet = 0
		if self.parent.GetConfigValue('task.genbooklet') == '1':
			print "Generating Booklet PDF"
			Booklet = 1
		if Full or Booklet:
			ImageDirectory = self.parent.GetConfigValue('file.imagesdirectory')
			OutputFolder = self.parent.GetConfigValue('file.pdf_outdirectory')
			DictionaryData = None
			self.AppHandle.InitiatePDF(ImageDirectory, OutputFolder, Full, Booklet)
		#Generate Missing Image Report
		if self.parent.GetConfigValue('task.missreport') == '1':
			print "Generating missing report"
			LiveFolder = self.parent.GetConfigValue('file.imagesdirectory')
			msg = self.AppHandle.GetMissingMsg(LiveFolder)
			dlg = wx.lib.dialogs.ScrolledMessageDialog(self, msg, caption = "Missing Images Report", size=(500,600))
			dlg.ShowModal()

	def makingActive(self):
		if self.parent.GetConfigValue('task.missreport') == '1':
			self.CB_MissingReport.SetValue(True)
		if self.parent.GetConfigValue('task.sendemail') == '1':
			self.CB_SendEmail.SetValue(True)
		if self.parent.GetConfigValue('task.genmissfile') == '1':
			self.CB_MissingFile.SetValue(True)
		if self.parent.GetConfigValue('task.extract_moveouts') == '1':
			self.CB_ExtractMoveOuts.SetValue(True)
		if self.parent.GetConfigValue('task.genfull') == '1':
			self.CB_GenPDF_Full.SetValue(True)
		if self.parent.GetConfigValue('task.genbooklet') == '1':
			self.CB_GenPDF_Booklet.SetValue(True)

