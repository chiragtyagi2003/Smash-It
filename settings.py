#module to contain all settings of space smash

class Settings():
    """a class to contain all settings of space smash."""
    
    def __init__(self):
        """initialize the game's static settings."""

        #screen settings
        self.screen_width = 1400
        self.screen_height = 800
        self.bg_color = (0,0,0)

        #spaceship's  static settings
        self.spaceship_limit = 3
        
        #spark's static settings
        self.spark_width = 3
        self.spark_height = 40
        self.spark_color = (255, 255, 255)
        self.spark_allowed = 3
        
        #aesteroid's static settings
        self.fleet_drop_speed = 10

        #how quickly the game speed's up
        self.speedup_scale = 1.1

        #how quickly the aesteroid point value increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings() #we can use a member function as an attribute in its class

    def initialize_dynamic_settings(self):
        """initialize settings that change throught the game"""

        #spaceship's dynamic settings
        self.spaceship_speed_factor = 1.5
       
        #spark's dynamic settings
        self.spark_speed_factor = 3

        #aesteroid's dynamic settings
        self.aesteroid_speed_factor = 1.5

        #fleet direction of 1 represents right and -1 represents left
        self.fleet_direction = 1

        #scoring
        self.aesteroid_points = 50

    def increase_speed(self):
        """increase speed settings and aesteroid point values"""
        self.spaceship_speed_factor *= self.speedup_scale
        self.spark_speed_factor *= self.speedup_scale
        self.aesteroid_speed_factor *= self.speedup_scale
        self.aesteroid_points = int(self.aesteroid_points * self.score_scale)
        #print(self.aesteroid_points)
