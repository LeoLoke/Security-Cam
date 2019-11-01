# Author: Rodrigo Graca

from GUI.CameraPanel import ShowCapture
from Detection.Camera import Camera

import wx


class CamGUI(wx.Frame):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(CamGUI, self).__init__(*args, **kw)

        self.camera = Camera()

        # create a panel in the frame
        # self.pnl = wx.Panel(self)
        # self.makePanelElements()

        # self.captureWindow = ShowCapture(self, self.camera)

        self.textCtrl = None
        self.myBtn = None
        self.capturePanel = None

    def makePanelElements(self):
        # self.textCtrl = wx.TextCtrl(self.pnl, pos=(5, 5))
        # self.myBtn = wx.Button(self.pnl, label='Press Me', pos=(5, 55))
        pass

    def OnExit(self, event):
        # Close the frame and terminate any connection

        self.Close(True)
