import gym
from gym import error, spaces, utils
from gym.utils import seeding
import socket
import time
import numpy as np
import cv2
import mss
import struct


# TODO: find way so that i can send grayscale data right from unity to python without using opencv
# idea = use texture 2D and get pixel method
# use coroutine to process the frame by frame
# setting timescale to 0 will pause the game
# TODO: use unity event system for handling movement and input data
class MazeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        # c# and python communication
        host, port = "127.0.0.1", 25002
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        # setting some gym variables
        self.step_that_can_be_taken = 1000
        self.current_step = 0
        self.penalty_for_every_steps = 0.01
        self.observation_space = spaces.Box(low=0, high=255, shape=(84, 84,))
        # first one is rotation and second is translation
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,))
        self.done = False
        self.episodes = 0

    def step(self, action):
        self.do_action(action)
        # returning bunch of stuff
        self.current_step += 1
        observation = self.get_observation()
        x_coor, y_coor = self.receive()
        reward = self.get_reward()
        return observation, reward, self.done, {x_coor, y_coor}

    def reset(self):
        self.current_step = 0
        self.done = False
        self.episodes += 1
        # send signal to unity to reset
        action_to_send = bytearray(b'\x00' * 8 + b'\x01')
        self.sock.sendall(action_to_send)
        return self.get_observation()

    def render(self, mode='human'):
        # render is handled on the unity side
        pass

    def close(self):
        # prob some script that gives unity application to stop/close or just manually closing
        print("Application Closed.")
        self.sock.close()
        raise SystemExit(0)

    def get_reward(self):
        total_reward = 0
        total_reward -= self.penalty_for_every_steps
        if self.done:
            total_reward += 1
        return total_reward

    def receive(self):
        # if it is too fast, then unity can't handle it
        time.sleep(2)
        received_data = bytearray(self.sock.recv(9))
        if self.current_step >= self.step_that_can_be_taken or received_data[0] == 0x01:
            self.done = True
        elif received_data[0] == 0x00:
            self.done = False
        else:
            print("Error on get_done")
        x_coordinate = struct.unpack('f', received_data[1:5])
        y_coordinate = struct.unpack('f', received_data[5:9])
        print(x_coordinate)
        return x_coordinate, y_coordinate

    def get_observation(self):
        screen = np.array(mss.mss().grab({'top': 540 - (42 - 14), 'left': 960 - 42, 'width': 84, 'height': 84}))
        screen = cv2.cvtColor(screen, cv2.cv2.COLOR_BGR2GRAY, 0)
        cv2.imshow('window', screen)
        return screen

    def do_action(self, action):
        action_to_send = bytearray(struct.pack('f',action[0])) + bytearray(struct.pack('f',action[1]) + b'\x00')
        self.sock.sendall(action_to_send)
