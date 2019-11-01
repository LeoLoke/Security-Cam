# Author: Rodrigo Graca

import wx
import cv2


class ShowCapture(wx.Panel):
    def __init__(self, parent, camera, fps=25):
        wx.Panel.__init__(self, parent)

        self.camera = camera

        frame = self.camera.getFrame()

        height, width = frame.shape[:2]
        # parent.SetSize((width, height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.bmp = wx.Bitmap.FromBuffer(width, height, frame)

        self.timer = wx.Timer(self)
        self.timer.Start(1000. / fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

        evt.Skip()

    def NextFrame(self, evt):
        frame = self.camera.getFrame()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()

        evt.Skip()
