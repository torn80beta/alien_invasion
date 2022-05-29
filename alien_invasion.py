import sys
import pygame
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализация игры и создание игровых ресурсов"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion by Alex Ostrovskyi')
        self.ship = Ship(self)

    def _check_events(self):
        """Отслеживание событий клавиатуры и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Перемещение корабля вправо клавишей -->
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True

            # Остановка корабля ели клавишу отпустили
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False



    def _update_screen(self):
        """Перерисовка экрана при каждом проходе цикла"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        """Отображение последнего прорисованого экрана"""
        pygame.display.flip()

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()





if __name__ == '__main__':
    """Создание экземпляра и запуск игры."""
    ai = AlienInvasion()
    ai.run_game()
