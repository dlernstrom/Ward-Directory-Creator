# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import os
import site

site.addsitedir(os.getcwd())

handler = logging.getLogger()
handler.setLevel(logging.DEBUG)
handler.addHandler(logging.NullHandler())

from application import GUI

app = GUI.MyApp(False)
app.MainLoop()
