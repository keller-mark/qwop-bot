from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
driver.get("file://index.html")
driver.findElementByClassName("clblHP").click();
