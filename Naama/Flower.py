
import random
import pygame


class Flower(pygame.sprite.Sprite):

    LAND_HEIGHT = 410
    MAX_HEIGHT = 200
    SCREEN_WIDTH = 800
    FLOWER_SPEED = 10

    def __init__(self, image):
        self.__x_position = self.SCREEN_WIDTH
        self.__y_position = random.randint(self.LAND_HEIGHT - self.MAX_HEIGHT, self.LAND_HEIGHT)
        self.__image = image

    def get_position(self):
        return self.__x_position, self.__y_position

    def move(self):
        self.__x_position -= self.FLOWER_SPEED

    def get_x_pos(self):
        return self.__x_position

    def get_image(self):
        return self.__image