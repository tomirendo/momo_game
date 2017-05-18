import pygame
import random
import os

class Shopper():
    '''a shopper at the store'''

    HEIGHT = 200
    WIDTH = 60

    def __init__(self,name,shopping_list):
        '''create a new shopper'''
        self.__name = name
        self.__shopping_list = shopping_list
        path = os.path.abspath('Neta/Human.jpg')
        self.__image = pygame.image.load(path)




    def get_image(self):
        '''get the shopper's image'''
        return self.__image


    def get_shopping_list(self):
        '''get the shopper's shopping list'''
        return self.__shopping_list



