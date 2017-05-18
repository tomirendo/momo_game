import pygame
import os
import time
from momo_game.Neta.Shopper import Shopper

POSITION = 'positiom'
IMAGE = 'image'
WIDTH = 'width'
HEIGHT = 'height'
SHOPPER = 'shopper'
GROCER = 'grocer'


#vegetable constants:
TOMATOES = 'tomatoes'
TOMATO_POSITION = (119,198)
CARROTS = 'carrots'
CARROT_POSITION = (14,118)
CUCUMBERS = 'cucumbers'
CUCUMBER_POSITION = (199,330)


class GreenGrocerGame():
    '''The green Grocer minigame for the Momo game'''

    STEPSIZE = 3
    GROCER_IMAGE_WIDTH = 50
    GROCER_IMAGE_HEIGHT = 200


    def __init__(self,game):
        '''Initiate the game object'''
        self.__game = game
        image_path = os.path.abspath('Neta/temp_screen.jpg')
        self.__bg_image = pygame.image.load(image_path)
        self.__screen = self.__game.get_screen()
        self.initiate_grocer()
        self.initiate_stalls()
        self.__basket = list()
        self.__last_vegetable_added = time.time()




    def initiate_grocer(self):
        '''initiate the grocer object'''
        self.__grocer = {}
        human_image_path = os.path.abspath('Neta/Human.jpg')
        self.__grocer[IMAGE] = pygame.image.load(human_image_path)
        self.__grocer[POSITION] = (50,250)
        self.__grocer[WIDTH] = GreenGrocerGame.GROCER_IMAGE_WIDTH
        self.__grocer[HEIGHT] = GreenGrocerGame.GROCER_IMAGE_HEIGHT

    def initiate_stalls(self):
        '''initiate the stalls'''
        self.__stalls = {}
        self.__stalls[TOMATOES] = {}
        self.__stalls[TOMATOES][POSITION] = TOMATO_POSITION
        path = os.path.abspath('Neta/tomato.png')
        self.__stalls[TOMATOES][IMAGE] = pygame.image.load(path)

        self.__stalls[CARROTS] = {}
        self.__stalls[CARROTS][POSITION] = CARROT_POSITION
        path = os.path.abspath('Neta/carrot.png')
        self.__stalls[CARROTS][IMAGE] = pygame.image.load(path)

        self.__stalls[CUCUMBERS] = {}
        self.__stalls[CUCUMBERS][POSITION] = CUCUMBER_POSITION
        path = os.path.abspath('Neta/cucumber.png')
        self.__stalls[CUCUMBERS][IMAGE] = pygame.image.load(path)





    def check_keys(self):
        '''move the grocer according to pressed keys
        Add vegetables if needed'''
        pressed_keys = self.__game.get_keys_pressed()
        if pressed_keys[pygame.K_LEFT] and self.__grocer[POSITION][0] >= 0:
            self.__grocer[POSITION] = (self.__grocer[POSITION][0] - GreenGrocerGame.STEPSIZE, self.__grocer[POSITION][1])

        if pressed_keys[pygame.K_RIGHT] and self.__grocer[POSITION][0] <= self.__game.SCREEN_WIDTH - self.__grocer[WIDTH]:
            self.__grocer[POSITION] = (self.__grocer[POSITION][0] + GreenGrocerGame.STEPSIZE, self.__grocer[POSITION][1])

        if pressed_keys[pygame.K_DOWN]:
            for vegetable in self.__stalls:
                if (self.__grocer[POSITION][0] > self.__stalls[vegetable][POSITION][0] and self.__grocer[POSITION][0] < self.__stalls[vegetable][POSITION][1] - GreenGrocerGame.GROCER_IMAGE_WIDTH):
                    if time.time() - self.__last_vegetable_added > 0.5 and len(self.__basket) <= 10:
                        print (len(self.__basket))
                        self.__basket.append(vegetable)
                        self.__last_vegetable_added = time.time()




    def draw_vegetables(self):
        '''draw the vegetables to the screen'''
        currentPosition = 10
        for vegetable in self.__basket:
            self.__screen.blit(self.__stalls[vegetable][IMAGE], (currentPosition, 5))
            currentPosition += 55


    def main_loop(self):
        '''the main loop for the minigame'''
        self.__screen.blit(self.__bg_image,(0,60))
        self.check_keys()
        self.__screen.blit(self.__grocer[IMAGE],self.__grocer[POSITION])
        self.draw_vegetables()
        return True



    def get_music(self):
        '''get the game's background music'''
        return None



    def get_loop(self):
        '''get the game's main loop'''
        return self.main_loop



    def create_shoppers(self):
        '''create the shoppers'''
        self.__shoppers = list()
        self.__shoppers.append(Shopper('Mike',{SHOPPER: "I want 3 tomatoes", GROCER : "OK"}))
