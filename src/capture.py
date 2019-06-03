import os, threading, time, random
import cv2
from mss import mss
import numpy as np
import keyboard

class Recorder(object):

    def __init__(self, identifier, counter, split_at,coords=(360,30,615,160)):
        print("Starting Recorder")
        self.counter = int(counter)
        self.do_split = False
        self.split_at = 2000
        if split_at != None:
            self.do_split = True
            self.split_at = int(split_at)
        self.filename = None
        self.identifier = identifier
        top,left,width,height = coords
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.training_data = []
        self.is_running = False
        self.paused = False
        self.exit_save = False
        keyboard.add_hotkey("p", self.switcher, args=["pause"])
        keyboard.add_hotkey("q", self.switcher, args=["quit"])
        print("Recorder instantiated")


    def __del__(self):
        while (not self.exit_save and self.thread_handle != None):
            if not self.exit_save:
                self.exit_save = True
                self.do_save()
            if self.thread_handle != None:
                self.thread_handle.join()
                del self.thread_handle
        print("Recorder removed")

    def do_save(self):
        if len(self.training_data) > 100:
            trained_data = self.training_data
            self.filename = "training/training_data_%s%s.npy" % (self.identifier,self.counter)
            np.save(self.filename, trained_data)
            # empty the array
            self.training_data.clear()
            self.counter += 1
        else:
            print("Not enough data to save")

    def monitor(self):
        while self.is_running:
            if len(self.training_data) % 500 == 0:
                print("Current lenght: %s" % len(self.training_data))
                time.sleep(2)
                if len(self.training_data) >= self.split_at:
                    self.do_save()

    def switcher(self, action):
        if action == "pause":
            s = "Pausing" if not self.paused else "Resuming"
            print(s)
            self.paused = not self.paused
            print("Blocked for 2 seconds")
            time.sleep(2)
        elif action == "quit":
            self.is_running = False

    def start(self):
        print("Monitor started")
        self.is_running = True
        choices = [1,2,3,4,5,6]
        # forward, jump, duck
        # action = [0,0,0]
        self.thread_handle = threading.Thread(target=self.monitor, args=())
        self.thread_handle.start()
        sct = mss()
        coords = {
            "top": self.top,
            "left": self.left,
            "width": self.width,
            "height": self.height,
        }
        while self.is_running:
            if not self.paused:
                img = np.array(sct.grab(coords))
                # Crop dino
                img = img[::,75:615]
                # edge detection
                img = cv2.Canny(img, threshold1=100,threshold2=200)
                if keyboard.is_pressed("up arrow"):
                    self.training_data.append([img, [0,1,0]])
                elif keyboard.is_pressed("down arrow"):
                    self.training_data.append([img, [0,0,1]])
                elif random.choice(choices) == 3:
                    self.training_data.append([img, [1,0,0]])
