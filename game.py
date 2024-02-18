import pygame
import math
import random

# Game global variables
score = 0
high_score = 0
game_over = False
SCREEN_WIDTH = 560
SCREEN_HEIGHT = 580

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

        self.standing = [pygame.image.load('sprites/player/down.png')]

        # For Animation
        self.left = [pygame.image.load('sprites/player/left/1.png'),pygame.image.load('sprites/player/left/2.png'),pygame.image.load('sprites/player/left/3.png'),pygame.image.load('sprites/player/left/4.png'),pygame.image.load('sprites/player/left/5.png'),pygame.image.load('sprites/player/left/6.png'),pygame.image.load('sprites/player/left/7.png'),pygame.image.load('sprites/player/left/8.png'),]
        self.right = [pygame.image.load('sprites/player/right/1.png'),pygame.image.load('sprites/player/right/2.png'),pygame.image.load('sprites/player/right/3.png'),pygame.image.load('sprites/player/right/4.png'),pygame.image.load('sprites/player/right/5.png'),pygame.image.load('sprites/player/right/6.png'),pygame.image.load('sprites/player/right/7.png'),pygame.image.load('sprites/player/right/8.png'),]
        self.up = [pygame.image.load('sprites/player/up/1.png'),pygame.image.load('sprites/player/up/2.png'),pygame.image.load('sprites/player/up/3.png'),pygame.image.load('sprites/player/up/4.png'),pygame.image.load('sprites/player/up/5.png'),pygame.image.load('sprites/player/up/6.png'),pygame.image.load('sprites/player/up/7.png'),pygame.image.load('sprites/player/up/8.png'),]
        self.up_left = [pygame.image.load('sprites/player/up_left/1.png'),pygame.image.load('sprites/player/up_left/2.png'),pygame.image.load('sprites/player/up_left/3.png'),pygame.image.load('sprites/player/up_left/4.png'),pygame.image.load('sprites/player/up_left/5.png'),pygame.image.load('sprites/player/up_left/6.png'),pygame.image.load('sprites/player/up_left/7.png'),pygame.image.load('sprites/player/up_left/8.png'),]
        self.up_right = [pygame.image.load('sprites/player/up_right/1.png'),pygame.image.load('sprites/player/up_right/2.png'),pygame.image.load('sprites/player/up_right/3.png'),pygame.image.load('sprites/player/up_right/4.png'),pygame.image.load('sprites/player/up_right/5.png'),pygame.image.load('sprites/player/up_right/6.png'),pygame.image.load('sprites/player/up_right/7.png'),pygame.image.load('sprites/player/up_right/8.png'),]
        self.down = [pygame.image.load('sprites/player/down/1.png'),pygame.image.load('sprites/player/down/2.png'),pygame.image.load('sprites/player/down/3.png'),pygame.image.load('sprites/player/down/4.png'),pygame.image.load('sprites/player/down/5.png'),pygame.image.load('sprites/player/down/6.png'),pygame.image.load('sprites/player/down/7.png'),pygame.image.load('sprites/player/down/8.png'),]
        self.down_left = [pygame.image.load('sprites/player/down_left/1.png'),pygame.image.load('sprites/player/down_left/2.png'),pygame.image.load('sprites/player/down_left/3.png'),pygame.image.load('sprites/player/down_left/4.png'),pygame.image.load('sprites/player/down_left/5.png'),pygame.image.load('sprites/player/down_left/6.png'),pygame.image.load('sprites/player/down_left/7.png'),pygame.image.load('sprites/player/down_left/8.png'),]
        self.down_right = [pygame.image.load('sprites/player/down_right/1.png'),pygame.image.load('sprites/player/down_right/2.png'),pygame.image.load('sprites/player/down_right/3.png'),pygame.image.load('sprites/player/down_right/4.png'),pygame.image.load('sprites/player/down_right/5.png'),pygame.image.load('sprites/player/down_right/6.png'),pygame.image.load('sprites/player/down_right/7.png'),pygame.image.load('sprites/player/down_right/8.png'),]
        
        self.current_sprite = 0
        self.image = self.standing[self.current_sprite]
        self.image = pygame.transform.scale(self.image, (20,40))
        self.rect = self.image.get_rect(center = (self.player_pos.x, self.player_pos.y))
        
    # TODO: make the nested if statement into one if statement per move
    def player_input(self):

        speed = 0.7
        self.current_sprite += speed

        if self.current_sprite > 7:
            self.current_sprite = 0

        # If player is not moving, default sprite is used
        self.image = self.standing[0]

        keys = pygame.key.get_pressed()
        if self.rect.y >= 10 and not keys[pygame.K_a] and not keys[pygame.K_d] and keys[pygame.K_w]:
            self.rect.y -= 200*dt
            self.image = self.up[int(self.current_sprite)]

        if self.rect.y <= 533 and not keys[pygame.K_a] and not keys[pygame.K_d] and keys[pygame.K_s]:
            self.rect.y += 200*dt
            self.image = self.down[int(self.current_sprite)]

        if self.rect.x >= 10 and not keys[pygame.K_w] and not keys[pygame.K_s] and keys[pygame.K_a]:
            self.rect.x -= 200*dt
            self.image = self.left[int(self.current_sprite)]

        if self.rect.x <= 530 and not keys[pygame.K_w] and not keys[pygame.K_s] and keys[pygame.K_d]:
            self.rect.x += 200*dt
            self.image = self.right[int(self.current_sprite)]

        # Diagonal
        if self.rect.y >= 10 and self.rect.x >= 10 and keys[pygame.K_w] and keys[pygame.K_a]:
            self.rect.y -= 200*dt
            self.rect.x -= 200*dt
            self.image = self.up_left[int(self.current_sprite)]

        if self.rect.y >= 10 and self.rect.x <= 530 and keys[pygame.K_w] and keys[pygame.K_d]:
            self.rect.y -= 200*dt
            self.rect.x += 200*dt
            self.image = self.up_right[int(self.current_sprite)]

        if self.rect.y <= 533 and self.rect.x >= 10 and keys[pygame.K_s] and keys[pygame.K_a]:
            self.rect.y += 200*dt
            self.rect.x -= 200*dt
            self.image = self.down_left[int(self.current_sprite)]

        if self.rect.y <= 533 and self.rect.x <= 530 and keys[pygame.K_s] and keys[pygame.K_d]:
            self.rect.y += 200*dt
            self.rect.x += 200*dt
            self.image = self.down_right[int(self.current_sprite)]

        self.image = pygame.transform.scale(self.image, (20,40))

    def update(self):
        self.player_input()

