import pygame
import os


class Runner(pygame.sprite.Sprite):

    GROUND_LEVEL = 410
    MAX_ROUND_PER_JUMP = 30
    JUMP_DURATION = 6
    JUMP_COOL_DOWN_ROUNDS = 50
    FIXED_X_POSITION = 300
    MOMO_IMAGE = pygame.image.load(os.path.abspath('momo_skate.png'))

    def __init__(self):
        super().__init__()
        self.rect = self.MOMO_IMAGE.get_rect()
        self.__scores = 0
        self.__x_position = self.FIXED_X_POSITION
        self.__y_position = self.GROUND_LEVEL
        self.__rounds_in_jump = 0
        self.__jump_cool_down_count = 0
        self.rect.topleft = 0, 0

    def jump(self):
        if self.__rounds_in_jump < self.MAX_ROUND_PER_JUMP:
            self.__y_position -= self.JUMP_DURATION
            self.__rounds_in_jump += 1
        else:
            if self.__jump_cool_down_count < self.JUMP_COOL_DOWN_ROUNDS:
                self.__jump_cool_down_count += 1
            else:
                self.__jump_cool_down_count = 0
            self.__y_position += 5
        self.set_rect_top()

    # def flip(self):
    #     pygame.transform.rotate(self.__image, 30)
    #     return

    def slide(self):
        if self.__y_position < self.GROUND_LEVEL:
            self.__y_position += 5
            self.set_rect_top()
        self.__rounds_in_jump = 0
        return

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

    def set_rect_top(self):
        self.rect.topleft = self.__x_position, self.__y_position
