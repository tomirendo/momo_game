import pygame

class Obstacle(pygame.sprite.Sprite):
    '''A class representing obstacles in the pac man game'''

    def __init__(self,image,position):
        super().__init__()
        self.__image = image
        self.__position = position
        self.rect = self.__image.get_rect()
        self.rect.topleft = self.__position


    def get_image(self):
        return self.__image

    def get_position(self):
        return self.__position
