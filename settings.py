class Settings():
    """Класс для хранения всех настроек игры Alien Invasion"""

    def __init__(self):
        """Инициализация настроек игры"""
        #Параметры экрана для оконного режима:
        # self.screen_width = 1200
        # self.screen_height = 800
        # Black color:
        self.bg_color = (0, 0, 0)
        #Blue color:
        # self.bg_color = (17, 30, 108)
        #Настройки корабля
        self.sheep_speed = 1.5
        #Параметры снаряда
        self.bullet_speed = 2
        self.bullet_width = 2
        self.bullet_height = 18
        self.bullet_color = (48, 255, 0)
        self.bullets_allowed = 5
