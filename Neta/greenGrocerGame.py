import pygame
import os

class GreenGrocerGame():
    '''The green Grocer minigame for the Momo game'''


    def __init__(self,game):
        '''Initiate the game object'''
        self.__game = game
        image_path = os.path.abspath('Neta/temp_screen.jpg')
        self.__bg_image = pygame.image.load(image_path)
        self.__screen = self.__game.get_screen()
        self.__grocer = {}
        human_image_path = os.path.abspath('Neta/Human.jpg')
        self.__grocer['image'] = pygame.image.load(human_image_path)
        self.__grocer['position'] = (50,250)




    def main_loop(self):
        '''the main loop for the minigame'''
        self.__screen.blit(self.__bg_image,(0,60))
        self.__grocer['position'] = (self.__grocer['position'][0] + 3, self.__grocer['position'][1])
        self.__screen.blit(self.__grocer['image'],self.__grocer['position'])
        return True



    def get_music(self):
        '''get the game's background music'''
        return None



    def get_loop(self):
        '''get the game's main loop'''
        return self.main_loop