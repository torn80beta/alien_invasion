import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from space import Space
from button import Button


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализация игры и создание игровых ресурсов"""
        pygame.init()
        self.settings = Settings()
        #Fullscreen mode:
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        #Параметры экрана для оконного режима:
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.screen_width = 1600
        # self.screen_height = 810

        pygame.display.set_caption('Alien Invasion based on the Eric Matthes book by Alex Ostrovskyi')
        #Создание экземпляра для хранения игровой статистики
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.spaces = pygame.sprite.Group()
        self._create_space()
        self._create_fleet()
        #Создание кнопки Play
        self.play_button = Button(self, "Play")

    def _check_events(self):
        """Отслеживание событий клавиатуры и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запуск новой игры при нажатии кнопки Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Сброс игровой статистики
            self.stats.reset_stats()
            self.stats.game_active = True
            #Очистка списка пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            #Создание нового флота и размещение нового корабля
            self._create_fleet()
            self.ship.center_ship()
            #Скрытие указателя мыши
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш"""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновление позиции снарядов и уничтожение старых снарядов"""
        # Обновление позиции снарядов
        self.bullets.update()

        # Удаление снарядов вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Проверка попаданий в пришельцев"""
        #При обнаружении столкновения удаляется снаряд и пришелец
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        #Проверка состояния флота и создание нового если все корабли уничтожены
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _ship_hit(self):
        """Обработка столкновений корабля с пришельцем"""
        if self.stats.ships_left > 0:
            #Уменьшение количества оставшихся кораблей
            self.stats.ships_left -= 1
            #Очистка списка пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()
            #Создание нового фота и размещение нового корабля
            self._create_fleet()
            self.ship.center_ship()
            #Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Обновление позиции всех пришельцев во флоте при достижении флотом края экрана"""
        self._check_fleet_edges()
        self.aliens.update()
        #Проверка столкновений корабля с прешельцем
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #Проверка, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_bottom()

    def _create_space_patch(self, patch_x, patch_y):
        #Создание и размещение первого участка
        patch = Space(self)
        patch_width, patch_height = patch.rect.size
        patch.x = patch_width * patch_x
        patch.rect.x = patch.x
        patch.y = patch_height * patch_y
        patch.rect.y = patch.y - patch_height
        self.spaces.add(patch)

    def _create_space(self):
        #Заполнение поля участками неба
        space = Space(self)
        space_width, space_height = space.rect.size
        patches_numbers_x = self.screen_width // space_width
        patches_numbers_y = self.screen_height // space_height + 1
        total_patches = patches_numbers_x * patches_numbers_y
        for patch_y in range(patches_numbers_y):
            for patch_x in range(patches_numbers_x):
                if len(self.spaces) < total_patches:
                    self._create_space_patch(patch_x, patch_y)
            #Проверка правильности заполнения карты участками неба
            #print(len(self.spaces), 'Spaces created')

    def _space_movement(self):
        #Движение карты
        for space in self.spaces.sprites():
            space.rect.y += 1

    def _update_space(self):
        #Удаление участков карты вышедших за пределы экрана и создание новых
        self.spaces.update()
        for space in self.spaces.copy():
            if space.rect.top >= self.screen_height:
                self.spaces.remove(space)
                #Проверка правильности удаления участков звездного неба вышедших за границы экрана
                #print(len(self.spaces), 'Space removed')
        self._create_space()

    def _create_alien(self, alien_number, row_number):
        #Создание пришелца и размещение его в ряду
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _create_fleet(self):
        """Создание флота вторжения"""
        #Создание пришельца и вычисление количества пришельцев вряду
        #Интервал между пришелцами равен ширине пришельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        """Определение количества рядов помещающихся на экране"""
        ship_height = self.ship.rect.height
        available_space_y = (self.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Создание флота вторжения
        for row_number in range(number_rows // 2):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришелцами края экрана"""
        for alien in self.aliens.sprites():
            if alien._check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Проверка столкновения пришельцев с нижним краем экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Уменьшение количества оставшихся кораблей, размещение нового флота и корабля
                self._ship_hit()
                break

    def _update_screen(self):
        """Перерисовка экрана при каждом проходе цикла"""
        self.screen.fill(self.settings.bg_color)
        self.spaces.draw(self.screen)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        #Кнопка Play отображается в том случае, если игра не активна
        if not self.stats.game_active:
            self.play_button.draw_button()
        """Отображение последнего прорисованого экрана"""
        pygame.display.flip()

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self._space_movement()
                self._update_space()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()


if __name__ == '__main__':
    """Создание экземпляра и запуск игры."""
    ai = AlienInvasion()
    ai.run_game()
