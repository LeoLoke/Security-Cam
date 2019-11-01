# Author: Rodrigo Graca

from Constants import STATIC_UPDATE_TIME, MOTION_CHECK_DELAY, THRESHHOLD_SUM, THRESHHOLD_SENSITIVITY, STD_DIMENSIONS, \
    VIDEO_DIR, OPERATION_START_TIME, OPERATION_END_TIME
from Detection.Camera import Camera
from Communication.SMS import send

from datetime import datetime
from math import log

import threading
import logging
import socket
import time
import cv2
import os


class Server(threading.Thread):
    def __init__(self, server_addr=('', 65532), daemon=True):

        # Getting the local address of the computer in the network
        super(Server, self).__init__(daemon=daemon)

        localHostname = socket.gethostname()
        self.internalIP = socket.gethostbyname(localHostname)

        # Controls if the thread is functioning
        self.running = True

        # Control camera motion detection
        self.detectMotion = True  # Say if we should detect
        self.staticBack = None  # Assigning our staticBack to None
        self.staticLastUpdateTime = None  # Used to check time since last background comparision image update

        self.motion = False  # Flag for motion
        self.motionTime = 0  # Time since last motion detection, prevents motion detection spam
        self.threshFrame = None  # Visual representation of movement detection

        self.showCam = True

        self.record = False
        self.recordID = None

        # Initialize Camera
        self.camera = Camera()

        self.motionLock = threading.Lock()
        self.cameraLock = threading.Lock()

    def run(self):
        last = False

        newRes = (int(STD_DIMENSIONS['720p'][0] / 2), int(STD_DIMENSIONS['720p'][1] / 2))

        while self.running:
            frame = self.camera.getFrame()

            if frame is None:
                continue

            if self.detectMotion:
                if self.motion and not last:
                    # Motion detected
                    last = True

                    send('Motion detected!\n-------------------------------\n' + str(
                        datetime.now().strftime("%m/%d/%Y %H-%M")), '9082093348')

                    # Begin recording and make dirs if they don't exist yet
                    if not os.path.exists(VIDEO_DIR + str(datetime.now().strftime('%m-%d-%Y'))):
                        os.makedirs(VIDEO_DIR + str(datetime.now().strftime('%m-%d-%Y')))
                    self.recordID = self.camera.startRec(str(datetime.now().strftime('%m-%d-%Y\\%H-%M-%S')) + '.avi')

                elif not self.motion and last:
                    # Motion stopped
                    last = False

                    # Cease recording
                    self.camera.stopRec(self.recordID)

                # Resize frame for quicker motion calc
                frame = cv2.resize(frame, newRes)

                # Ensure only detecting during desired hours
                hour = datetime.now().hour
                if OPERATION_START_TIME > OPERATION_END_TIME:
                    if OPERATION_END_TIME >= hour or hour >= OPERATION_START_TIME:
                        time.sleep(.1)
                        self.detectMotionFromFrame(frame)
                else:
                    if OPERATION_START_TIME <= hour <= OPERATION_END_TIME:
                        time.sleep(.1)
                        self.detectMotionFromFrame(frame)

            if self.showCam:
                cv2.imshow('Server: ' + self.internalIP, frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False
                    break

    def motionDetected(self):
        self.motionLock.acquire()

        motion = self.motion

        self.motionLock.release()

        return motion

    # Note: Assumes frame passed will be gray scale
    def detectMotionFromFrame(self, frame):

        # Blur the image to get pixel averages
        blurred = cv2.GaussianBlur(frame, (21, 21), 0)
        currentTime = time.time()

        # If staticBack hasn't been set yet or, the time to update has passed, update staticBack with current
        if self.staticBack is None or self.staticLastUpdateTime + STATIC_UPDATE_TIME <= currentTime:
            self.staticBack = blurred
            self.staticLastUpdateTime = currentTime
            return

        # If the allotted time since the last detected motion has passed, check for more motion
        if self.motionTime + MOTION_CHECK_DELAY <= currentTime:

            # Find pixel difference between static background image and current image
            diffFrame = cv2.absdiff(self.staticBack, blurred)

            # Filter the pixel difference by a given threshold
            thresh = cv2.threshold(diffFrame, THRESHHOLD_SENSITIVITY, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)

            self.threshFrame = thresh

            # Sum up the differences and log()
            threshSum = thresh.sum()
            if threshSum <= 0:
                threshSum = 1

            threshSum = log(threshSum, 10)
            logging.debug('Thresh sum: ' + str(threshSum))

            self.motionLock.acquire()

            # If the threshold's sum passes the set limit, motion is detected
            if threshSum > THRESHHOLD_SUM:
                logging.info('Motion detected! Time: ' + str(datetime.now().strftime("%m/%d/%Y %H:%M")))
                self.motion = True
                self.motionTime = currentTime
            else:
                self.motion = False

            self.motionLock.release()

    def reset(self):
        # Controls if the thread is functioning
        self.running = True

        # Control camera motion detection
        self.detectMotion = False  # Say if we should detect
        self.staticBack = None  # Assigning our staticBack to None
        self.staticLastUpdateTime = None  # Used to check time since last background comparision image update

        self.motion = False  # Flag for motion
        self.motionTime = 0  # Time since last motion detection, prevents motion detection spam
        self.threshFrame = None  # Visual representation of movement detection

        self.camera.reset()
