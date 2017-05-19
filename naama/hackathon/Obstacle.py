
import random
import pygame
import os


class Obstacle(pygame.sprite.Sprite):

    SPEED = 5
    COOL_DOWN_FREQUENCY = 5

    def __init__(self, image, ground_level, momo_x_pos, screen_width, speed):
        super().__init__()
        self.image = image
        self.__x_pos = random.randint(momo_x_pos + 200, screen_width)
        self.__y_pos = ground_level + 50
        self.__cool_down_count = 0
        self.__speed = speed
        self.rect = self.image.get_rect()
        self.topleft = 0, 0

    def get_cooldown_count(self):
        return self.__cool_down_count

    def update_cooldown_count(self):
        if self.__cool_down_count <= self.COOL_DOWN_FREQUENCY:
            self.__cool_down_count += 1
        else:
            self.__cool_down_count = 0

    def get_x_position(self):
        return self.__x_pos

    def get_y_position(self):
        return self.__y_pos

    def get_position(self):
        return self.__x_pos, self.__y_pos

    def get_image(self):
        return self.image

    def move(self):
        self.__x_pos -= self.SPEED
        self.set_rect_top()

    def set_rect_top(self):
        self.rect.topleft = self.__x_pos, self.__y_pos


