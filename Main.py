# Author: Rodrigo Graca

from GUI.SecurityCamGUI import CamGUI
from Server.Server import Server
import Constants

import logging
import time
import cv2
import wx


def main():
    logging.basicConfig(level=logging.INFO)

    # app = wx.App()
    # frame = CamGUI(
    #     None, title="Security", size=Constants.WINDOW_SIZE,
    #     style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
    # )
    # frame.Show()
    # app.MainLoop()

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

    server = Server()

    server.start()

    logging.basicConfig(level=logging.INFO)

    # server.camera.recordForTime(15, 'testTimer.avi')

    while server.running:
        if server.threshFrame is not None:
            cv2.imshow('Thresh', server.threshFrame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        time.sleep(.1)
        pass


if __name__ == '__main__':
    main()
