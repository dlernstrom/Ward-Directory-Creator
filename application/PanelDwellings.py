import wx
import wx.lib.filebrowsebutton as filebrowse

from ColoredPanel import *

class DwellingsPanel(ColoredPanel):
    Title = "Dwellings"
    def __init__(self, parent):
        ColoredPanel.__init__(self, parent, wx.BLUE)

        ScheduleGrid = wx.GridBagSizer()

        self.SetSizer(ScheduleGrid)

    def makingActive(self):
        pass

