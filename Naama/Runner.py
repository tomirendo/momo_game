import pygame
import os


class Runner(pygame.sprite.Sprite):

    GROUND_LEVEL = 410
    ROUNDS_PER_JUMP = 20
    JUMP_DURATION = 6
    JUMP_COOL_DOWN_ROUNDS = 50
    FIXED_X_POSITION = 300
    MOMO_IMAGE = pygame.image.load(os.path.abspath('momo_skate.png'))

    def __init__(self):
        super().__init__()
        self.__scores = 0
        self.__x_position = self.FIXED_X_POSITION
        self.__y_position = self.GROUND_LEVEL
        self.__rounds_in_jump = 0
        # self.__jump_cool_down_count = 0

    def jump(self):
        if self.__y_position == self.GROUND_LEVEL:
            self.__y_position -= 120
            self.__x_position += 1
            self.__rounds_in_jump = 0
        elif self.__rounds_in_jump < self.ROUNDS_PER_JUMP:
            self.__y_position -= 5
            self.__x_position += 1
            self.__rounds_in_jump += 1
        else:
            self.slide()

    def slide(self):
        if self.__y_position < self.GROUND_LEVEL:
            self.__y_position += 5
        if self.__x_position >= self.FIXED_X_POSITION:
            self.__x_position -= 1

    def get_image(self):
        return self.MOMO_IMAGE

    def get_position(self):
        return self.__x_position, self.__y_position

    def get_scores(self):
        return self.__scores

    def reset_state(self):
        self.__scores = 0
        self.__x_position = self.FIXED_X_POSITION
        self.__y_position = self.GROUND_LEVEL
        self.__rounds_in_jump = 0
        self.__jump_cool_down_count = 0

    def update_scores(self):
        self.__scores += 1
