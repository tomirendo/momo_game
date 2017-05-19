import pygame
import os

class Momo(pygame.sprite.Sprite):
    '''Momo'''

    def __init__(self,position):
        '''create the instance of Momo'''
        super().__init__()
        self.__position = position
        self.__image = pygame.image.load(os.path.abspath('crazyPacManBlitz/momo_front.png'))
        self.rect = self.__image.get_rect()
        self.rect.topleft = self.__position


    def get_image(self):
        '''get Momo's image'''
        return self.__image


    def set_position(self,position):
        '''set Momo's positions'''
        self.__position = position
        self.rect.topleft = self.__position


    def get_position(self):
        '''get Momo's position'''
        return self.__position

