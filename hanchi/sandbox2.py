from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time

#"./chromedriver"

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver.exe")
browser = webdriver.Chrome(executable_path = DRIVER_BIN)



browser.get("https://en.wiktionary.org/wiki/Wiktionary:Main_Page")
time.sleep(10)
print ("Driver chrome Initialized")


browser.quit()