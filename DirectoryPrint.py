import wx
import time
import Application

SEND_EMAILS = 0
SMTP_SERVER = 'smtp.forward.email.dupont.com'
#SMTP_SERVER = 'smtp.comcast.net'
APPDATAFOLDER = 'Ward Directory'
DEBUG = 0
MISSING_PEOPLE_EMAILS = ['david.ernstrom@usa.dupont.com', 'tina@ernstrom.net', 'david@ernstrom.net']
DIRECTORY_IMAGES = 'C:\\Documents and Settings\\Administrator\\Desktop\\Directory\\WardPictures\\'
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

		panel = wx.Panel(self, -1, style = wx.TAB_TRAVERSAL
						 | wx.CLIP_CHILDREN
						 | wx.FULL_REPAINT_ON_RESIZE
						 )

		gbs = self.gbs = wx.GridBagSizer(15, 6)

		Title = wx.StaticText(panel, -1, "Ward Photo Directory Printing Tool")
		Title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
		gbs.Add( Title, (0,0), (1,6), wx.ALIGN_CENTER, wx.ALL, 5)

		PrintButton = wx.Button(panel, -1, "Print")
		gbs.Add(PrintButton, (5, 5))

		gbs.AddGrowableRow(14)
		gbs.AddGrowableCol(0)
		gbs.AddGrowableCol(5)

		panel.SetSizerAndFit(gbs)
		self.SetClientSize(panel.GetSize())

		self.Bind(wx.EVT_BUTTON, self.OnDoPrint, PrintButton)
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
		Application.Application(self, 'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '.pdf',
				  'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '_FRONT.pdf',
				  'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '_BACK.pdf',
				  APPDATAFOLDER,
				  DIRECTORY_IMAGES,
				  CSV_LOCATION,
				  SEND_EMAILS,
				  SMTP_SERVER,
				  MISSING_PEOPLE_EMAILS,
				  DEBUG
				  )
		self.Destroy()



	def OnCloseWindow(self, event):
		self.Destroy()

	def OnDoPrint(self, event):
		Application.Application(self,
								'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '.pdf',
								'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '_FRONT.pdf',
								'PhotoDirectory_' + time.strftime("%Y_%m_%d_%H_%M") + '_BACK.pdf',
								APPDATAFOLDER,
								DIRECTORY_IMAGES,
								CSV_LOCATION,
								SEND_EMAILS,
								SMTP_SERVER,
								MISSING_PEOPLE_EMAILS,
								DEBUG
								)

class MyApp(wx.App):
	def OnInit(self):
		win = MyFrame(None, -1, "Ward Photo Directory Printing/Configuration Utility", size=wx.DefaultSize,
				style = wx.DEFAULT_FRAME_STYLE)
		win.Show(True)
		return True

if __name__ == '__main__':
	app = MyApp(False)
	app.MainLoop()

