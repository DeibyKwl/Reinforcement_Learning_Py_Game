import pygame
import math
import random
import time

import cards as card
import dice

game_over = False
roll_dice = False

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
dice_number = None
dice_number_view = None

# Select Player
player = pygame.sprite.Group()
player_class = None
player_clicked = False
player_selected = True
player_class_code = None # Use to determine if card attack receive bonus


# TODO: Change this while loop into its own file
while player_selected:

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    if pygame.QUIT in set([x.type for x in pygame.event.get()]):
        player_selected = False
    
    screen.fill("black")

    mouse_pos = pygame.mouse.get_pos()

    selection_text = pygame.font.Font(None, 50).render('Select your character', False, 'White')
    screen.blit(selection_text,(430,200))

    swordman_text = pygame.font.Font(None, 30).render('SWORDMAN', False, 'White')
    swordman_rect = swordman_text.get_rect(topleft = (560,350))
    screen.blit(swordman_text,(560,350))

    archer_text = pygame.font.Font(None, 30).render('ARCHER', False, 'White')
    archer_rect = archer_text.get_rect(topleft = (580,450))
    screen.blit(archer_text,(580,450))

    mage_text = pygame.font.Font(None, 30).render('MAGE', False, 'White')
    mage_rect = mage_text.get_rect(topleft = (595,550))
    screen.blit(mage_text,(595,550))

    pressed = True if pygame.mouse.get_pressed()[0] == 1 else False

    if swordman_rect.collidepoint(mouse_pos) and pressed:
        player_class = 'swordman'
        player_selected = False
        player_class_code = 0

    if archer_rect.collidepoint(mouse_pos) and pressed:
        player_class = 'archer'
        player_selected = False
        player_class_code = 1

    if mage_rect.collidepoint(mouse_pos) and pressed:
        player_class = 'mage'
        player_selected = False
        player_class_code = 2

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000


player_instance = card.player_set(player_class)
player.add(player_instance)

# Determine number of enemies
enemy_num = dice.roll_dice(screen)
dice_num = enemy_num

enemies = pygame.sprite.Group()
enemy_classes = ['swordman', 'archer', 'mage']
enemy_x_pos, enemy_y_pos = 25,10
number_of_enemies = 0

# Creation of enemies
for _ in range(enemy_num):
    # TODO: find a way to sparce enemies evenly depending on the number of enemies

    enemy_class_code = random.randint(0,2)
    enemy_instance = card.enemy_set(enemy_classes[enemy_class_code], enemy_class_code,enemy_x_pos,enemy_y_pos)
    enemies.add(enemy_instance)
    enemy_x_pos += 170
    number_of_enemies += 1


cards_set = pygame.sprite.Group()
card_classes = ['sword_attack', 'arrow_shot', 'magic_attack', 'heal', 'defense']
card_x_pos, card_y_pos = 25, 700

attack_card_num = 0
defense_card_num = 0

# To know last x position of attack card
last_x_pos = 0

# Creation of card set
for _ in range(7):
    card_class = random.randint(0,4)
    bonus = True if player_class_code == card_class else False
    card_instance = card.deck_set(card_classes[card_class], card_x_pos, card_y_pos, bonus)
    
    if card_class in [0,1,2]:
        attack_card_num += 1
        last_x_pos = card_x_pos

    # For the shield
    elif card_class == 4:
        defense_card_num += 1

    cards_set.add(card_instance)
    card_x_pos += 170

card_selection = True
attack_enemy = False
card_selected = None
enemy_turn = False


# main gameplay
while running:

    mouse_pos = pygame.mouse.get_pos()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    if not roll_dice:
        dice_number_view = pygame.font.Font(None, 45).render(str(dice_num), True, "White")
    screen.blit(dice_number_view, (1100,500))

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    if pygame.QUIT in set([x.type for x in pygame.event.get()]):
        running = False
    
    player.draw(screen)
    enemies.draw(screen)
    cards_set.draw(screen)


    if enemy_turn and len(enemies) > 0:
        bonus_damage = False
        card_class = random.randint(0,2)
        if list(enemies)[0].enemy_class_code == card_class:
            enemy_card = card.deck_set(card_classes[card_class], 800, 300, True)
            bonus_damage = True
        else:
            enemy_card = card.deck_set(card_classes[card_class], 800, 300)
        
        enemy_card_attack = pygame.sprite.Group()
        enemy_card_attack.add(enemy_card)

        card_selection = True
        enemy_turn = False

        # Draw enemy card attack and wait some seconds to attack player
        duration = 1
        start_time = time.time()
        while time.time() - start_time < duration:
            enemy_card_attack.draw(screen)
            pygame.display.flip()

        if defense_card_num > 0:
            for c in cards_set:
                if c.card_class == 'defense':
                    c.kill()
                    defense_card_num -= 1
                    break
        else:
            # Dealing damage to player
            if bonus_damage:
                list(player)[0].health -= 2
            else:
                list(player)[0].health -= 1
            
            if list(player)[0].health > 0:
                list(player)[0].player_update()
            else:
                running = False
                result = 'Defeated'


    pressed = True if pygame.mouse.get_pressed()[0] == 1 else False

    # Card selection for attacking enemies
    if card_selection and pressed:
        for c in cards_set:
            if c.rect.collidepoint(mouse_pos) and c.card_class in ['sword_attack', 'arrow_shot', 'magic_attack']:
                c.player_card_used()
                card_selection = False
                attack_enemy = True
                card_selected = c

            elif c.rect.collidepoint(mouse_pos) and c.card_class == 'heal' and list(player)[0].health < 5:
                c.player_card_used()
                card_selection = False
                attack_enemy = False
                enemy_turn = True
                if list(player)[0].health == 4:
                    list(player)[0].health += 1
                else:
                    list(player)[0].health += 2
                list(player)[0].player_update()
                c.kill()
        
    if attack_enemy and pressed:
        for e in enemies:
            if e.rect.collidepoint(mouse_pos):
                e.kill()
                card_selected.kill()
                card_selection = False
                attack_enemy = False
                enemy_turn = True
                attack_card_num -= 1
                number_of_enemies -= 1
    
    if number_of_enemies == 0:
        running = False
        result = 'Victory'

    elif attack_card_num == 0:
        card_class = random.randint(0,2)
        bonus = True if player_class_code == card_class else False
        card_instance = card.deck_set(card_classes[card_class], last_x_pos, 700, bonus)
        attack_card_num += 1
        cards_set.add(card_instance)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000


game_over = True
while game_over:
    if pygame.QUIT in set([x.type for x in pygame.event.get()]):
        game_over = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    if result == 'Defeated':
        result_text = pygame.font.Font(None, 50).render('DEFEATED', False, 'White')
    elif result == 'Victory':
        result_text = pygame.font.Font(None, 50).render('VICTORY', False, 'White')

    screen.blit(result_text,(500,200))
    
    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()