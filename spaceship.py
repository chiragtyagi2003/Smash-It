#class for spaceship
import pygame
from pygame.sprite import Sprite

class Spaceship(Sprite):
    """defines the spaceship"""


    def __init__(self, ss_settings, screen):
        """initialise the sprite and ship and set its starting position"""
        super().__init__()
        self.screen = screen
        self.ss_settings = ss_settings

        #load the spaceship image and get its rect attributes
        self.image = pygame.image.load("images\spaceship.jpg")
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        #start each spaceship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #store a decimal value for spaceship's center
        self.center = float(self.rect.centerx)

        #setting the movements flag
        self.moving_right = False
        self.moving_left = False


    def center_spaceship(self):
        """Center the spaceship on the screen"""
        self.center = self.screen_rect.centerx
    def update(self):
        """update's ship's position based on flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ss_settings.spaceship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ss_settings.spaceship_speed_factor

        #update rect object from self.center
        self.rect.centerx = self.center
    
    def blitme(self):
        """draw the image at its current location"""
        self.screen.blit(self.image,self.rect)


    
    