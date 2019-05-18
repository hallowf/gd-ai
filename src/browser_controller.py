import time, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException


class BController(object):

    def __init__(self, version="75"):
        self.driver_version = version
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-background-networking")
        self.chrome_options = chrome_options
        self.test_driver()
        if not self.driver_connected:
            sys.stdout.write("Erro de driver. Nenhuma versão compativel do chrome encontrada\n")
            sys.exit(1)
        else:
            sys.stdout.write("Browser iniciado\n")

    def test_driver(self):
        try:
            self.driver = webdriver.Chrome("drivers/%s" % (self.driver_version), options=self.chrome_options)
            time.sleep(2)
            self.driver.get("chrome://dino")
            self.driver_connected = True
        except (Exception, SessionNotCreatedException) as e:
            self.driver = None
            self.driver_version = "74" if self.driver_version == "75" else "73"
            if self.driver_version > "75" or self.driver_version < "73":
                return False
            self.test_driver()

    def get_driver(self):
        return self.driver
