import gymnasium as gym
from stable_baselines3 import PPO
import matplotlib.pyplot as plt
from register_env import register_custom_env
import numpy as np

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
total_timesteps = 4000000  # Set the number of training timesteps


obs, _ = env.reset()
env.render()

# Training loop with episode rewards collection
episode_rewards = []
episode_reward = 0  # Track the total reward per episode

# Exploration rate (20% exploration)
exploration_rate = 0.99999

# Visualize the learning curve
plt.figure(figsize=(8, 6))
plt.xlabel('Timesteps')
plt.ylabel('Total Rewards')
plt.title('Learning Curve')

for timestep in range(total_timesteps):
    if np.random.rand() < exploration_rate:
        action = env.action_space.sample()  # Random exploration
        exploration_rate *= 0.99999
    else:
        action, _ = model.predict(obs, deterministic=True)  # Exploitation
        
    obs, reward, truncated, done, _ = env.step(action)
    env.render()

    episode_reward += reward  # Accumulate the reward for the episode

    if env.done:
        print(exploration_rate)
        print(f"Episode finished with reward: {episode_reward}")
        episode_rewards.append(episode_reward)
        episode_reward = 0  # Reset episode reward for the next episode

        obs, _ = env.reset()
        env.render()
        plt.clf()  # Clear the previous plot
        plt.plot(episode_rewards, label='Episode Rewards')
        plt.legend()
        plt.pause(0.001)  # Pause to show the updated plot

        
# Plot the final learning curve after training completion
plt.clf()
plt.plot(episode_rewards, label='Episode Rewards')
plt.legend()
plt.show()



