import time

import wx

from Engine import Application
import Notebook

import __version__

SEND_EMAILS = 0
#SMTP_SERVER = 'smtp.forward.email.dupont.com'
#SMTP_SERVER = 'smtp.comcast.net'
DEBUG = 0

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

        self.AppHandle = Application.Application(self, DEBUG)

        self.SetTitle("Ward Directory Creator v." + __version__.__version__)
        self.StatusBar = wx.StatusBar(self, -1)
        self.StatusBar.SetStatusText("Version " + __version__.__version__)
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