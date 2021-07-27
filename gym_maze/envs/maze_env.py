import gym
from gym import error, spaces, utils
from gym.utils import seeding
import socket
import time
import numpy as np
import cv2
import mss

# TODO: find way so that i can send grayscale data right from unity to python without using opencv
# idea = use texture 2D and get pixel method
# use coroutine to process the frame by frame
# setting timescale to 0 will pause the game
class MazeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # c# and python communication
        host, port = "127.0.0.1", 25001
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        #setting some gym variables

        self.viewer = None
        self.state = None
        self.step_that_can_be_taken = 1000
        self.current_step = 0
        self.penalty_for_every_steps = 0.01
        self.observation_space = spaces.Box(low=0, high=255, shape=(84, 84, 1))
        # first one is rotation and second is translation
        self.action_space = spaces.Box(low=-1, high=1, shape=(2, 1, 1))
        self.done = False
        self.episodes = 0

        self.reset()


    def step(self, action):
        # TODO: do action

        # returning bunch of stuff
        self.current_step +=1
        observation = self.get_observation()
        done = self.get_done()
        reward = self.get_reward()
        return observation, reward, done, {}

    def reset(self):
        self.current_step = 0
        self.done = False
        # prob some script that gives unity application to reset
        message = ""
        self.sock.sendall(message.encode("UTF-8"))


    def render(self, mode='human'):
        pass

    def close(self):
        # prob some script that gives unity application to stop/close
        message = ""
        self.sock.sendall(message.encode("UTF-8"))

    def get_reward(self):
        total_reward = 0
        total_reward -= self.penalty_for_every_steps
        if self.done:
            total_reward += 1
        return total_reward

    def get_done(self):
        received_data = self.sock.recv(1)
        if self.current_step >= self.step_that_can_be_taken or received_data == 0x01:
            self.done = True
            return True
        elif received_data == 0x00:
            self.done = False
            return False
        else:
            print("Error on get_done")

    def get_observation(self):
        screen = np.array(mss.mss().grab({'top': 540 - (42 - 14), 'left': 960 - 42, 'width': 84, 'height': 84}))
        screen = cv2.cvtColor(screen, cv2.cv2.COLOR_BGR2GRAY, 0)
        cv2.imshow('window', screen)
        return screen
