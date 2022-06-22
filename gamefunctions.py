import sys
from time import sleep
import pygame
from aesteroid import Aesteroid
from spark import Spark
#from spaceship import Spaceship


def check_keydown_events(event, spaceship, ss_settings, screen, sparks):
    """responds to key presses."""
    if event.key == pygame.K_RIGHT: #case for when right key is pressed down
        spaceship.moving_right = True

    elif event.key == pygame.K_LEFT: #case for when left key is pressed down
        spaceship.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_spark(ss_settings=ss_settings, screen=screen, spaceship=spaceship, sparks=sparks)
        
    


def check_play_buttons(stats, play_button, mouse_x, mouse_y, ss_settings,screen, spaceship, aesteroids, sparks, sb):
    """start a new game when the player clicks play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #reset the game settings
        ss_settings.initialize_dynamic_settings()
        
        #hide the mouse cursor
        pygame.mouse.set_visible(False)

        #reset the game statistics
        stats.reset_stats()
        stats.game_active = True  #sets the flag to be true which controls whether to create a new game or not
        
        #reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_spaceships()

        #empty the list of aesteroids and sparks
        aesteroids.empty()
        sparks.empty()

        #create a new fleet  and center the spaceship
        create_fleet(ss_settings=ss_settings, screen=screen, spaceship=spaceship, aesteroids=aesteroids)
        spaceship.center_spaceship()


def check_keyup_events(event, spaceship):
    """responds to key releases."""
    if event.key == pygame.K_RIGHT: #case for when right key is released
        spaceship.moving_right = False

    elif event.key == pygame.K_LEFT: #case for when left key is released
        spaceship.moving_left = False

def check_events(spaceship, ss_settings, screen, sparks, stats, play_button, aesteroids, sb):
    """respond to keypress and mouse events."""
    for event in pygame.event.get(): #recieves the event occurred
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN: #when any key is pressed down
            check_keydown_events(event=event, spaceship=spaceship, screen=screen, sparks=sparks, ss_settings=ss_settings)
           
        elif event.type == pygame.KEYUP: #when any key is released
            check_keyup_events(event, spaceship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_buttons(stats=stats, play_button=play_button, mouse_x=mouse_x, mouse_y=mouse_y, ss_settings=ss_settings, screen=screen, aesteroids=aesteroids, spaceship=spaceship, sparks=sparks, sb=sb)


def update_screen(ss_settings, screen, spaceship, sparks,stats, aesteroids, play_button, sb):
    """update the images on the screen and flip to the new screen."""
    
    #fill the screen with BG color
    screen.fill(ss_settings.bg_color)

    #redraw all bullets behind spaceship and planets
    for spark in sparks.sprites():
        spark.draw_spark()


    #drawing the image
    spaceship.blitme() #draws spaceship
    #aesteroid.blitme() #draws aesteroid
    aesteroids.draw(screen) #draws the row of aesteroids

    #draw the score information
    sb.show_score()


    #draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()


    #mak the most recent screen visible that is screen is updated each time through the loop

    pygame.display.flip()

def update_spark(aesteroids, sparks, spaceship, ss_settings, screen, stats, sb):
    """update the pos of sparks and get rid of old sparks"""
    sparks.update() #when you call update fun on a group(here sparks) , update is automatically
                        #called for each sprite in the group.

    #getting rid of bullets that have disappeared
    for spark in sparks.copy():
        if spark.rect.bottom == 0:
            sparks.remove(spark)

    check_spark_aeteroid_collision(ss_settings=ss_settings, screen=screen, spaceship=spaceship, sparks=sparks, aesteroids=aesteroids, stats=stats, sb=sb)        

    
    
def check_spark_aeteroid_collision(ss_settings, screen, stats, sb, spaceship, aesteroids, sparks):
    #check for any sparks that have hit the aesteroids
    # if so , get rid of the bullet and the aesteroids
    collisions = pygame.sprite.groupcollide(sparks, aesteroids, True, True)

    if len(aesteroids) == 0:
        # If the entire fleet is destroyed , start a new level
        sparks.empty()
        ss_settings.increase_speed()

        #increase the level
        stats.level += 1
        sb.prep_level()

        create_fleet(ss_settings=ss_settings, screen=screen, spaceship=spaceship, aesteroids=aesteroids)

    if collisions:
        for aesteroids in collisions.values():
            stats.score += ss_settings.aesteroid_points * len(aesteroids)
            sb.prep_score()

        check_high_score(stats=stats, sb=sb )


def fire_spark(ss_settings, screen, spaceship, sparks):
    """fire a spark if limit not reached yet"""
    #create a new spark each time spacebar is pressed and add it to the sparks group
    if len(sparks) < ss_settings.spark_allowed:
        new_spark = Spark(ss_settings=ss_settings, screen=screen, spaceship=spaceship)
        sparks.add(new_spark)

def get_number_aesteroids(ss_settings, aesteroid_width):
    """Determine the number of aesteroids that fits in a row."""
    available_space_x = ss_settings.screen_width - (2 * aesteroid_width)
    number_aesteroids_x = int(available_space_x/(2*aesteroid_width))
    return number_aesteroids_x

def get_number_rows(ss_settings, spaceship_height, aesteroid_height):
    """Determine the number of rows of aesteroids that fits on the screen"""
    available_space_y = (ss_settings.screen_height - (3*aesteroid_height) - spaceship_height)
    number_rows = int(available_space_y/(2*aesteroid_height))
    return number_rows

def create_aesteroid(ss_settings, screen, aesteroids, aesteroid_number, row_number):
    """create an aesteroid and place it in the row"""
    #creates an aesteroid and place it in the row
    aesteroid = Aesteroid(ss_settings=ss_settings, screen=screen)
    aesteroid_width = aesteroid.rect.width
    aesteroid.x = aesteroid_width + (2 * aesteroid_width * aesteroid_number)
    aesteroid.rect.x = aesteroid.x
    aesteroid.rect.y = aesteroid.rect.height + (2 * aesteroid.rect.height * row_number)
    aesteroids.add(aesteroid)




def create_fleet(ss_settings, screen, aesteroids, spaceship):
    """create a full fleet of aesteroids"""
   
    #create an aesteroid and find the number of aesteroids in a row
    ##spacing between each aesteroid is equal to one aesteroid width
    aesteroid = Aesteroid(ss_settings=ss_settings, screen=screen)
    number_aesteroids_x = get_number_aesteroids(ss_settings=ss_settings, aesteroid_width=aesteroid.rect.width)
    number_rows = get_number_rows(ss_settings=ss_settings, spaceship_height=spaceship.rect.height, aesteroid_height=aesteroid.rect.height)
    
    #create the fleet of aesteroids
    for row_number in range(number_rows): 
        for aesteroid_number in range(number_aesteroids_x):
            create_aesteroid(ss_settings=ss_settings, screen=screen, aesteroids=aesteroids, aesteroid_number=aesteroid_number, row_number=row_number)


def check_fleet_edges(ss_settings, aesteroids):
    """respond appropriatley if any aesteroids have reached an edge"""
    for aesteroid in aesteroids.sprites():
        if aesteroid.check_edges(): #if its true
            change_fleet_direction(ss_settings=ss_settings, aesteroids=aesteroids)
            break #break beacuase our problem will be solved even if one aesteroid reaches the screen

def change_fleet_direction(ss_settings, aesteroids):
    """drop the entire fleet and change the fleet's direction"""
    for aesteroid in aesteroids.sprites():
        aesteroid.rect.y += ss_settings.fleet_drop_speed

    ss_settings.fleet_direction *= -1

