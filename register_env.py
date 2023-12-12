import gymnasium as gym

def register_custom_env():
    gym.envs.register(
        id='dodge_game_env-v0',
        entry_point='game_cus_gym_env:Game_env',  
        max_episode_steps=10000,  # Optional: Define maximum episode steps
        reward_threshold=1000,   # Optional: Set the reward threshold
    )

    gym.envs.register(
        id='dodge_game_env-v1',
        entry_point='game_cus_gym_env_version_2:Game_env',  
        max_episode_steps=10000,  # Optional: Define maximum episode steps
        reward_threshold=1000,   # Optional: Set the reward threshold
    )

    gym.envs.register(
        id='dodge_game_env-v3',
        entry_point='game_cus_gym_env_v3:Game_env',  
        max_episode_steps=10000,  # Optional: Define maximum episode steps
        reward_threshold=1000,   # Optional: Set the reward threshold
    )