import pygame
import random
import os

class Shopper():
    '''a shopper at the store'''

    HEIGHT = 200
    WIDTH = 60

    def __init__(self,name,conv):
        '''create a new shopper'''
        self.__name = name
        self.__conv = conv
        path = os.path.abspath('Neta/Human.png')
        self.__image = pygame.image.load(path)



    def get_conversation(self):
        '''return the shopper's conversation'''
        return self.__conv




