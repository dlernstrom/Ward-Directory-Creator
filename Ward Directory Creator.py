import logging
import os
import site

site.addsitedir(os.getcwd())
#from LoganTools import connections
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", connections.djangoSettings)

handler = logging.getLogger()
handler.setLevel(logging.DEBUG)
handler.addHandler(logging.NullHandler())

#from LoganTools.Logging import FileLoggingManager
#log = FileLoggingManager.RedirectedFileLogManager(appNameLong = 'Shipping Application', appNameShort = 'Shipping')

#from LoganTools.wxTools import TracebackPlusWX
#sys.excepthook = TracebackPlusWX.traceback_plus_wx_hook

from application import GUI

app = GUI.MyApp(False)
app.MainLoop()
