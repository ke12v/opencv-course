import sys
sys.path.insert(0, r'C:\Users\Technical-10\AppData\Roaming\Python\Python312\site-packages')
import cv2 as cv
import numpy as np
class Dummy:
    def __init__(self):
        self.frame = np.zeros((10,10,3), dtype='uint8')
    def read(self):
        return True, self.frame
    def release(self):
        pass
    def isOpened(self):
        return True
cv.VideoCapture = lambda *args, **kwargs: Dummy()
cap = cv.VideoCapture('x')
ok, frame = cap.read()
print(ok, type(frame), frame.shape)
