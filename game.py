import pygame
import math
import random

# Game global variables
score = 0
high_score = 0
game_over = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        self.image = pygame.image.load('sprites/player/down.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20,40))
        self.rect = self.image.get_rect(center = (player_pos.x, player_pos.y))
        
        self.position = pygame.Vector2(self.player_pos)
        self.direction = pygame.Vector2(0, -1)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if self.rect.y >= 10:
            if keys[pygame.K_w]:
                self.rect.y -= 200*dt
        if self.rect.y <= 533:
            if keys[pygame.K_s]:
                self.rect.y += 200*dt
        if self.rect.x >= 10:
            if keys[pygame.K_a]:
                self.rect.x -= 200*dt
        if self.rect.x <= 530:
            if keys[pygame.K_d]:
                self.rect.x += 200*dt
    
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

SCREEN_WIDTH = 560
SCREEN_HEIGHT = 580

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ground_image = pygame.image.load('images/background_simple.png').convert_alpha()

# For game over screen
test_font = pygame.font.Font(None, 50)
pause_text = test_font.render('Pause', False, 'Red')
score_text = pygame.font.Font(None, 20).render(f'Score: {score}', False, 'White' )

# Player
player_surf = pygame.image.load('sprites/player/down.png').convert_alpha()
player_rect = player_surf.get_rect(center = (player_pos.x, player_pos.y))

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
#pygame.time.set_timer(tomato_timer, 900)

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