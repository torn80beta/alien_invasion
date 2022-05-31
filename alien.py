import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Класс представляющий одного пришельца"""

    def __init__(self, ai_game):
        """Инициализация пришельца и задание начальной позиции"""
        super().__init__()
        self.screen = ai_game.screen

        #Загрузка изображения пришельца и назначение атрибута rect
        self.image = pygame.image.load('images/alien_1.png')
        self.rect = self.image.get_rect()

        #Каждый новый пришелец появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Сохранение точной горизонтальной позиции пришельца
        self.x = float(self.rect.x)
