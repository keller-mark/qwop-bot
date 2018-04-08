import gym
from env import *

env = SlimeEnv()
env.reset()
# existing while loop
  action = env.action_space.sample()
  # TODO take action in running game
  # action = binary whether button pressed, with duration (range)
   observation = {
            PLAYER: {
                POSITION_X: 0,
                POSITION_Y: 0,
                VELOCITY_X: 0
            }, 
            OPPONENT: {
                POSITION_X: 0,
                POSITION_Y: 0,
                VELOCITY_X: 0 
            }, 
            BALL: {
                POSITION_X: 0,
                POSITION_Y: 0,
                VELOCITY_X: 0
            }
        }
  env.step(action, observation) # take a random action
