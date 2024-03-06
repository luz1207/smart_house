import cv2

class VideoCamera(object):
    def __init__(self):
    # 通过opencv获取实时视频流
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

cap = VideoCamera()