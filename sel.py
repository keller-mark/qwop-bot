# Imports
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import pyautogui
import os
import time
import json
import re

# Constrain
constrain = lambda n, minn, maxn: max(min(maxn, n), minn)
#Get only numbers
def get_pos(string):
    pos_filter = re.compile(r'[^\d.]+')
    string = string.split(';')
    return (float(pos_filter.sub('', string[0])), float(pos_filter.sub('', string[1])))

# Key Constants
RIGHT = 'd'
UP = 'w'
LEFT = 'a'
# Class constants
SP = "clblHP"
GO = "wbc-btn-go"
CH_TEAM = "cTXYfN"

# Get elements
elements = json.load(open('slime_elements.json'))
player_selector = elements['player']
ball_selector = elements['ball']
# Open Webdriver
options = Options()
#options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)
print("Firefox Headless started")
path = os.path.abspath(os.path.join("slime", "index.html"))
driver.get("file://" + path)
for i in range(0,3):
    print("Game %d started" %i)
    # Enter SP game as team USA
    driver.find_element_by_class_name(SP).click()
    go_button = driver.find_element_by_class_name(GO)
    go_button.click()
    #team_select = driver.find_element_by_class_name(CH_TEAM)
    #for i in range(0,13):
    #    team_select.click()
    go_button = driver.find_element_by_class_name(GO)
    go_button.click()
    go_button = driver.find_element_by_class_name(GO)
    go_button.click()
    time.sleep(0.01)
    game_counter = 0
    ball_X = 0
    messi_X = 0
    # GAME STARTS
    while True:
        try:
            end_game = driver.find_element_by_class_name(elements['end-game'])
            print("Game %d has ended" %i)
            break
        except :
            game_counter+=1
            player = driver.find_elements_by_class_name(player_selector)
            ball = driver.find_element_by_class_name(ball_selector)
            messi_pos = player[0].get_attribute("style")
            comp_pos = player[1].get_attribute("style")
            prev_ball_X = ball_X
            prev_messi_X = messi_X
            ball_pos = ball.get_attribute("style")
            ball_X = get_pos(ball_pos)[0]
            ball_Y = get_pos(ball_pos)[1]
            messi_X = get_pos(messi_pos)[0]
            messi_Y = get_pos(messi_pos)[1]
            comp_X = get_pos(comp_pos)[0]
            comp_Y = get_pos(comp_pos)[1]
            '''
            print("Game %d Running" %i)
            print("Messi: "+ str(get_pos(messi_pos)))
            print("Computer: " + str(get_pos(comp_pos)))
            print("Ball: " + str(get_pos(ball_pos)))
            '''
            ball_vel = constrain((ball_X - prev_ball_X), -30, 30)
            messi_vel = constrain((messi_X - prev_messi_X), -10, 10)
            print(ball_vel)
            
    driver.refresh()
    time.sleep(1)
driver.close()
