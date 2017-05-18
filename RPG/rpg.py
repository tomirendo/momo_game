#!/usr/local/bin/python3.5
import pygame
import pygame.locals 

from path import street


done = False 
background = pygame.image.load("./background.jpg")
forground = pygame.image.load("./forground.png")
character = pygame.image.load("./character.png")

x,y = 0,0
STEP = 10
middle = 300
down = 550


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1024,768))
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pressed_keys =  pygame.key.get_pressed()

        if pressed_keys[pygame.K_RIGHT]: x+= STEP
        if pressed_keys[pygame.K_LEFT]: x-= STEP
        if pressed_keys[pygame.K_DOWN]: y-= STEP
        if pressed_keys[pygame.K_UP]: y+= STEP
     
        screen.fill((0,0,0))
        print(street.get_position(x,y))
        screen.blit(character, street.get_position(x, y))
        pygame.display.flip()


    while pygame.event.wait().type != pygame.locals.QUIT:
        pass


