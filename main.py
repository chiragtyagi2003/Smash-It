#main file for space_smash game

import pygame
from pygame.sprite import Group
#from aesteroid import Aesteroid
from settings import Settings
from spaceship import Spaceship
import gamefunctions as gf
from game_stats import Gamestats
from scoreboard import Scoreboard
from button import Button


def run_game():
    """Initialise the game and create a screen object."""
    pygame.init() #initializes the necessary BG settings for pygame to run.
    ss_settings = Settings() #making instance of settings class to access settings
    screen = pygame.display.set_mode((ss_settings.screen_width, ss_settings.screen_height))
    pygame.display.set_caption("Smash It!") #sets the title of game.

    #make the play button
    play_button = Button(ss_settings=ss_settings, screen=screen, msg="PLAY")

    #create an instance of gamestats to store the game statistics and create a scoreboard
    stats = Gamestats(ss_settings=ss_settings)
    sb = Scoreboard(ss_settings=ss_settings, screen=screen, stats=stats)


    #making a spaceship (instance)
    spaceship = Spaceship(ss_settings=ss_settings, screen=screen)

    #making a group to store sparks in
    sparks = Group()  #this group is created outside of the while loop so we 
                      # don't  create a new group each time the loop cycles.

    #make a group of aesteroids
    aesteroids = Group()

    #create a fleet of aesteroids
    gf.create_fleet(ss_settings=ss_settings, screen=screen, aesteroids=aesteroids, spaceship=spaceship)

    #the main loop for game
    while True:


        #event loop
        gf.check_events(spaceship=spaceship,ss_settings=ss_settings, screen=screen, sparks=sparks, stats=stats, play_button=play_button, aesteroids=aesteroids, sb=sb)

        if stats.game_active:
            #update the spaceship pos
            spaceship.update()

            #update the sparks pos
            gf.update_spark(aesteroids=aesteroids, sparks=sparks, ss_settings=ss_settings, spaceship=spaceship, screen=screen, stats=stats, sb=sb)

            
            #update the aesteroids pos after updating spark pos
            gf.update_aesteroids(ss_settings=ss_settings, aesteroids=aesteroids, spaceship=spaceship, stats=stats, screen=screen, sparks=sparks, sb=sb)

        #update screen
        gf.update_screen(ss_settings=ss_settings, screen=screen, spaceship=spaceship, sparks=sparks, aesteroids=aesteroids, stats=stats, play_button=play_button, sb=sb)
      

        

run_game() #calling the function to initialize the game

