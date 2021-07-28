import gym_maze
import numpy as np
import gym

env = gym.make('maze-v0')
for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        # testing
        action = np.array([1,0])
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()