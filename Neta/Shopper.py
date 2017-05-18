import pygame
import random
import os
import json

class Shopper():
    '''a shopper at the store'''

    HEIGHT = 200
    WIDTH = 60

    def __init__(self,name,shopping_list,dialogue):
        '''create a new shopper'''
        self.__name = name
        self.__shopping_list = shopping_list
        path = os.path.abspath('Neta/Human.jpg')
        self.__image = pygame.image.load(path)

        json_file_path = os.path.abspath(dialogue)
        json_file = open(json_file_path)
        json_str = json_file.read()
        self.__dialogue = json.loads(json_str)





    def get_image(self):
        '''get the shopper's image'''
        return self.__image


    def get_shopping_list(self):
        '''get the shopper's shopping list'''
        return self.__shopping_list


    def get_dialogue(self):
        '''get the shopper's dialogue'''
        return self.__dialogue



