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
    bot = CNNBot("CIFAR10_RMSprop_set1.h5")
    try:
        while True:
            if keyboard.is_pressed("q"):
                raise KeyboardInterrupt
            bot.predict()
    except KeyboardInterrupt:
        del bot
        sys.stdout.write("Disconnecting\n")
        sys.exit(0)
