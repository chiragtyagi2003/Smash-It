#class for controlling aesteroid properties

import pygame
from pygame.sprite import Sprite

class Aesteroid(Sprite):
    """a class to represent a single aesteroid in the fleet."""

    def __init__(self,ss_settings, screen):
        """initialize the aesteroid and set its starting pos"""

        super().__init__()
        self.screen = screen
        self.ss_settitngs = ss_settings

        #loading the aesteroid img and setting its rect attribute
        self.image = pygame.image.load('images/cosmic_65.jpg')  ######add image path here
        self.rect = self.image.get_rect()

        #start each new aesteroid near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store the aesteroid's exact pos
        self.x = float(self.rect.x)


    def check_edges(self):
        """returns True if aesteroid is at the edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True

        elif self.rect.left <= 0:
            return True

    def update(self):
        """move the aesteroid to the right or left"""
        self.x += self.ss_settitngs.aesteroid_speed_factor * self.ss_settitngs.fleet_direction
        self.rect.x = self.x
        


    def blitme(self):
        """Draw the aesteroids at its current location."""
        self.screen.blit(self.image, self.rect)