class Tomato(pygame.sprite.Sprite):
    def __init__(self, x, y, p_x, p_y, player_instance):
        super().__init__()
        self.image = pygame.image.load('sprites/tomato.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect(center=(x,y))
        self.player_instance = player_instance

        angle = math.atan2(p_y - y, p_x - x)
        speed = 5
        self.dx = (math.cos(angle) + random.uniform(-0.1, 0.1)) * speed 
        self.dy = (math.sin(angle) + random.uniform(-0.1, 0.1)) * speed
    
    # TODO: Fix the angles
    def update(self):
        global game_over

        self.rect.x += int(self.dx)
        self.rect.y += int(self.dy)

        if player_instance.rect.colliderect(self.rect):
            game_over = True

        self.destroy()
    
    def destroy(self):
        global score
        if self.rect.x <= 15 or self.rect.x >= 545 or self.rect.y <= 15 or self.rect.y >= 565:
            self.kill()
            score += 1

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

ground_image = pygame.image.load('sprites/background_simple.png').convert_alpha()

# For game over screen
test_font = pygame.font.Font(None, 50)
pause_text = test_font.render('Pause', False, 'Red')
score_text = pygame.font.Font(None, 20).render(f'Score: {score}', False, 'White' )

# Class player
player = pygame.sprite.Group()
player_instance = Player()
player.add(player_instance)

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

# 4 Event times for each enemy
top_left_timer = pygame.USEREVENT + 1
top_right_timer = pygame.USEREVENT + 2
bottom_left_timer = pygame.USEREVENT + 3
bottom_right_timer = pygame.USEREVENT + 4

pygame.time.set_timer(top_left_timer, random.randint(200, 500))  # Timer 1
pygame.time.set_timer(top_right_timer, random.randint(300, 500))  # Timer 2
pygame.time.set_timer(bottom_left_timer, random.randint(200, 900))  # Timer 3
pygame.time.set_timer(bottom_right_timer, random.randint(100, 500))  # Timer 4

# Class tomato 
tomato = pygame.sprite.Group()

while running:
    
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():

        tomato_top_left = Tomato(40,40, player_instance.rect.x, player_instance.rect.y, player_instance)
        tomato_top_right = Tomato(518,40, player_instance.rect.x, player_instance.rect.y, player_instance)
        tomato_bottom_left = Tomato(40,540, player_instance.rect.x, player_instance.rect.y, player_instance)
        tomato_bottom_right = Tomato(518,540, player_instance.rect.x, player_instance.rect.y, player_instance)
        
        # Top Left
        if event.type == top_left_timer:
            tomato.add(tomato_top_left)
            pygame.time.set_timer(top_left_timer, random.randint(400, 800))  # reset timer
        # Top Right
        if event.type == top_right_timer:
            tomato.add(tomato_top_right)
            pygame.time.set_timer(top_right_timer, random.randint(500, 700))  # reset timer 2
        # Bottom Left
        if event.type == bottom_left_timer:
            tomato.add(tomato_bottom_left)
            pygame.time.set_timer(bottom_left_timer, random.randint(200, 900)) # reset timer 3
        # Bottom right
        if event.type == bottom_right_timer:
            tomato.add(tomato_bottom_right)
            pygame.time.set_timer(bottom_right_timer, random.randint(400, 800))  # Timer 4
            
        if event.type == pygame.QUIT:
            running = False

    # Gaming screen
    if not game_over:

        # Background here
        screen.blit(ground_image, (0,0))

        player.draw(screen)
        player.update()

        #Enemy
        screen.blit(enemy_up_left, enemy_up_left_rect)
        screen.blit(enemy_up_right, enemy_up_right_rect)
        screen.blit(enemy_down_left, enemy_down_left_rect)
        screen.blit(enemy_down_right, enemy_down_right_rect)

        tomato.draw(screen)
        tomato.update()

        # Score
        screen.blit(score_text,(250,40))
        score_text = pygame.font.Font(None, 20).render(f'Score: {score}', False, 'White')

    # game over screen
    else:
        screen.fill('Black')
        if score > high_score:
            high_score = score
        
        # Display score
        score_text = pygame.font.Font(None, 30).render(f'Score: {score}', False, 'White')
        screen.blit(score_text,(200,180))

        # Display highest score
        high_score_text = pygame.font.Font(None, 30).render(f'Highest score: {high_score}', False, 'White')
        screen.blit(high_score_text,(200,215))

        continue_prompt = pygame.font.Font(None, 50).render('Press Enter to play again', False, 'White')
        screen.blit(continue_prompt,(100,340))
        keys = pygame.key.get_pressed()

        # Reset game
        if keys[pygame.K_RETURN]:
            score = 0 # Reset score
            game_over = False
            tomato = pygame.sprite.Group()
            player = pygame.sprite.Group()
            player_instance = Player()
            player.add(player_instance)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()