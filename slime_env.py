import gym
from gym import spaces
from gym.utils import seeding
import numpy as np


class SlimeEnv(gym.Env):
    """

    Based on https://github.com/openai/gym/blob/master/gym/envs/toy_text/guessing_game.py

    The object of the game is to score more goals than your opponent
    within 200 time steps

    The observation is a tuple of: (
        the player's current position,
        the player's current velocity,
        the opponent's current position,
        the opponent's current velocity,
        the ball's current position,
        the ball's current velocity
    )
    
    The rewards are:
    -2 reward if player kicks ball away from opponent goal
    -1 reward if player moving away from ball (distance to ball increasing)
    1 reward if player moving toward ball (distance to ball decreasing)
    2 reward if player kicks ball toward opponent goal
    
    The episode terminates after the agent has scored a goal or
    200 steps have been taken
    
    The agent will need to use a memory of previously submitted actions and observations
    in order to efficiently explore the available actions
    
    The purpose is to have agents optimise their exploration parameters (e.g. how far to
    explore from previous actions) based on previous experience. Because the goal changes
    each episode a state-value or action-value function isn't able to provide any additional
    benefit apart from being able to tell whether to increase or decrease the next guess.
    The perfect agent would likely learn the bounds of the action space (without referring
    to them explicitly) and then follow binary tree style exploration towards to goal number
    """
    def __init__(self):

        self.frame_max = 200
        self.frame_count = 0

        self.observation_space = spaces.Dict({
            "player": spaces.Dict({
                'position': spaces.Box(low=0, high=100, shape=()),
                'velocity': spaces.Box(low=-1, high=1, shape=())
            }), 
            "opponent": spaces.Dict({
                'position': spaces.Box(low=0, high=100, shape=()),
                'velocity': spaces.Box(low=-1, high=1, shape=()) 
            }), 
            "ball": spaces.Dict({
                'position': spaces.Box(low=0, high=100, shape=()),
                'velocity': spaces.Box(low=-1, high=1, shape=())
            })
        })

        self.action_space = spaces.Dict({
            "w": spaces.Discrete(2),
            "s": spaces.Discrete(2),
            "a": spaces.Discrete(2),
            "d": spaces.Discrete(2)
        })

        self.seed()
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action)

        # Get an observation by pressing the keys specified in action
        self.observation = self.observe_action(action)

        reward = 0
        done = False

        reward, done = self.compute_reward(observation)

        self.frame_count += 1
        if self.frame_count >= self.frame_max:
            # override done if >= 200 frames have passed
            done = True

        return self.observation, reward, done #, {"number": self.number, "guesses": self.guess_count}

    def reset(self):
        self.guess_count = 0