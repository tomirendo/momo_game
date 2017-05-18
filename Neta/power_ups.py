import pygame
import os

SIZE = 55
class PowerUps():

    def __init__(self,function,image,price,position):
        '''create a new power up object'''
        self.__function = function
        file_path = os.path.abspath(image)
        self.__image = pygame.image.load(file_path)
        self.__price = price
        self.__position = position


    def get_function(self):
        '''return the powerUp's function'''
        return self.__function

    def get_image(self):
        '''return the powerUps image representation'''
        return self.__image

    def get_price(self):
        '''return the powerUp's price'''
        return self.__price

    def get_position(self):
        '''get the powerup's position on the screen'''
        return self.__position



    def hit_power_up(self,position):
        '''return true if the position is in the power up button, False otherwise'''
        if position[0] >= self.__position[0] and position[0] <= self.__position[0] + SIZE:
            if position[1] >= self.__position[1] and position[1] <= self.__position[1] + SIZE:
                return True