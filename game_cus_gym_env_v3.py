import gymnasium as gym
#import gym
from gymnasium import spaces
import pygame
import math
import random
import numpy as np
import time

# this is the game enviroment file
# in this file we will define the game enviroment(duh)


# Game global variables
score = 0
high_score = 0
game_over = False
dt=0
player_dir = ''

SCREEN_WIDTH = 560
SCREEN_HEIGHT = 580

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.image = pygame.image.load('sprites/player/down.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20,40))
        self.rect = self.image.get_rect(center = (self.player_pos.x, self.player_pos.y))
        
        self.position = pygame.Vector2(self.player_pos)
        self.direction = pygame.Vector2(0, -1)

    # There are 8 input (actions)
    def player_input(self, player_dir):
        global dt
        

        corner_regions = [
        pygame.Rect(520, 535, 20, 30),  # Top left corner
        pygame.Rect(15, 535, 20, 30),   # Top right corner
        pygame.Rect(520, 15, 20, 30),   # Bottom left corner
        pygame.Rect(15, 15, 20, 30)     # Bottom right corner
        ]
    # Check if the player is in any corner region and adjust position
        for corner_rect in corner_regions:
            if corner_rect.colliderect(self.rect):
                if corner_rect == corner_regions[0]:
                    self.rect.x += 1
                    self.rect.y += 1
                elif corner_rect == corner_regions[1]:
                    self.rect.x -= 1
                    self.rect.y += 1
                elif corner_rect == corner_regions[2]:
                    self.rect.x += 1
                    self.rect.y -= 1
                elif corner_rect == corner_regions[3]:
                    self.rect.x -= 1
                    self.rect.y -= 1
        
        if self.rect.y >= 10:
            if player_dir == 'up':
                self.rect.y -= 300*dt
        if self.rect.y <= 533:
            if player_dir == 'down':
                self.rect.y += 300*dt
        if self.rect.x >= 10:
            if player_dir == 'left':
                self.rect.x -= 300*dt
        if self.rect.x <= 530:
            if player_dir == 'right':
                self.rect.x += 300*dt

        # For diagonal movement for IA (testing process)
        if self.rect.y >= 10 and self.rect.x >= 10:
            if player_dir == 'up_left':
                self.rect.y -= 300*dt
                self.rect.x -= 300*dt
        if self.rect.y >= 10 and self.rect.x <= 530:
            if player_dir == 'up_right':
                self.rect.y -= 300*dt
                self.rect.x += 300*dt
        if self.rect.y <= 533 and self.rect.x >= 10:
            if player_dir == 'down_left':
                self.rect.y += 300*dt
                self.rect.x -= 300*dt
        if self.rect.y <= 533 and self.rect.x <= 530:
            if player_dir == 'down_right':
                self.rect.y += 300*dt
                self.rect.x += 300*dt
        
    
    def update(self, player_dir):
        self.player_input(player_dir)

# Tomato class
class Tomato(pygame.sprite.Sprite):
    def __init__(self, x, y, p_x, p_y, player_instance):
        super().__init__()
        self.image = pygame.image.load('sprites/tomato.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect(center=(x,y))
        self.player_instance = player_instance

        angle = math.atan2(p_y - y, p_x - x)
        angle += random.uniform(-0.3, 0.3)
        speed = 8
        self.dx = math.cos(angle) * speed 
        self.dy = math.sin(angle) * speed
    
    # TODO: Fix the angles
    def update(self):
        global game_over

        self.rect.x += (int(self.dx))
        self.rect.y += (int(self.dy))

        if self.player_instance.rect.colliderect(self.rect):
           game_over = True

        self.destroy()
    
    def destroy(self):
        global score
        if self.rect.x <= 15 or self.rect.x >= 545 or self.rect.y <= 15 or self.rect.y >= 565:
            self.kill()
            score += 1

# Game enviroment class

class Game_env(gym.Env):
    def __init__(self):
        self.render_mode = None
        self.done = False
        self.action_space = spaces.Discrete(8)
        # FOR TESTING, change the shape as needed
        self.observation_space = spaces.Box(low=-1000, high=1000, shape=(42,), dtype=np.int32) # Player position and potential 100 tomatoes positions
        pygame.init()
        pygame.font.init()
        # for the game
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.score_text = pygame.font.Font(None, 20).render(f'Score: {score}', False, 'White')
        # Create the player starting position
        self.player_pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        
        # Load player sprite
        self.player_surf = pygame.image.load('sprites/player/down.png').convert_alpha()

        # Background
        self.ground_image = pygame.image.load('images/background_simple.png').convert_alpha()

        self.start_time = time.time()  # Store the start time
        self.player = pygame.sprite.Group()
        self.player_instance = Player()
        self.player.add(self.player_instance)  

        self.tomato = pygame.sprite.Group()

        self.reset()

    def _get_obs(self):
        player_pos = [self.player_instance.rect.x, self.player_instance.rect.y]

        tomato_pos = []
        for tomatoes in self.tomato.sprites():
            tomato_pos.extend([tomatoes.rect.x, tomatoes.rect.y])

        # For testing purposes, change the number_instances as needed
        number_instances = 20
        if len(self.tomato) < number_instances:
            zeros_to_fill = (number_instances - len(self.tomato)) * 2
            tomato_pos.extend([0] * zeros_to_fill)

        return player_pos + tomato_pos

    def step(self, action):

        global dt, game_over
        
        self.tomato.update()
        dt = self.clock.tick(60) / 1000
        play_field_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)


        if not play_field_rect.contains(self.player_instance.rect):
        # Player has gone off the map
            game_over = True
            self.reward = -200
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            tomato_top_left = Tomato(40,40, self.player_instance.rect.x, self.player_instance.rect.y, self.player_instance)
            tomato_top_right = Tomato(518,40, self.player_instance.rect.x, self.player_instance.rect.y, self.player_instance)
            tomato_bottom_left = Tomato(40,540, self.player_instance.rect.x, self.player_instance.rect.y, self.player_instance)
            tomato_bottom_right = Tomato(518,540, self.player_instance.rect.x, self.player_instance.rect.y, self.player_instance)
            
            # Top Left
            if event.type == self.top_left_timer:
                self.tomato.add(tomato_top_left)
                pygame.time.set_timer(self.top_left_timer, random.randint(900, 1400))  # reset timer
            # Top Right
            if event.type == self.top_right_timer:
                self.tomato.add(tomato_top_right)
                pygame.time.set_timer(self.top_right_timer, random.randint(1100, 1200))  # reset timer 2
            # Bottom Left
            if event.type == self.bottom_left_timer:
                self.tomato.add(tomato_bottom_left)
                pygame.time.set_timer(self.bottom_left_timer, random.randint(900, 1000)) # reset timer 3
            # Bottom right
            if event.type == self.bottom_right_timer:
                self.tomato.add(tomato_bottom_right)
                pygame.time.set_timer(self.bottom_right_timer, random.randint(700, 1800))  # Timer 4

        # player direction
        if action == 0:
            player_dir = 'up'
        elif action == 1:
            player_dir = 'down'
        elif action == 2:
            player_dir = 'left'
        elif action == 3:
            player_dir = 'right'
        elif action == 4:
            player_dir = 'up_left'
        elif action == 5:
            player_dir = 'up_right'
        elif action == 6:
            player_dir = 'down_left'
        elif action == 7:
            player_dir = 'down_right'

        self.player.update(player_dir)
        
        """self.observation = {
            'player_x_pos': self.player_instance.rect.x,
            'player_y_pos': self.player_instance.rect.y,
            'player_action': action
        }"""

        reward_interval = 3
        elapsed_time = time.time() - self.start_time

        if elapsed_time >= reward_interval:
            self.reward = 2
            self.start_time = time.time() # reset timer
        #else:
        #    self.reward = 0

        self.info = {}

        self.observation = self._get_obs()
        self.observation = np.array([self.observation])
        self.observation = self.observation.reshape(-1)
        self.truncated = False
        #print(self.done)
        corner_buffer = 60  # Adjust this value to set how close to the corner counts as 'near'
        corner_areas = [
            pygame.Rect(0, 0, corner_buffer, corner_buffer),  # Top left corner
            pygame.Rect(SCREEN_WIDTH - corner_buffer, 0, corner_buffer, corner_buffer),  # Top right corner
            pygame.Rect(0, SCREEN_HEIGHT - corner_buffer, corner_buffer, corner_buffer),  # Bottom left corner
            pygame.Rect(SCREEN_WIDTH - corner_buffer, SCREEN_HEIGHT - corner_buffer, corner_buffer, corner_buffer)  # Bottom right corner
        ]

        if game_over:
            # Check if player is near any corner
            player_near_corner = any(corner_area.colliderect(self.player_instance.rect) for corner_area in corner_areas)
            self.reward = -21 if player_near_corner else -7
            self.start_time = time.time() # reset timer
            self.done = True
            #return self.observation, self.reward, self.truncated, self.done, self.info

        return self.observation, self.reward, self.truncated, self.done, self.info



    def reset(self, seed=None):
        global score, game_over
        # Reset part
        self.done = False
        game_over = False
        score = 0 # Reset score
        self.game_over = False
        self.tomato = pygame.sprite.Group()
        self.player = pygame.sprite.Group()
        self.player_instance = Player()
        self.player.add(self.player_instance)   

        # 4 Event times for each tomato spawn
        self.top_left_timer = pygame.USEREVENT + 1
        self.top_right_timer = pygame.USEREVENT + 2
        self.bottom_left_timer = pygame.USEREVENT + 3
        self.bottom_right_timer = pygame.USEREVENT + 4
        pygame.time.set_timer(self.top_left_timer, random.randint(1200, 1500))  # Timer 1
        pygame.time.set_timer(self.top_right_timer, random.randint(1300, 1500))  # Timer 2
        pygame.time.set_timer(self.bottom_left_timer, random.randint(1200, 1900))  # Timer 3
        pygame.time.set_timer(self.bottom_right_timer, random.randint(1100, 1500))  # Timer 4
        
        if player_dir == 'up':
            self.numerical_dir = 0
        elif player_dir == 'down':
            self.numerical_dir = 1
        elif player_dir == 'left':
            self.numerical_dir = 2
        elif player_dir == 'right':
            self.numerical_dir = 3
        elif player_dir == 'up_left':
            self.numerical_dir = 4
        elif player_dir == 'up_right':
            self.numerical_dir = 5
        elif player_dir == 'down_left':
            self.numerical_dir = 6
        elif player_dir == 'down_right':
            self.numerical_dir = 7

        self.reward = 0
        

        if self.render_mode == 'human':
            self.render()

        self.observation = self._get_obs()
        self.observation = np.array([self.observation])
        self.observation = self.observation.reshape(-1)

        self.info = {}

        return self.observation, self.info

    def render(self, render_mode='human'):

        global score

        # Background
        self.screen.blit(self.ground_image, (0,0))

        # Loading the 4 enemy sprites
        enemy_up_left = pygame.image.load('sprites/enemy/up_left.png').convert_alpha()
        enemy_up_left = pygame.transform.scale(enemy_up_left, (20,30))
        enemy_up_right = pygame.image.load('sprites/enemy/up_right.png').convert_alpha()
        enemy_up_right = pygame.transform.scale(enemy_up_right, (20,30))
        enemy_down_left = pygame.image.load('sprites/enemy/down_left.png').convert_alpha()
        enemy_down_left = pygame.transform.scale(enemy_down_left, (20,30))
        enemy_down_right = pygame.image.load('sprites/enemy/down_right.png').convert_alpha()
        enemy_down_right = pygame.transform.scale(enemy_down_right, (20,30))
        # Positioning the 4 enemies
        enemy_up_left_rect = enemy_up_left.get_rect(topleft=(520,535))
        enemy_up_right_rect = enemy_up_right.get_rect(topleft=(15,535))
        enemy_down_left_rect = enemy_down_left.get_rect(topleft=(520,15))
        enemy_down_right_rect = enemy_down_right.get_rect(topleft=(15,15))
        
        #Enemy drawn
        self.screen.blit(enemy_up_left, enemy_up_left_rect)
        self.screen.blit(enemy_up_right, enemy_up_right_rect)
        self.screen.blit(enemy_down_left, enemy_down_left_rect)
        self.screen.blit(enemy_down_right, enemy_down_right_rect)

        # Score
        self.screen.blit(self.score_text,(250,40))
        self.score_text = pygame.font.Font(None, 20).render(f'Score: {score}', False, 'White')

        # Draw player and tomato
        self.player.draw(self.screen)
        self.tomato.draw(self.screen)


        # flip() the display to put your work on screen
        #pygame.display.flip()
        pygame.display.update()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = self.clock.tick(60) / 1000
    
    def close(self):
        pygame.quit()



# Unit testing 
# env = Game_env()
# for _ in range(3000):
#    action = env.action_space.sample()
#    obs, reward, truncated, done, _ = env.step(action)
#    if done:
#        env.reset()
#    env.render()
    
# env.close()