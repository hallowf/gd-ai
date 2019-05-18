import time, sys
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
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        if not os.path.isfile(set_name):
            sys.stdout.write("Missing trained data\n")
            sys.exit(1)
        self.model = load_model(set_name)
        self.start = time.time()
        driver = BController().get_driver()
        self.driver = driver.find_element_by_id("t")
        # start game
        self.driver.send_keys(u'\ue013')

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
        img = np.array(img)

        # model prediction
        y_prob = self.model.predict(img)
        prediction = y_prob.argmax(axis=-1)

        if keyboard.is_pressed("q"):
            sys.exit(0)

        sys.stdout.flush()
        if int(prediction) == 1:
            # jump
            sys.stdout.write("jump\n")
            keyboard.press("up arrow")
            time.sleep(0.2)
            keyboard.release("up arrow")
            time.sleep(0.2)
        elif int(prediction) == 0:
            # do nothing
            sys.stdout.write("walk\n")
            pass
        elif int(prediction) == 2:
            # duck
            sys.stdout.write("duck\n")
            keyboard.press("down arrow")
            time.sleep(0.2)
            keyboard.release("down arrow")
            time.sleep(0.2)
