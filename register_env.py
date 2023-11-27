import gymnasium as gym

def register_custom_env():
    gym.envs.register(
        id='dodge_game_env-v0',
        entry_point='game_cus_gym_env:Game_env',  
        max_episode_steps=100,  # Optional: Define maximum episode steps
        reward_threshold=10,   # Optional: Set the reward threshold
    )