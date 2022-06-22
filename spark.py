import pygame 
from pygame.sprite import Sprite

class Spark(Sprite):
    """A class to manage the sparks fired from the ship."""

    def __init__(self, ss_settings, screen, spaceship):
        """create a spark object at the spaceship's current pos."""
        super().__init__()
        self.screen = screen

        #create a spark rect at (0,0) and then set the correct pos.
        self.rect = pygame.Rect(0,0, ss_settings.spark_width, ss_settings.spark_height)
        self.rect.centerx = spaceship.rect.centerx
        self.rect.top = spaceship.rect.top

        #store the spark's pos as a decimal value
        self.y = float(self.rect.y)

        self.color = ss_settings.spark_color
        self.speed_factor = ss_settings.spark_speed_factor 

    def update(self):
        """move the spark up the screen"""
        #update decimal pos of spark
        self.y -= self.speed_factor

        #update the the rect position
        self.rect.y = self.y

    def draw_spark(self):
        """Draw the spark to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)