def update_aesteroids(ss_settings ,aesteroids, spaceship, stats, sb, screen, sparks):
    """checks if the fleet is at either edge and then
    updates the position of all aesteroids in the fleet"""
    check_fleet_edges(ss_settings=ss_settings, aesteroids=aesteroids)
    aesteroids.update()

    #looks for aesteroid-ship collision
    if pygame.sprite.spritecollideany(spaceship , aesteroids):
        #print("Spaceship Hit!!!!")
        spaceship_hit(ss_settings=ss_settings, stats=stats, screen=screen, spaceship=spaceship, aesteroids=aesteroids, sparks=sparks, sb=sb)

    #looks for aesteroids hitting the bottom of the screen
    check_aesteroids_bottom(ss_settings=ss_settings,stats=stats,screen=screen,spaceship=spaceship,aesteroids=aesteroids,sparks=sparks, sb=sb)

def spaceship_hit(ss_settings, stats, screen, spaceship, aesteroids, sparks, sb):
    """respond to spaceship being hit by aesteroid"""
    if stats.spaceship_left > 0:
        #decrement the no. of spacehsip_left
        stats.spaceship_left -= 1
        
        #update scoreboard
        sb.prep_spaceships()

        #empty the list of aesteroids and sparks as we want a new whole game reset after collision
        aesteroids.empty()
        sparks.empty()

        #create a new fleet and center the spaceship
        create_fleet(ss_settings=ss_settings, screen=screen, spaceship=spaceship, aesteroids=aesteroids)
        spaceship.center_spaceship()

        #pause after collision
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aesteroids_bottom(ss_settings,stats, screen, spaceship, aesteroids, sparks, sb):
    """check if any aesteroids have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for aesteroid in aesteroids.sprites():
        if aesteroid.rect.bottom >= screen_rect.bottom:
            #treat this same as if spaceship was hit
            spaceship_hit(ss_settings=ss_settings, screen=screen, stats=stats, spaceship=spaceship, aesteroids=aesteroids, sparks=sparks, sb=sb)
            break


def check_high_score(stats,sb):
    """check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
