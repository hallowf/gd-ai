import time, sys, os
from keras.models import load_model
import selenium
import keyboard
from mss import mss
import cv2
import numpy as np
from browser_controller import BController

class CNNBot(object):

    def __init__(self, set_name="testing_data.h5", coords=(360,30,615,160)):
        top,left,width,height = coords
        self.session_driver = None
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.trained_set  = "trained_models"
        if not os.path.isfile(set_name):
            sys.stdout.write("Missing trained data\n")
            sys.exit(1)
        self.model = load_model(set_name)
        self.start = time.time()
        self.b_controller = BController(75)
        self.session_driver = self.b_controller.get_driver()
        self.driver = self.session_driver.find_element_by_id("t")
        # start game
        self.driver.send_keys(u'\ue013')

    def __del__(self):
        if self.session_driver != None:
            sys.stdout.write("Closing browser session\n")
            self.session_driver.quit()
            del self.b_controller

    def predict(self):
        sct = mss()
        coords = {
            "top": self.top,
            "left": self.left,
            "width": self.width,
            "height": self.height,
        }

        # image capture
        img = np.array(sct.grab(coords))

        # cropping, edge detection, resizing to fit expected model input
        img = img[::,75:615]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.Canny(img, threshold1=100, threshold2=200)
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
        img = img[np.newaxis, :, :, np.newaxis]
        # img = np.array(img)

        # forward, jump, duck
        # [0,0,0]

        # model prediction
        y_prob = self.model.predict(img / 255)
        print(y_prob)
        prediction = y_prob.argmax(axis=-1)
        # print(prediction)

        if int(prediction) == 1:
            # jump
            sys.stdout.write("jump\n")
            # time.sleep(0.1)
            keyboard.press("up arrow")
            time.sleep(0.09)
            keyboard.release("up arrow")
        elif int(prediction) == 0:
            # do nothing
            # sys.stdout.write("walk\n")
            pass
        elif int(prediction) == 2:
            # duck
            sys.stdout.write("duck\n")
            keyboard.press("down arrow")
            time.sleep(0.25)
            keyboard.release("down arrow")
