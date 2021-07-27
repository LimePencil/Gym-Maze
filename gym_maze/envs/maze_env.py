import gym
from gym import error, spaces, utils
from gym.utils import seeding


class MazeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.viewer = None
        self.state = None
        self.frames_at_once = 4
        self.step_that_can_be_taken = 1000
        self.observation_space = spaces.Box(low=0, high=255, shape=(84, 84, self.number_of_frames_at_once))
        # first one is rotation and second is translation
        self.action_space = spaces.Box(low=-1, high=1, shape=(2, 1, 1))
        self.done = False
        self.episodes = 0


    def step(self, action):
        done = self._get_done()
        reward = self._get_reward()

        return observation, reward, done, {}

    def reset(self):
        ...

    def render(self, mode='human'):
        ...

    def close(self):
        ...

    def _get_reward(self):
        if self.done:
            return 1
        else:
            return 0


env = MazeEnv()
print(env.action_space.high)
