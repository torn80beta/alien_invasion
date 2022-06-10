class GameStats():
    """Отслеживание статистики для игы"""

    def __init__(self, ai_game):
        """Инициализация статистики"""
        self.settings = ai_game.settings
        self.reset_stats()
        #Запуск игры в неактивном состоянии
        self.game_active = False

    def reset_stats(self):
        """Инициализирует статистику изменяющуюся в ходе игры"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
