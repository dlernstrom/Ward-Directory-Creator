import wx
import time
import Application
import Notebook

SEND_EMAILS = 0
SMTP_SERVER = 'smtp.forward.email.dupont.com'
#SMTP_SERVER = 'smtp.comcast.net'
APPDATAFOLDER = 'Ward Directory'
DEBUG = 0
MISSING_PEOPLE_EMAILS = ['david.ernstrom@usa.dupont.com', 'tina@ernstrom.net', 'david@ernstrom.net']
DIRECTORY_IMAGES = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\WardPictures\\'
MOVED_OUT = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\ImageArchive\\'
CSV_LOCATION = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\'

########################
## Application Options:
## -Analyze Ward Data
##     -Parse Ward Data
##     -Paginate Ward
##     -Add Filler Pages
##     -Repaginate Ward
## -Generate Booklet PDF
## -Generate Standard PDF
## -Generate Missing List
## -Email Missing List
## -Extract Moved Family Images

class MyFrame(wx.Frame):
	def __init__(
			self, parent, ID, title, pos=wx.DefaultPosition,
			size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE
			):
		wx.Frame.__init__(self, parent, ID, title, pos, size, style)
		self.AppHandle = Application.Application(self,
								'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '.pdf',
								'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '_FRONT.pdf',
								'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '_BACK.pdf',
								APPDATAFOLDER,
								DIRECTORY_IMAGES,
								MOVED_OUT,
								CSV_LOCATION,
								SEND_EMAILS,
								SMTP_SERVER,
								MISSING_PEOPLE_EMAILS,
								DEBUG
								)
		self.FullAppVersion = self.AppHandle.GetFullVersion()
		self.MajorAppVersion = self.AppHandle.GetMajorVersion()
		self.SetTitle("Ward Directory Creator " + self.MajorAppVersion)
		self.StatusBar = wx.StatusBar(self, -1)
		self.StatusBar.SetStatusText("Version " + self.FullAppVersion)
		self.myNotebook = Notebook.Notebook(self, -1, self.AppHandle)

		self.Fit()

	def OnCloseWindow(self, event):
		self.Destroy()

	def OnDoPrint(self, event):
		self.AppHandle.InitiatePDF()

class MyApp(wx.App):
	def OnInit(self):
		win = MyFrame(None, -1, "Ward Directory Creator", size=wx.DefaultSize,
				style = wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX
					  | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
		win.Show(True)
		return True

if __name__ == '__main__':
	app = MyApp(False)
	app.MainLoop()

