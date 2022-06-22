class Gamestats():
    """track statistics for main.py"""

    def __init__(self, ss_settings):
        """initialize the statistics"""
        self.ss_settings = ss_settings
        self.reset_stats()
        #start the game in an inactive state so that player can play it using play button
        self.game_active = False

        #high score should never be reset
        self.high_score = 0

    def reset_stats(self):
        """initialize stats that can change during the game."""
        #no. of spaceships left
        self.spaceship_left = self.ss_settings.spaceship_limit
        self.score = 0
        self.level = 1
