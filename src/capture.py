import os
import cv2
from mss import mss
import numpy as np
import keyboard

class Recorder(object):

    def __init__(self, set=1,coords=(360,30,615,160)):
        if os.path.isfile("actions/set%s_actions.csv") or os.path.isdir("images/set%s" % set):
            set += 1
        self.actions = "actions/set%s_actions.csv" % set
        self.set = set
        top,left,width,height = coords
        self.top = top
        self.left = left
        self.width = width
        self.height = height

    def start(self):
        sct = mss()
        coords = {
            "top": self.top,
            "left": self.left,
            "width": self.width,
            "height": self.height,
        }
        with open(self.actions, "w") as csv:
            self.img_num = 0

            if not os.path.exists('./images/set%s' % (self.set)):
                os.mkdir('./images/set%s' % (self.set))

            while True:
                img = np.array(sct.grab(coords))
                # Crop dino
                img = img[::,75:615]

                # edge detection
                img = cv2.Canny(img, threshold1=100,threshold2=200)

                if keyboard.is_pressed("up arrow"):
                    cv2.imwrite("./images/set%s/frame_%s.jpg" % (self.set,self.img_num), img)
                    csv.write("1\n")
                    self.img_num+=1

                if keyboard.is_pressed("down arrow"):
                    cv2.imwrite("./images/set%s/frame_%s.jpg" % (self.set,self.img_num), img)
                    csv.write("2\n")
                    self.img_num+=1

                if keyboard.is_pressed("t"):
                    cv2.imwrite("./images/set%s/frame_%s.jpg" % (self.set,self.img_num), img)
                    csv.write("0\n")
                    self.img_num+=1

                # break the video feed
                if keyboard.is_pressed("q"):
                    csv.close()
                    cv2.destroyAllWindows()
                    break
