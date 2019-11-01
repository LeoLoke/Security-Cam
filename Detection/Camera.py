# Author: Rodrigo Graca

from Constants import STD_DIMENSIONS, VIDEO_TYPE, VIDEO_DIR, CAMERA_INIT_TIME, CHIME_ENABLED

from playsound import playsound
from threading import Timer
from hashlib import sha512
import logging
import time
import cv2
import os


class Camera:
    def __init__(self, deviceID=0):
        self.deviceID = deviceID

        self.captureDevice = cv2.VideoCapture(self.deviceID, cv2.CAP_DSHOW)

        self.currentDim = STD_DIMENSIONS['720p']
        self.changeRes(self.currentDim[0], self.currentDim[1])

        self.sinceLastFrame = 0
        self.fps = 29

        self.recording = False

        # Store current recordings
        self.currentRecordings = {}

        # Sleep for a bit to allow the camera time to initialize
        time.sleep(CAMERA_INIT_TIME)

        if not os.path.exists(VIDEO_DIR):
            os.makedirs(VIDEO_DIR)

    def setDevice(self, deviceID):
        self.deviceID = deviceID

        self.captureDevice.release()
        self.captureDevice = cv2.VideoCapture(self.deviceID, cv2.CAP_DSHOW)

    def getFrame(self, gray=True):

        # Grab the most recent img from camera
        ret, frame = self.captureDevice.read()

        if ret:

            # If recording active and time for single frame has passed, write current frame to each recording
            currentTime = time.time()
            if self.recording and self.sinceLastFrame + (1 / self.fps) <= currentTime:
                for recording in self.currentRecordings.values():
                    recording.write(frame)

                self.sinceLastFrame = currentTime

            # If gray scale option, convert to grey
            if gray:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return frame
        else:
            return None

    def startRec(self, filename):

        # Create new VideoWriter to record video
        videoOut = cv2.VideoWriter(
            VIDEO_DIR + filename,
            self.getVideoExt(filename),
            int(self.fps / 2),
            self.currentDim
        )

        # Produce a identifier for the recording by it's initialized time
        ID = sha512((str(time.time())).encode('utf-8')).digest().hex()
        logging.debug(ID)

        # Produce another if key already utilized
        while ID in self.currentRecordings.keys():
            ID = sha512((str(time.time())).encode('utf-8')).digest().hex()
            time.sleep(.02)

        # Add recording to recordings dict
        self.currentRecordings.update({ID: videoOut})

        self.recording = True

        if CHIME_ENABLED:
            playsound('Detection/chime.wav', False)

        logging.info('Started Recording')

        return ID

    def stopRec(self, ID):

        # Iterate through the dict, find + remove from, and release the recording
        if ID in self.currentRecordings:
            videoOut = self.currentRecordings.pop(ID)
            videoOut.release()

            # Leave recording as True if other recordings are still active
            self.recording = len(self.currentRecordings) > 0
            self.sinceLastFrame = 0

            logging.info('Stopped Recording')
        else:
            logging.debug('Recording ' + ID + 'not present')

    def close(self):

        # Iterate through each recording and release it
        for recording in self.currentRecordings.keys():
            self.stopRec(recording)

        # Clear recordings and release camera
        self.currentRecordings = {}
        self.captureDevice.release()

        logging.debug('Closed Cam')

    # Reset the Camera obj
    def reset(self):
        self.close()
        self.captureDevice = cv2.VideoCapture(self.deviceID)

    # Record video for x amount of seconds
    def recordForTime(self, seconds, filename):
        ID = self.startRec(filename)
        timer = Timer(seconds, self.stopRec, args=[ID])
        timer.daemon = True
        timer.start()

    # Set resolution of the camera
    def changeRes(self, width, height):
        self.captureDevice.set(3, width)
        self.captureDevice.set(4, height)

    # Grab res dimensions from array, otherwise return default
    def getDims(self, res='480p'):
        width, height = STD_DIMENSIONS['480p']
        if res in STD_DIMENSIONS:
            width, height = STD_DIMENSIONS[res]

        return width, height

    @staticmethod
    def getVideoExt(filename):
        filename, extension = os.path.splitext(filename)
        if extension in VIDEO_TYPE:
            return VIDEO_TYPE[extension]
        return VIDEO_TYPE['avi']

