class Settings():
    """Класс для хранения всех настроек игры Alien Invasion"""

    def __init__(self):
        """Инициализация постоянных настроек игры"""
        #Параметры экрана для оконного режима:
        # self.screen_width = 1600
        # self.screen_height = 810
        # Black color:
        self.bg_color = (0, 0, 0)
        #Blue color:
        # self.bg_color = (17, 30, 108)
        # #Настройки корабля
        self.ship_limit = 3
        #Параметры снаряда
        self.bullet_width = 2
        self.bullet_height = 20
        self.bullet_color = (48, 255, 0)
        self.bullets_allowed = 5

        #Настройки пришельцев
        self.fleet_drop_speed = 10
        #Темп ускорения игры
        self.speedup_scale = 1.1
        #Темп роста награды за пришельцев
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализация настроек изменяющихся в ходе игры"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        #fleet_direction = 1 обозначает движение вправо, а -1 - влево
        self.fleet_direction = 1
        #Подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        """Увеличение  настроек скорости"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        #Проверка увеличения награды
        #print(self.alien_points)
