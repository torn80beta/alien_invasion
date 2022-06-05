class GameStats():
    """Отслеживание статистики для игы"""

    def __init__(self, ai_game):
        """Инициализация статистики"""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Инициализирует статистику изменяющуюся в ходе игры"""
        self.ships_left = self.settings.ship_limit
