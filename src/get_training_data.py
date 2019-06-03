import time, threading, sys, argparse
import keyboard
import selenium.webdriver.common.keys as keys

from browser_controller import BController
from capture import Recorder

class Watcher(object):

    def __init__(self, identifier, counter, split_at, *args, **kwargs):
        self.identifier = identifier
        self.counter = int(counter)
        self.split_at = int(split_at)
        self.driver_version = int(kwargs.get("driver", 74))
        self.driver = BController(self.driver_version).get_driver()
        self.monitor = Recorder(self.identifier, self.counter, self.split_at)
        self.capturing = False

    def __del__(self):
        if self.monitor != None:
            del self.monitor
        if self.driver != None:
            del self.driver

    def countdown(self,t):
        for i in range(t,0,-1):
            sys.stdout.write(str(i)+"\n")
            time.sleep(1)

    def start(self):
        sys.stdout.write("A iniciar\n")
        self.countdown(5)
        page = self.driver.find_element_by_id("t")
        page.send_keys(u"\ue00d")
        self.monitor.start()




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Capture training data, press ctrl+q to stop recording')
    parser.add_argument("identifier", type=str, help='An identifier for training data file')
    parser.add_argument("--r", "--resume", type=int, help="Number of file name to write to")
    parser.add_argument("--s", "--split-at", type=int,
    help="Number that defines max len for the data, whenever this is reached the file is saved and a new one is created")
    args = parser.parse_args()
    counter = args.r or 0
    split_at = args.s or 3000
    try:
        w = Watcher(args.identifier, counter, split_at)
        w.start()
    except Exception as e:
        print(e)
        raise
