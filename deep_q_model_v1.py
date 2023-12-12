import gymnasium as gym
import matplotlib.pyplot as plt
from register_env import register_custom_env
import numpy as np
import tensorflow as tf
from tensorflow import keras
from collections import deque
import os

register_custom_env()

# Create an instance of your custom environment
env = gym.make('dodge_game_env-v1')


input_shape = [21]
n_outputs = 8

# Deep Q-Network model
model = keras.models.Sequential([
    keras.layers.Dense(21, activation="relu", input_shape=input_shape),
    keras.layers.Dense(30, activation="relu"),
    keras.layers.Dense(20, activation="relu"),
    keras.layers.Dense(n_outputs)
])


#model.load_weights('models/trained_model.h5')


# Epsilon-greedy policy
def epsilon_greedy_policy(state, epsilon=0):
    if np.random.rand() < epsilon:
        return np.random.randint(n_outputs)
    else:
        Q_values = model.predict(state[np.newaxis])
        return np.argmax(Q_values[0])
    

# Other parameters and initialization
replay_buffer = deque(maxlen=2000)
batch_size = 21
discount_factor = 0.95
optimizer = keras.optimizers.Adam(lr=1e-3)
loss_fn = keras.losses.mean_squared_error


# Function to sample experiences from replay buffer
def sample_experiences(batch_size):
    indices = np.random.randint(len(replay_buffer), size=batch_size)
    batch = [replay_buffer[index] for index in indices]
    states, actions, rewards, next_states, dones = [
        np.array([experience[field_index] for experience in batch])
        for field_index in range(5)]
    return states, actions, rewards, next_states, dones


# Training step for DQN
def training_step(batch_size):
    experiences = sample_experiences(batch_size)
    states, actions, rewards, next_states, dones = experiences
    next_Q_values = model.predict(next_states)
    max_next_Q_values = np.max(next_Q_values, axis=1)
    target_Q_values = (rewards +
                       (1 - dones) * discount_factor * max_next_Q_values)
    mask = tf.one_hot(actions, n_outputs)
    with tf.GradientTape() as tape:
        all_Q_values = model(states)
        Q_values = tf.reduce_sum(all_Q_values * mask, axis=1, keepdims=True)
        loss = tf.reduce_mean(loss_fn(target_Q_values, Q_values))
    grads = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(grads, model.trainable_variables))

episode_rewards = []
training_losses = []

# Visualize the learning curve
plt.figure(figsize=(8, 6))
plt.xlabel('Timesteps')
plt.ylabel('Total Rewards')
plt.title('Learning Curve')

# Create a new file in write mode ('w') to start fresh
with open('record_training.txt', 'w') as file:
    file.write('Rewards per Episode:\n')  # Initial header or marker



# Directory to save models
model_dir = 'models'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)


# Main loop for training
for episode in range(100000):
    obs, info = env.reset()
    print('episode:', episode)
    # Your code here to preprocess 'obs' into a 42-element state representation if needed

    total_reward = 0  # Track total reward per episode
    env.render()

    for step in range(2000):
        
        env.render()
        epsilon = max(1 - episode / 500, 0.01)
        #epsilon = 6
        action = epsilon_greedy_policy(obs, epsilon)
        next_obs, reward, truncated, done, info = env.step(action)

        # Your code here to preprocess 'next_obs' into a 42-element state representation if needed

        replay_buffer.append((obs, action, reward, next_obs, done))
        obs = next_obs

        total_reward += reward  # Accumulate total reward for this episode

        if env.done:

            with open('record_training.txt', 'a') as file:
                file.write(f'Episode: {episode + 1}, Total Reward: {total_reward}, Exploration Rate (epsilon): {epsilon}\n')
            plt.clf()  # Clear the previous plot
            plt.plot(episode_rewards, label='Episode Rewards')
            plt.legend()
            plt.pause(0.001)  # Pause to show the updated plot
            obs = env.reset()

            if episode % 100 == 0:
                model.save('models/trained_model.h5')

            break

    if episode > 50:
        training_step(batch_size)
    
    episode_rewards.append(total_reward)  # Append episode total reward for plotting
    print('Total reward:', total_reward)



# Plot the final learning curve after training completion
plt.clf()
plt.plot(episode_rewards, label='Episode Rewards')
plt.legend()
plt.show()