import pygame
from pygame.sprite import Sprite


class Space(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.image = pygame.image.load('images/space_1.bmp')
        self.rect = self.image.get_rect()
        self.x = float(self.rect.x)
