import pygame
from crazyPacManBlitz.Momo import Momo
import os
from crazyPacManBlitz.Obstacles import Obstacle
from crazyPacManBlitz.Ghost import Ghost

car_img = 'crazyPacManBlitz/car.jpg'
car_img_path = os.path.abspath(car_img)
CAR_IMAGE = pygame.image.load(car_img_path)


OBSTACLE_SIZE = 55


UP = 'up'
LEFT = 'left'
DOWN = 'down'
RIGHT = 'right'

STEP_SIZE = 4
class PacMan():
    '''the pac man in frozen time minigame'''

    def __init__(self,game):
        '''create a new pac man minigame instance'''
        self.__game = game
        self.__screen = self.__game.get_screen()
        self.__momo = Momo((self.__game.SCREEN_WIDTH // 2, self.__game.SCREEN_HEIGHT // 2))

        self.__obstacle_list = list()
        self.put_obstacles_on_path((55*5,55*8),0,True)
        self.put_obstacles_on_path((55*1, 55*5),55*2,True)
        self.put_obstacles_on_path((55*7, 55*10), 55 *2, True)
        self.put_obstacles_on_path((55*0, 55* 6), 55 *4, True)
        self.put_obstacles_on_path((55*2, 55* 8), 55 *6, True)
        self.put_obstacles_on_path((55* 4, 55* 10), 55 *8, True)
        self.put_obstacles_on_path((55*2, 55*7), 55 *10, True)
        self.put_obstacles_on_path((55*6, 55 *9), 55 *12, True)
        self.put_obstacles_on_path((55*0, 55 * 5), 55 * 13, True)
        self.put_obstacles_on_path((55*4, 55 * 7), 55 * 0, False)
        self.put_obstacles_on_path((55*9, 55 *11), 55 * 0, False)
        self.put_obstacles_on_path((55*1, 55 * 2), 55 *1, False)
        self.put_obstacles_on_path((55*6,55*12),55*2, False)
        self.put_obstacles_on_path((55*0, 55 * 3), 55 * 2, False)
        self.put_obstacles_on_path((55 * 0, 55 * 7),55 *7, False)
        self.put_obstacles_on_path((55 * 10, 55 * 13), 55 *8, False)
        self.put_obstacles_on_path((55 * 4, 55 * 9), 55 * 9, False)





        self.can_move = {RIGHT : True, LEFT: True, UP: True, DOWN: True}


        self.__ghost_list = list()
        self.__ghost_list.append(Ghost((self.__game.SCREEN_WIDTH // 5, self.__game.SCREEN_HEIGHT // 5),self))





    def main_loop(self):
        '''the minigame's main loop'''
        self.__screen.fill((0,0,0))
        self.__screen.blit(self.__momo.get_image(), self.__momo.get_position())
        self.move()
        for obstacle in self.__obstacle_list:
            self.__screen.blit(obstacle.get_image(),obstacle.get_position())

        for ghost in self.__ghost_list:
            self.__screen.blit(ghost.get_image(),ghost.get_position())
            ghost.move()
        return True



    def get_loop(self):
        '''get the minigame's main loop'''
        return self.main_loop


    def get_music(self):
        '''get the music for the mini-game'''
        return None


    def move(self):
        '''move Momo on the screen'''

        keys_pressed = self.__game.get_keys_pressed()
        if keys_pressed[pygame.K_UP] and self.__momo.get_position()[1] > 0:
            if self.can_move[UP]:
                self.__momo.set_position((self.__momo.get_position()[0], self.__momo.get_position()[1] - STEP_SIZE))
                if self.get_colision():
                    self.can_move[UP] = False

                self.can_move[DOWN] = True
                self.can_move[LEFT] = True
                self.can_move[RIGHT] = True

        elif keys_pressed[pygame.K_LEFT] and self.__momo.get_position()[0] > 0:
            if self.can_move[LEFT]:
                self.__momo.set_position((self.__momo.get_position()[0]  - STEP_SIZE, self.__momo.get_position()[1]))
                if self.get_colision():
                    self.can_move[LEFT] = False

                self.can_move[UP] = True
                self.can_move[DOWN] = True
                self.can_move[RIGHT] = True

        elif keys_pressed[pygame.K_RIGHT] and self.__momo.get_position()[0] < 800 - 55:
            if self.can_move[RIGHT]:
                self.__momo.set_position((self.__momo.get_position()[0]  + STEP_SIZE, self.__momo.get_position()[1]))
                if self.get_colision():
                    self.can_move[RIGHT] = False
                self.can_move[UP] = True
                self.can_move[LEFT] = True
                self.can_move[DOWN] = True

        elif keys_pressed[pygame.K_DOWN]:
            if self.can_move[DOWN] and self.__momo.get_position()[1] <= 500:
                self.__momo.set_position((self.__momo.get_position()[0], self.__momo.get_position()[1]  + STEP_SIZE))
                if self.get_colision():
                    self.can_move[DOWN] = False
                self.can_move[UP] = True
                self.can_move[LEFT] = True
                self.can_move[RIGHT] = True


    def get_colision(self):
        '''True if there is a collision with an obstacle'''
        collision = False
        for obstacle in self.__obstacle_list:
            if pygame.sprite.collide_rect(obstacle,self.__momo):
                collision = True

        return collision


    def get_obstacles(self):
        return self.__obstacle_list



    def put_obstacles_on_path(self,target_path,coord,bottom_up):
        if bottom_up:
            x = coord
            y = target_path[0]

            while (y + OBSTACLE_SIZE <= target_path[1]):
                self.__obstacle_list.append(Obstacle(CAR_IMAGE,(x,y)))
                y += OBSTACLE_SIZE

        else:
            print('g')
            y = coord
            x = target_path[0]

            while (x + OBSTACLE_SIZE <= target_path[1]):
                self.__obstacle_list.append(Obstacle(CAR_IMAGE,(x,y)))
                x += OBSTACLE_SIZE
