import pygame
import os

POSITION = 'positiom'
IMAGE = 'image'
WIDTH = 'width'

#vegetable constants:
TOMATOES = 'tomatoes'
TOMATO_POSITION = (14,118)
CARROTS = 'carrots'
CARROT_POSITION = (119,198)
CUCUMBERS = 'cucumbers'
CUCUMBER_POSITION = (199,330)


class GreenGrocerGame():
    '''The green Grocer minigame for the Momo game'''

    STEPSIZE = 3
    GROCER_IMAGE_WIDTH = 50


    def __init__(self,game):
        '''Initiate the game object'''
        self.__game = game
        image_path = os.path.abspath('Neta/temp_screen.jpg')
        self.__bg_image = pygame.image.load(image_path)
        self.__screen = self.__game.get_screen()
        self.initiate_grocer()



    def initiate_grocer(self):
        '''initiate the grocer object'''
        self.__grocer = {}
        human_image_path = os.path.abspath('Neta/Human.jpg')
        self.__grocer[IMAGE] = pygame.image.load(human_image_path)
        self.__grocer[POSITION] = (50,250)
        self.__grocer[WIDTH] = GreenGrocerGame.GROCER_IMAGE_WIDTH

    def initiate_stalls(self):
        '''initiate the stalls'''
        self.__stalls = {}
        self.__stalls['TOMATOES'] = {}


    def get_vegetables(self):
        '''add_vegetables to the basket'''
        


    def move_grocer(self):
        '''move the grocer according to pressed keys'''
        pressed_keys = self.__game.get_keys_pressed()
        if pressed_keys[pygame.K_LEFT] and self.__grocer[POSITION][0] >= 0:
            self.__grocer[POSITION] = (self.__grocer[POSITION][0] - GreenGrocerGame.STEPSIZE, self.__grocer[POSITION][1])

        if pressed_keys[pygame.K_RIGHT] and self.__grocer[POSITION][0] <= self.__game.SCREEN_WIDTH - self.__grocer[WIDTH]:
            self.__grocer[POSITION] = (self.__grocer[POSITION][0] + GreenGrocerGame.STEPSIZE, self.__grocer[POSITION][1])



    def main_loop(self):
        '''the main loop for the minigame'''
        self.__screen.blit(self.__bg_image,(0,60))
        self.move_grocer()
        self.__screen.blit(self.__grocer[IMAGE],self.__grocer[POSITION])
        return True



    def get_music(self):
        '''get the game's background music'''
        return None



    def get_loop(self):
        '''get the game's main loop'''
        return self.main_loop