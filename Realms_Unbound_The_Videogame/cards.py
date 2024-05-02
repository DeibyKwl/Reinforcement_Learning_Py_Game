import pygame

class deck_set(pygame.sprite.Sprite):
    def __init__(self, card_class, x_pos, y_pos, bonus=False):
        super().__init__()
        if bonus:
            self.image = pygame.image.load(f'sprites/deck/{card_class}_bonus.png').convert_alpha()
            self.card_class = f'{card_class}_bonus'
        else:
            self.image = pygame.image.load(f'sprites/deck/{card_class}.png').convert_alpha()
            self.card_class = card_class
         
        self.image = pygame.transform.scale(self.image, (130,180))
        self.rect = self.image.get_rect(topleft = (x_pos,y_pos))
        self.card_class = card_class
    
    def player_card_used(self):
        self.image = pygame.transform.scale(self.image, (130,180))
        self.rect = self.image.get_rect(topleft = (400,300))


class player_set(pygame.sprite.Sprite):
    def __init__(self, player_class):
        super().__init__()
        self.health = 5
        self.image = pygame.image.load(f'sprites/player/player_{player_class}_{self.health}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (130,180))
        self.rect = self.image.get_rect(topleft = (535,500))
        self.player_class = player_class


    # Stats
    def player_update(self):
        self.image = pygame.image.load(f'sprites/player/player_{self.player_class}_{self.health}.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (130,180))
        self.rect = self.image.get_rect(topleft = (535,510))


class enemy_set(pygame.sprite.Sprite):
    def __init__(self, enemy_class, class_code, x_pos, y_pos):
            super().__init__()
            health = 1
            self.image = pygame.image.load(f'sprites/enemy/enemy_{enemy_class}.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (130,180))
            self.rect = self.image.get_rect(topleft = (x_pos,y_pos))
            self.enemy_class = enemy_class
            self.enemy_class_code = class_code