import gymnasium as gym
import matplotlib.pyplot as plt
from register_env import register_custom_env
import numpy as np
import tensorflow as tf
from tensorflow import keras
from collections import deque

register_custom_env()

# Create an instance of your custom environment
env = gym.make('dodge_game_env-v0')


input_shape = [42]
n_outputs = env.action_space.n

# Deep Q-Network model
#is there a way to improve this model?
model = keras.models.Sequential([
    keras.layers.Dense(64, activation="elu", input_shape=input_shape),
    keras.layers.Dropout(0.2), # Dropout layer to prevent overfitting
    keras.layers.Dense(64, activation="elu"),
    keras.layers.BatchNormalization(), # Batch Normalization layer
    keras.layers.Dense(32, activation="elu"),
    keras.layers.Dense(n_outputs)
])


# Boltzmann policy with numerically stable softmax
def stable_softmax(logits):
    z = logits - np.max(logits)
    exp_logits = np.exp(z)
    sum_exp_logits = np.sum(exp_logits)
    softmax = exp_logits / sum_exp_logits
    return softmax

def boltzmann_policy(state, temperature=1.0):
    Q_values = model.predict(state[np.newaxis], verbose=0)[0]
    scaled_Q_values = Q_values / temperature
    probabilities = stable_softmax(scaled_Q_values)
    action = np.random.choice(n_outputs, p=probabilities)
    return action

# Other configurations
replay_buffer = deque(maxlen=2000)
batch_size = 32
discount_factor = 0.95
optimizer = keras.optimizers.legacy.Adam(learning_rate=1e-3)  # Adjusted optimizer
loss_fn = keras.losses.mean_squared_error


# Epsilon-greedy policy
def epsilon_greedy_policy(state, epsilon=0):
    if np.random.rand() < epsilon:
        return np.random.randint(n_outputs)
    else:
        Q_values = model.predict(state[np.newaxis])
        return np.argmax(Q_values[0])
    


# Other parameters and initialization
replay_buffer = deque(maxlen=2000)
batch_size = 32
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
try:
# Main loop for training
    for episode in range(1000):
        obs, info = env.reset()
        print('episode:', episode)
        # Your code here to preprocess 'obs' into a 42-element state representation if needed

        total_reward = 0  # Track total reward per episode
        env.render()

        for step in range(20000):
            
            env.render()
            epsilon = max(1 - episode / 500, 0.01)
            temperature = 1
            # epsilon greedy policy
            # action = epsilon_greedy_policy(obs, epsilon)
            action = boltzmann_policy(obs, temperature)
            next_obs, reward, truncated, done, info = env.step(action)

            # Your code here to preprocess 'next_obs' into a 42-element state representation if needed

            replay_buffer.append((obs, action, reward, next_obs, done))
            obs = next_obs

            total_reward += reward  # Accumulate total reward for this episode

            if env.done:
                plt.clf()  # Clear the previous plot
                plt.plot(episode_rewards, label='Episode Rewards')
                plt.legend()
                plt.pause(0.001)  # Pause to show the updated plot
                obs = env.reset()
                break

        if episode > 50:
            training_step(batch_size)
        
        episode_rewards.append(total_reward)  # Append episode total reward for plotting
        print('Total reward:', total_reward)

    #after the loop ends, I want to save the model and the plot
    model.save('my_trained_model')  # This will create a directory named 'my_trained_model'

    # Plot the final learning curve after training completion
    plt.clf()  # Clear any existing plot
    plt.plot(episode_rewards, label='Episode Rewards')  # Plot the data
    plt.xlabel('Episodes')
    plt.ylabel('Total Rewards')
    plt.title('Learning Curve')
    plt.legend()
    plt.savefig('learning_curve.png')  # This will create a PNG file named 'learning_curve.png'
    plt.show()  # Show the plot

except Exception as e:
    print(e)
    model.save('path_to_model_on_error')
        # Plot the final learning curve after training completion
    plt.clf()  # Clear any existing plot
    plt.plot(episode_rewards, label='Episode Rewards')  # Plot the data
    plt.xlabel('Episodes')
    plt.ylabel('Total Rewards')
    plt.title('Learning Curve')
    plt.legend()
    plt.savefig('learning_curve.png')  # This will create a PNG file named 'learning_curve.png'
    plt.show()  # Show the plot
finally:
    model.save('path_to_model_on_error')