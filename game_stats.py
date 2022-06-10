class GameStats():
    """Отслеживание статистики для игы"""

    def __init__(self, ai_game):
        """Инициализация статистики"""
        self.settings = ai_game.settings
        self.reset_stats()
        #Запуск игры в неактивном состоянии
        self.game_active = False
        #Чтение рекорда из файла
        with open('high_score.txt') as file:
            self.high_score = int(file.read().strip())

    def reset_stats(self):
        """Инициализирует статистику изменяющуюся в ходе игры"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
