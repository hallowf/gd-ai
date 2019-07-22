import time, threading, sys
import keyboard
from selenium import webdriver
import selenium.webdriver.common.keys as Keys

from network.controller import CNNBot
from browser_controller import BController


# CIFAR10 best
# VGG not bad
# all others seem bad

if __name__ == '__main__':
    bot = CNNBot("trained_models/jd_CIFAR10_RMSprop.h5")
    is_paused = False
    try:
        while True:
            if not is_paused:
                if keyboard.is_pressed("q"):
                    raise KeyboardInterrupt
                if keyboard.is_pressed("t"):
                    is_paused = not is_paused
                bot.predict()
    except KeyboardInterrupt:
        del bot
        sys.stdout.write("Disconnecting\n")
        sys.exit(0)
