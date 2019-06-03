import time, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException


class BController(object):

    def __init__(self, version):
        self.driver_version = version
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-background-networking")
        self.chrome_options = chrome_options
        has_driver = self.test_driver()
        if has_driver:
            sys.stdout.write("Browser iniciado\n")

    def test_driver(self):
        print("d_version", self.driver_version)
        try:
            self.driver = webdriver.Chrome("drivers/%i" % (self.driver_version), options=self.chrome_options)
            self.driver.get("chrome://dino")
            time.sleep(2)
            print("found driver")
            return True
        except (Exception, SessionNotCreatedException) as e:
            print("d_version exception", self.driver_version)
            print(e)
            self.driver_version -= 1
            if self.driver_version < 70:
                sys.stdout.write("Erro de driver. Nenhuma versão compativel do chrome encontrada\n")
                return False
            else:
                self.test_driver()

    def get_driver(self):
        return self.driver
