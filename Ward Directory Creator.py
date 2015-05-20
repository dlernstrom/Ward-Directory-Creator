# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import os
import site

site.addsitedir(os.getcwd())

handler = logging.getLogger()
handler.setLevel(logging.DEBUG)
handler.addHandler(logging.NullHandler())

import wx

from application.GUI import MyFrame


class MyApp(wx.App):
    def OnInit(self):
        win = MyFrame()
        win.Show(True)
        return True


if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
