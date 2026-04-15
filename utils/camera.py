import cv2
from config import CAMERA_ID

def get_camera():

    cap = cv2.VideoCapture(CAMERA_ID)

    return cap