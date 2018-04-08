# Imports
import selenium
from pickle import dump,load
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import pyautogui
import os
import time
import json
import re
from env import *

if os.path.isfile('env.obj') and open('env.obj').read() == '':
    env = SlimeEnv()
    env.reset() 
else:
    env = load(open('env.obj', 'rb'))


# Constrain
constrain = lambda n, minn, maxn: max(min(maxn, n), minn)
#Get only numbers
def get_pos(string):
    pos_filter = re.compile(r'[^\d.]+')
    string = string.split(';')
    return (float(pos_filter.sub('', string[0])), float(pos_filter.sub('', string[1])))
def get_hang_percent(string):
    filt = re.compile(r'[^\d.]+')
    return float(filt.sub('',string))
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
end_path = '//*[@id="content"]/div/div[2]/div[2]/div[2]/div[1]/div/div/div/div[5]/div/div[3]/div'

# Open Webdriver
options = Options()
#options.add_argument("--headless")
driver = webdriver.Firefox(firefox_options=options)
print("Firefox Headless started")
path = os.path.abspath(os.path.join("slime", "index.html"))
driver.get("file://" + path)

w_down = ActionChains(driver).key_down(KEY_W)
a_down = ActionChains(driver).key_down(KEY_A)
s_down = ActionChains(driver).key_down(KEY_S)
d_down = ActionChains(driver).key_down(KEY_D)
w_up = ActionChains(driver).key_up(KEY_W)
a_up = ActionChains(driver).key_up(KEY_A)
s_up = ActionChains(driver).key_up(KEY_S)
d_up = ActionChains(driver).key_up(KEY_D)

for i in range(0,1001):
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
    comp_X = 0
    if i % 10 == 0:
        dump(env,open('env.obj', 'wb'))

    # GAME STARTS
    while True:
        end_game = driver.find_element_by_xpath(end_path)
        if int(end_game.text[3:5]) == 0 and int(end_game.text[-2:]) < 10:
            print("Game %d has ended" %i)
            break
        else:
            game_counter+=1
            action = env.action_space.sample()
            w_end = time.time() + (action[DURATION_W]/100) + 0.05
            a_end = time.time() + (action[DURATION_A]/100) + .5
            s_end = time.time() + (action[DURATION_S]/100) + .5
            d_end = time.time() + (action[DURATION_D]/100) + .5
            is_w = True
            is_a = True
            is_s = True
            is_d = True
            while True:
               # if action[KEY_A]:
               #     a_down.perform()
                if action[KEY_S]:
                    s_down.perform()
                if action[KEY_W]:
                    w_down.perform()
                if action[KEY_D]:
                    d_down.perform()

                if time.time() > w_end:
                    w_up.perform()
                    is_w = False
               # if time.time() > a_end:
               #     a_up.perform()
               #     is_a = False
                if time.time() > s_end:
                    a_up.perform()
                    is_s = False
                if time.time() > d_end:
                    d_up.perform()
                    is_d = False

                if not is_w and not is_s and not is_d:
                    break
            
            player = driver.find_elements_by_class_name(player_selector)
            ball = driver.find_element_by_class_name(ball_selector)
            messi_pos = player[0].get_attribute("style")
            comp_pos = player[1].get_attribute("style")
            prev_ball_X = ball_X
            prev_messi_X = messi_X
            prev_comp_X = comp_X
            ball_pos = ball.get_attribute("style")
            ball_X = get_pos(ball_pos)[0]
            ball_Y = get_pos(ball_pos)[1]
            messi_X = get_pos(messi_pos)[0]
            messi_Y = get_pos(messi_pos)[1]
            comp_X = get_pos(comp_pos)[0]
            comp_Y = get_pos(comp_pos)[1]
            ball_vel = constrain((ball_X - prev_ball_X), -30, 30)
            messi_vel = constrain((messi_X - prev_messi_X), -10, 10)
            comp_vel = constrain((comp_X - prev_comp_X), -10, 10)
            hanging = driver.find_element_by_class_name('iqiixv').get_attribute("style")
            is_hanging = get_hang_percent(hanging) < 2.0
            observation = {
                PLAYER: {
                    POSITION_X: messi_X,
                    POSITION_Y: messi_Y,
                    VELOCITY_X: messi_vel,
                    HANGING: is_hanging
                }, 
                OPPONENT: {
                    POSITION_X: comp_X,
                    POSITION_Y: comp_Y,
                    VELOCITY_X: comp_vel 
                }, 
                BALL: {
                    POSITION_X: ball_X,
                    POSITION_Y: ball_Y,
                    VELOCITY_X: ball_vel
                }
            }
            env.step(action, observation)

    print(game_counter) 
    driver.refresh()
    time.sleep(1)
driver.close()
