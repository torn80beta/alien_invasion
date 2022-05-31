import pygame

class Ship:
    """Класс для управления кораблем."""

    def __init__(self, ai_game):
        """Инициализация корабля и его стартовой позиции"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        """Загрузка изображения корабля и получение прямоугольника"""
        self.image = pygame.image.load('images/ship_1.png')
        self.rect = self.image.get_rect()
        """Задание позиции для каждого нового корабля"""
        self.rect.midbottom = self.screen_rect.midbottom
        #Сохранение вещественной координаты центра корабля
        self.x = float(self.rect.x)
        """Флаг перемещения"""
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Обновление позиции корабля с учетом флага"""
        # Обновляется атрибут x, не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.sheep_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.sheep_speed
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= self.settings.sheep_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.settings.sheep_speed
        #Обновление атрибута rect на основании self.x (Почему этот участок кода не работает????)
        #self.rect.x = self.x


    def blitme(self):
        """Отрисовка корабля в текущей позиции"""
        self.screen.blit(self.image, self.rect)
