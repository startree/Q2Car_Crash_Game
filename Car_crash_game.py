import pygame
import os
import random
import pygame
from sys import exit
from pygame.locals import *

#initialize Pygame
pygame.init()

#count the score
def display_score():
    current_time = int((pygame.time.get_ticks()-start_time)/1000)
    score_surf = test_font.render("Score:{}".format(current_time),False,'Black')
    score_rect = score_surf.get_rect(center = (400,30))
    screen.blit(score_surf,score_rect)
    return current_time 

def set_Obstacle(Obstacle_list):
    if Obstacle_list: 
        for car_rect in Obstacle_list:
            if car_rect.x >= -100:
                n = random.randint(200,500)
                if car_rect.x > n:
                    car_rect.x -= 4
                    car_rect.y -= 1
                elif car_rect.x <= n:
                    car_rect.x -= 4
                    car_rect.y += 1
                screen.blit(redcar_surf,car_rect)
            else: Obstacle_list.remove(car_rect)

        return(Obstacle_list)
    return[]
        
#set the screen size
screen = pygame.display.set_mode([800,400])

#set the clock
clock = pygame.time.Clock()
start_time = 0
score = 0

# change the relative directory
base_path = os.path.dirname(__file__)
test_font = pygame.font.Font(os.path.join(base_path,'font/pixeltype/Pixeltype.ttf'),50)

#load the image
bg_surf = pygame.image.load(os.path.join(base_path, 'Graphic/road.png')).convert()
bg_rect = bg_surf.get_rect(center = (400,200))
redcar_surf = pygame.image.load(os.path.join(base_path,'Graphic/redcar.png')).convert_alpha()
bluecar_surf = pygame.image.load(os.path.join(base_path,'Graphic/bluecar.png')).convert_alpha()

player_surf = pygame.image.load(os.path.join(base_path,'Graphic/yellowcar.png')).convert_alpha()
player_rect = player_surf.get_rect(midbottom =(80,365))
player_direction = 0

#intro screen
intro_car = pygame.image.load(os.path.join(base_path,'Graphic/yellowcar.png'))
intro_car = pygame.transform.rotozoom(intro_car,45,2)
intro_car_rect = intro_car.get_rect(center = (400,170))

game_name = test_font.render('My Car Race', False,'#420D09')
game_name_rect = game_name.get_rect(center = (400,50))

game_message = test_font.render("PRESS SPACE TO RESTART THE GAME",False,"#420D09")
game_message_rect = game_message.get_rect(midbottom =(400,350))
# Load the sound file
sound = pygame.mixer.Sound(os.path.join(base_path,'audio/bg.mp3'))

# Set the volume of the sound
sound.set_volume(0.1)

# Create a custome event, Schedule the event to be triggered every 1 seconds
Obstacle_event = USEREVENT + 1
pygame.time.set_timer(Obstacle_event,1500)

Obstacle_list = []

#main game loop
running = True
game_active = False
bg_speed = 2
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sound.stop()
            pygame.quit()
            exit()
        
        if game_active:
            # Play the sound in a loop
            sound.play(-1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_direction = -2
                elif event.key == pygame.K_DOWN:
                    player_direction = 2
            if event.type == Obstacle_event:
                Obstacle_list.append(redcar_surf.get_rect(midbottom =(random.randint(900,1100),random.randint(200,365))))
                Obstacle_list.append(bluecar_surf.get_rect(midbottom =(random.randint(900,1100),random.randint(50,300))))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = True
                game_active = True
                start_time = pygame.time.get_ticks()
    if game_active:
        # Move the background
        bg_rect.x -= bg_speed
        if bg_rect.x <= -800:
            bg_rect.x = 0
        screen.blit(bg_surf,bg_rect)
        
        # Display score
        display_score()
        
        # Set obstacle car
        set_Obstacle(Obstacle_list)
        
        # Move the player car
        player_rect.y += player_direction
        screen.blit(player_surf,player_rect)
        # Collicion
        for car_rect in Obstacle_list:
            if car_rect.colliderect(player_rect) or player_rect.y < 0 or player_rect.y > 380 :
                score = display_score()
                game_active = False
                sound.stop()
                Obstacle_list=[]
                player_rect = player_surf.get_rect(midbottom =(80,165))
    else:
        # Game pause and display information
        screen.fill("#EEDC82")
        screen.blit(intro_car,intro_car_rect)
        screen.blit(game_name,game_name_rect)
        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            score_message = test_font.render("Score:{}".format(score),False,'#420D09')
            score_message_rect=score_message.get_rect(center=(400,350))
            screen.blit(score_message,score_message_rect)
    pygame.display.update()
    clock.tick(70)   
    
pygame.QUIT()