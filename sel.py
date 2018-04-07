from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import os
import time

SP = "clblHP"
GO = "wbc-btn-go"
ch_team = "cTXYfN"
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(chrome_options=chrome_options)
path = os.path.abspath(os.path.join("slime", "index.html"))
driver.get("file://" + path)
driver.find_element_by_class_name(SP).click()
driver.find_element_by_class_name(GO).click()
for i in range(0,13):
    driver.find_element_by_class_name(ch_team).click()
driver.find_element_by_class_name(GO).click()
driver.find_element_by_class_name(GO).click()
time.sleep(0.01)
pyautogui.keyDown('d')
time.sleep(1)
pyautogui.keyUp('d')
time.sleep(1)

driver.quit()
