import pygame
import os

class PowerUps():

    def __init__(self,function,image,price):
        '''create a new power up object'''
        self.__function = function
        file_path = os.path.abspath(image)
        self.__image = pygame.image.load(file_path)
        self.__price = price


    def get_function(self):
        '''return the powerUp's function'''
        return self.__function

    def get_image(self):
        '''return the powerUps image representation'''
        return self.__image

    def get_price(self):
        '''return the powerUp's price'''
        return self.__price





