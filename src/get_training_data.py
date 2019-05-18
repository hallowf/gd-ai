import time, threading, sys
import selenium.webdriver.common.keys as keys

from browser_controller import BController
from capture import Recorder

class Watcher(object):

    def __init__(self, driver="75"):
        self.capturing = False
        self.driver_version = driver
        self.driver_connected = False
        browser = BController()
        self.driver = browser.get_driver()

    def countdown(self,t):
        for i in range(t,0,-1):
            sys.stdout.write(str(i)+"\n")
            time.sleep(1)

    def start(self):
        sys.stdout.write("A iniciar\n")
        self.countdown(3)
        page = self.driver.find_element_by_id("t")
        page.send_keys(u"\ue00d")
        Recorder().start()



t = Watcher("74")
t.start()
