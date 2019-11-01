# Author: Rodrigo Graca

from enum import Enum
from cv2 import VideoWriter_fourcc

# Generate the windows binary
"""pyinstaller.exe -F -w -i camera.ico -n "Security Cam" Server.py"""

# Define encryption settings (Bytes)
RSA_KEY_LENGTH = 2048
AES_KEY_LENGTH = 32

# Define app settings
WINDOW_SIZE = (450, 500)

# Define how often the output is reloaded
OUTPUT_REFRESH_RATE = .5

# Public IP of common relay server
SERVER = 'zenov.ddns.net'

VIDEO_TYPE = {
    'avi': VideoWriter_fourcc(*'mp4v'),
    'mp4': VideoWriter_fourcc(*'mp4v'),
}

# Standard Video Dimensions Sizes
STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

# ------Motion detection settings------

STATIC_UPDATE_TIME = 60 * 5  # Seconds
MOTION_CHECK_DELAY = 5  # Seconds
THRESHHOLD_SUM = 7  # Log of threshSum value, 6 pretty decent motion detect
THRESHHOLD_SENSITIVITY = 35  # How sensitive the motion detection is to changes

# Current directory to base from
WORKING_DIR = ''

# Directory to store videos
VIDEO_DIR = WORKING_DIR + 'records\\'

# Time to allow for the camera to stabilize
CAMERA_INIT_TIME = 2

# Enable/disable chime when recording
CHIME_ENABLED = True

# Define times to start motion detection
OPERATION_START_TIME = 22
OPERATION_END_TIME = 8

# ------Motion detection settings end------

SEND_MESSAGE = False


# Provide commands to communicate between threads
class DisplayCommands(Enum):
    clearOutput = 1


class SocketKind(Enum):
    Client = 0
    Server = 1


class SocketCommands:
    DISPLAY = '0'
    FILE_SEND = '1'
