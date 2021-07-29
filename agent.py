import time

import gym_maze
import numpy as np
import gym
import keyboard

env = gym.make('maze-v0')
for i_episode in range(1):
    observation = env.reset()
    for t in range(1000):
        # testing
        arr = np.array((0,0))
        if keyboard.is_pressed('q'):
            arr = np.array((1,0))
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()