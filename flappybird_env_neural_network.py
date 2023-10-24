import gym
from gym import spaces
import FlappyBird
import numpy as np



class FlappyBirdEnv(gym.Env):
    def __init__(self):
        super(FlappyBirdEnv, self).__init__()
        self.flappy_bird = FlappyBird.Game()
        self.action_space = spaces.Discrete(2)  # Sauter ou ne pas sauter
        self.observation_space = gym.spaces.Box(low=0, high=1000, shape=(3,), dtype=np.float32)

    def reset(self):
        return(self.flappy_bird.reset())
    
    def step(self, action):
        return(self.flappy_bird.step(action))
        
    def render(self, mode='human'):
        self.flappy_bird.render()

    def get_state(self):
        return(self.flappy_bird.get_state())


# Test de l'environnement en envoyant des actions au hasard.
if __name__=='__main__':
    env = FlappyBirdEnv()
    for i_episode in range(5):  # pour 5 épisodes
        observation = env.reset()
        done = False
        while not done:
            env.render()
            action = env.action_space.sample()  # action au hasard
            observation, reward, done, info = env.step(action)
    env.close()

