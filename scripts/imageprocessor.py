#! /usr/bin/env python
from std_msgs.msg import Int32
import cv2 as cv
import math
import numpy as np
import rospy

class ImageProcessor():
    def __init__(self):
        self.dose = 0
        rospy.init_node('cv', anonymous=True)
        rospy.Subscriber("/dose", Int32, self.set_dose)
        cv.namedWindow("camera", 1)
        #capture = cv.VideoCapture("http://10.230.16.219:8080/video");
        self.capture = cv.VideoCapture(0);

    def __del__(self):
        cv.destroyWindow("camera")

    def set_dose(self, msg):
        self.dose = msg.data

    def tick(self, t):
        i = t
        result, img = self.capture.read()
        # wielowidzenie
        s = (int(30*np.sin(0.01*i) + 17*np.sin(0.03*i+0.5)))
        s = int(s*self.dose/4.0)
        img_shifted = np.concatenate([img[:, s:, :], img[:, :s, :]], 1)
        img = cv.addWeighted(img, 0.6, img_shifted, 0.4, 0)
        # rozmywanie
        s = abs(int(15*np.cos(0.01*i) + 3*np.sin(0.08*i+2.5)))
        s = abs(int(s*self.dose/4.0))
        s = 2*s+1
        img = cv.GaussianBlur(img, (s,s), 0)
        # plywanie
        s = abs(int(20*np.sin(0.01*i)))
        s = abs(int(s*self.dose/4.0))
        x = int(s*np.sin(0.03*i))
        y = int(s*np.cos(0.03*i))
        img = np.concatenate([img[x:, :, :], img[:x, :, :]], 0)
        img = np.concatenate([img[:, y:, :], img[:, :y, :]], 1)
        # zawezenie pola widzenia
        w = img.shape[1]
        h = img.shape[0]
        s = (4-self.dose)/2.0
        x, y = np.meshgrid(np.linspace(-1, 1, w), np.linspace(-1, 1, h))
        g = np.abs(np.exp(-((x**2 + y**2)/s)))
        g = np.where(g > 1, np.ones_like(g), g)
        img = (img * g[:, :, np.newaxis])/255
        cv.imshow("camera", img[20:-20, 20:-20, :])

    def run(self):
        rate = rospy.Rate(100)
        t = 0
        while not rospy.is_shutdown():
            if cv.waitKey(10) == 27:
                break
            t += 1
            self.tick(t)
            rate.sleep()

if __name__ == '__main__':
    ip = ImageProcessor()
    ip.run()
