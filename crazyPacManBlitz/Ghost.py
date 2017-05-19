import pygame
import os
import random

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'down'
STEP_SIZE = 3
class Ghost(pygame.sprite.Sprite):
    '''The gray men in the game'''

    def __init__(self,game):
        super().__init__()
        img_path = os.path.abspath('crazyPacManBlitz/dark_person.png')
        self.__image = pygame.image.load(img_path)
        self.__position = (random.randint(0,800),random.randint(0,600))
        self.__direction = UP
        self.__game = game

        self.can_move = {LEFT : True, RIGHT : True, DOWN : True, UP : True}

        self.rect = self.__image.get_rect()
        self.rect.topleft = self.__position


    def get_image(self):
        return self.__image


    def get_position(self):
        return self.__position



    def move(self):

        if self.__direction == UP and self.__position[1] > 0 :
            if self.can_move[UP]:
                self.__position = (self.__position[0] , self.__position[1] - STEP_SIZE)

            if self.get_collisions():
                self.can_move[UP] = False

            self.can_move[DOWN] = True
            self.can_move[RIGHT] = True
            self.can_move[LEFT] = True


        if self.__direction == DOWN and self.__position[1] <= 600 - 55:
            if self.can_move[DOWN]:
                self.__position = (self.__position[0], self.__position[1] + STEP_SIZE)

            if self.get_collisions():
                self.can_move[DOWN] = False

            self.can_move[UP] = True
            self.can_move[LEFT] = True
            self.can_move[RIGHT] = True

        if self.__direction == RIGHT and self.__position[0] <= 500:
            if self.can_move[RIGHT]:
                self.__position = (self.__position[0] +STEP_SIZE, self.__position[1])
            if self.get_collisions():
                self.can_move[RIGHT] = False

            self.can_move[LEFT] = True
            self.can_move[UP] = True
            self.can_move[DOWN] = True

        if self.__direction == LEFT and self.__position[0] >= 0:
            if self.can_move[LEFT]:
                self.__position = (self.__position[0] - STEP_SIZE, self.__position[1])

            if self.get_collisions():
                self.can_move[LEFT] = False

            self.can_move[RIGHT] = True
            self.can_move[UP] = True
            self.can_move[DOWN] = True

        self.rect.topleft = self.__position

        num = random.randint(1,20)
        if num == 2:
            self.__direction = UP

        elif num == 3:
            self.__direction = DOWN

        elif num == 4:
            self.__direction = RIGHT

        elif num == 5:
            self.__direction = LEFT



    def get_collisions(self):
        obstacles = self.__game.get_obstacles()
        collision = False
        for obst in obstacles:
            if (pygame.sprite.collide_rect(obst,self)):
                collision = True

        return collision

