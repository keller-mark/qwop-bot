import gym
from gym import spaces
from gym.utils import seeding
import numpy as np

POSITION_X = 'position_x'
POSITION_Y = 'position_y'
VELOCITY_X = 'velocity_x'
PLAYER = 'player'
OPPONENT = 'opponent'
BALL = 'ball'
HANGING = 'hanging'

KEY_W = 'w'
DURATION_W = 'duration_w'
KEY_A = 'a'
DURATION_A = 'duration_a'
KEY_S = 's'
DURATION_S = 'duration_s'
KEY_D = 'd'
DURATION_D = 'duration_d'


class SlimeEnv(gym.Env):
    """
    Based on https://github.com/openai/gym/blob/master/gym/envs/toy_text/guessing_game.py

    The object of the game is to score more goals than your opponent
    within 200 time steps

    The observation contains: (
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

    Future reward changes:
        - amount of velocity
        - 
    
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
            PLAYER: spaces.Dict({
                POSITION_X: spaces.Box(low=35, high=665, shape=()),
                POSITION_Y: spaces.Box(low=245, high=150, shape=()),
                VELOCITY_X: spaces.Box(low=-30, high=30, shape=()),
                HANGING: spaces.Discrete(2)
            }), 
            OPPONENT: spaces.Dict({
                POSITION_X: spaces.Box(low=35, high=665, shape=()),
                POSITION_Y: spaces.Box(low=245, high=150, shape=()),
                VELOCITY_X: spaces.Box(low=-30, high=30, shape=()) 
            }), 
            BALL: spaces.Dict({
                POSITION_X: spaces.Box(low=10, high=689.5, shape=()),
                POSITION_Y: spaces.Box(low=280, high=100, shape=()),
                VELOCITY_X: spaces.Box(low=-30, high=30, shape=())
            })
        })

        # TODO: add duration for each key
        self.action_space = spaces.Dict({
            KEY_A: spaces.Discrete(2),
            KEY_S: spaces.Discrete(2),
            KEY_W: spaces.Discrete(2),
            KEY_D: spaces.Discrete(2),
            DURATION_A: spaces.Discrete(100),
            DURATION_S: spaces.Discrete(100),
            DURATION_D: spaces.Discrete(100),
            DURATION_W: spaces.Discrete(100)
        })

        self.seed()
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action, observation):
        assert self.action_space.contains(action)

        reward = 0
        done = False

        reward, done = self.compute_reward(observation)

        self.frame_count += 1
        if self.frame_count >= self.frame_max:
            # override done if >= 200 frames have passed
            done = True

        return observation, reward, done, { "info": None }

    def reset(self):
        self.guess_count = 0
    def get_goal_state(self, observation):
        messi_goal = (30, 215)
        comp_goal = (670, 215)
        if (observation[BALL][POSITION_X] > comp_goal[0] and 
                observation[BALL][POSITION_Y] > comp_goal[1]):
            return 1    #AI scores
        elif (observation[BALL][POSITION_X] < messi_goal[0] and 
                observation[BALL][POSITION_Y] > messi_goal[1]):
            return -1   #Comp scores
        else:
            return 0    #No goal

    def is_kicking(self, observation):
        messi_x = observation[PLAYER][POSITION_X]
        messi_y = observation[PLAYER][POSITION_Y]
        ball_x = observation[BALL][POSITION_X]
        ball_y = observation[BALL][POSITION_Y]
        colliding = False
        if (ball_x < messi_x + 40 and ball_x > messi_x - 40 and ball_y > messi_y - 5 and 
                ball_y < messi_y + 40):
            colliding = True
        return colliding and (observation[PLAYER][VELOCITY_X] > 0)

    def compute_reward(self, observation):
        # see above for reward details
        """
        -2 reward if player kicks ball away from opponent goal
        -1 reward if player moving away from ball (distance to ball increasing)
        1 reward if player moving toward ball (distance to ball decreasing)
        2 reward if player kicks ball toward opponent goal
        """
        # TODO
        # set reward, done
        reward = 0
        goal_state = self.get_goal_state(observation)
        
        # calculate reward based on state
        ball_left_of_player = observation[BALL][POSITION_X] < observation[PLAYER][POSITION_X]

        if ball_left_of_player:
            if observation[PLAYER][VELOCITY_X] < 0:
                reward += 3
            else:
                reward += -2
        else:
            if observation[PLAYER][VELOCITY_X] > 0:
                reward += 3
            else:
                reward += -2
        if self.is_kicking(observation):
            reward += 5
        if observation[PLAYER][HANGING]:
            print("HANGING---------------")
            reward += -2

        reward += 10*goal_state
        print("REWARD= " + str(reward))
        return reward, goal_state
        

