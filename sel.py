from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
#from pyvirtualdisplay import Display
import time
#display = Display(visible=0, size = (800,800))
#display.start()

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(chrome_options=chrome_options)
#driver.get("file:///bot/slime/index.html")
path = os.path.abspath(os.path.join("slime", "index.html"))
driver.get("file://" + path)
driver.find_element_by_class_name("clblHP").click()
