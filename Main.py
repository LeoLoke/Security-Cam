# Author: Rodrigo Graca

from GUI.SecurityCamGUI import CamGUI
import Constants

import logging
import cv2
import wx


def main():
    logging.basicConfig(level=logging.INFO)

    app = wx.App()
    frame = CamGUI(
        None, title="Security", size=Constants.WINDOW_SIZE,
        style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
    )
    frame.Show()
    app.MainLoop()

    # cam = Camera()
    # cam.recordForTime(10, 'test.avi')
    #
    # while cam.recording:
    #     frame = cam.getFrame()
    #
    #     cv2.imshow('Camera', frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    #
    # cam.close()


if __name__ == '__main__':
    main()
