#!/usr/local/bin/python3.5
import pygame
import pygame.locals 

from character import momo

done = False 

x,y = 0,0
STEP = .10
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


        if pressed_keys[pygame.K_RIGHT]: momo.step_right()
        if pressed_keys[pygame.K_LEFT]: momo.step_left()
     
        screen.fill((0,0,0))
        momo.draw_on_screen(screen)
        pygame.display.flip()


    while pygame.event.wait().type != pygame.locals.QUIT:
        pass


