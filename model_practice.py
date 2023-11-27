import gymnasium as gym
from stable_baselines3 import PPO
import matplotlib.pyplot as plt
from register_env import register_custom_env

register_custom_env()

# Create an instance of your custom environment
env = gym.make('dodge_game_env-v0')  


"""# Testing game
for i in range(10000):
    obs,reward,truncated,done,_ = env.step(env.action_space.sample())
    if done:
        env.reset()
    env.render()"""

# Choose PPO as the reinforcement learning algorithm
model = PPO("MlpPolicy", env, verbose=1)  # You can change "MlpPolicy" based on your network architecture

# Train the agent on your environment for a certain number of timesteps
total_timesteps = 10000  # Set the number of training timesteps
#model.learn(total_timesteps=total_timesteps, callback=None)  # You can use callbacks to log additional information


obs, _ = env.reset()
env.render()

# Training loop with episode rewards collection
episode_rewards = []

# Visualize the learning curve
plt.figure(figsize=(8, 6))
plt.xlabel('Episodes')
plt.ylabel('Total Rewards')
plt.title('Learning Curve')

for timestep in range(total_timesteps):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, truncated, done, _ = env.step(action)
    env.render()

    episode_rewards.append(reward)

    if done:
        plt.clf()  # Clear the previous plot
        plt.plot(episode_rewards, label='Episode Rewards')
        plt.legend()
        plt.pause(0.001)  # Pause to show the updated plot
        obs, _ = env.reset()
        env.render()



