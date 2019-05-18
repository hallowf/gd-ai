import time, threading
from selenium import webdriver
import selenium.webdriver.common.keys as Keys

from network.controller import CNNBot
from browser_controller import BController


# CIFAR10 best
# VGG not bad
# all others seem bad

if __name__ == '__main__':
    bot = CNNBot("CIFAR10_RMSprop_set3.h5")
    try:
        while True:
            bot.predict()
    except KeyboardInterrupt:
        sys.stdout.write("Disconnecting\n")
