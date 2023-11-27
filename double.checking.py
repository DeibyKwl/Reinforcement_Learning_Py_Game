from game_cus_gym_env import *



env = Game_env()
episodes = 50
for episode in range(episodes):
    done = False
    obs = env.reset()
    while True:
        env.render()
        random_action = env.action_space.sample()
        print('action',random_action)
        obs,reward,truncated,done,info = env.step(random_action)
        print('reward',reward)