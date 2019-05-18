import time, threading
from selenium import webdriver
import selenium.webdriver.common.keys as Keys

from network.controller import CNNBot
from browser_controller import BController



if __name__ == '__main__':
    bot = CNNBot()
    try:
        while True:
            bot.predict()
    except KeyboardInterruption:
        sys.stdout.write("Disconnecting\n")
