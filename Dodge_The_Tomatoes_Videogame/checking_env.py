from game_cus_gym_env_v2 import *

env = Game_env()
episodes = 50
for episode in range(episodes):
    obs = env.reset()
    while True:
        env.render()
        random_action = env.action_space.sample()
        obs,reward,truncated,done,info = env.step(random_action)
        if env.done: 
            print('reward',reward)
            break