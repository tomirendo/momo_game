
import os
import pygame
import random
from Runner import Runner
from Chaser import Chaser
from Obstacle import Obstacle
from Stuff import Stuff


class ChaseGame:

    MAX_SCORE = 30
    BACKGROUND_SPEED = 10
    END_GAME_MESSAGE = "Oh my, seems like the Men in Grey got you. \n You must try again Momo, you must save our town!"
    OBSTACLE_FREQUENCY = 200
    RESET_DURATION = 300

    TRASH_CAN = pygame.image.load(os.path.abspath('trash_can.png'))
    TRASH_BAG = pygame.image.load(os.path.abspath('trash_bag.png'))
    OLD_MAN_1 = pygame.image.load(os.path.abspath('old_man.png'))
    OLD_MAN_2 = pygame.image.load(os.path.abspath('man.png'))
    OLD_WOMAN = pygame.image.load(os.path.abspath('old_woman.png'))

    def __init__(self, game):
        self.game = game
        self.screen = game.get_screen()
        self.screen_width = game.SCREEN_WIDTH
        self.screen_height = game.SCREEN_HEIGHT
        self.background_1 = pygame.image.load('city_final.jpg')
        self.background_2 = pygame.image.load('city_final.jpg')
        self.background_1_x_pos = 0
        self.background_2_x_pos = self.screen_width
        self.music = pygame.mixer.music.load(os.path.abspath('The Sound of Silence.mp3'))
        self.continue_game = True
        self.font = pygame.font.SysFont('monospace', 20, (0, 0, 0))
        self.runner = Runner()
        self.scores = self.runner.get_scores()
        self.chaser = Chaser()
        self.obstacle = Obstacle(self.TRASH_CAN, self.runner.GROUND_LEVEL, self.runner.FIXED_X_POSITION,
                self.screen_width, self.BACKGROUND_SPEED)
        self.__obstacle_cooldown_count = 0
        self.__reset_countdown = 0

    def manage_events(self):
        keys_pressed = self.game.get_keys_pressed()
        if keys_pressed[pygame.QUIT]:
            self.continue_game = False
        elif keys_pressed[pygame.K_SPACE]:
            self.runner.jump()
        # elif keys_pressed[pygame.K_UP]:
        #     self.runner.flip()
        else:
            self.runner.slide()

    def manage_background(self):
        if self.background_2_x_pos >= 0:
            self.background_1_x_pos -= self.BACKGROUND_SPEED
            self.background_2_x_pos -= self.BACKGROUND_SPEED
        else:
            self.background_1_x_pos = 0
            self.background_2_x_pos = self.screen_width

    def manage_obstacles(self):
        if self.obstacle is None:
            self.create_obstacle()
        elif (self.obstacle.get_x_position() <= 0) and (self.__obstacle_cooldown_count == 0):
            self.create_obstacle()
        else:
            self.obstacle.move()
            self.obstacle.update_cooldown_count()

    def create_obstacle(self):
        random_obstacle_choice = random.randint(0, 5)
        if random_obstacle_choice == 0:
            self.obstacle = Obstacle(self.TRASH_CAN, self.runner.GROUND_LEVEL, self.runner.FIXED_X_POSITION,
                                    self.screen_width, self.BACKGROUND_SPEED)
        elif random_obstacle_choice == 1:
            self.obstacle = Obstacle(self.TRASH_BAG, self.runner.GROUND_LEVEL, self.runner.FIXED_X_POSITION,
                                     self.screen_width, self.BACKGROUND_SPEED)
        elif random_obstacle_choice == 2:
            self.obstacle = Obstacle(self.OLD_MAN_2, self.runner.GROUND_LEVEL, self.runner.FIXED_X_POSITION,
                                     self.screen_width, self.BACKGROUND_SPEED)
        elif random_obstacle_choice == 3:
            self.obstacle = Obstacle(self.OLD_WOMAN, self.runner.GROUND_LEVEL, self.runner.FIXED_X_POSITION,
                                     self.screen_width, self.BACKGROUND_SPEED)
        else:
            self.obstacle = Obstacle(self.OLD_MAN_1, self.runner.GROUND_LEVEL, self.runner.FIXED_X_POSITION,
                                     self.screen_width, self.BACKGROUND_SPEED)
        self.__obstacle_cooldown_count = self.OBSTACLE_FREQUENCY

    def check_collisions(self):
        # for point_x in range(self.obstacle.get_x_position(), self.obstacle.get_x_position() +
        #         self.obstacle.image.get_width() + 1):
        #     for point_y in range(self.obstacle.get_y_position(), self.obstacle.get_y_position() +
        #             self.obstacle.image.get_height() + 1):
        #         if self.runner.rect.collidepoint(point_x, point_y):
        #             return True
        # return False
        pygame.sprite.collide_rect(self.runner, self.obstacle)

    def reset_game(self):
        self.print_end_message()
        self.__reset_countdown = self.RESET_DURATION
        self.background_1_x_pos = 0
        self.background_2_x_pos = self.screen_width
        self.runner.reset_state()
        self.obstacle = None

    def print_end_message(self):
        if self.__reset_countdown > 0:
            text_surface_obj = self.font.render(self.END_GAME_MESSAGE, True, (0, 0, 0))
            text_rect_obj = text_surface_obj.get_rect()
            text_rect_obj.center = (200, 150)
            self.screen.blit(text_surface_obj, text_rect_obj)
            self.__reset_countdown -= 1

    def run_round(self):
        if self.runner.get_scores() <= self.MAX_SCORE:
            if not self.__reset_countdown != 0:
                self.manage_background()
                self.screen.blit(self.background_1, (self.background_1_x_pos, 0))
                self.screen.blit(self.background_2, (self.background_2_x_pos, 0))
                self.screen.blit(self.runner.get_image(), self.runner.get_position())
                self.manage_events()
                self.manage_obstacles()
                self.screen.blit(self.obstacle.get_image(), self.obstacle.get_position())
                print(self.check_collisions())
                if self.check_collisions():
                    self.reset_game()
            else:
                self.print_end_message()
            pygame.display.update()

        else:
            self.continue_game = False
        return self.continue_game

    def get_loop(self):
        return self.run_round

    def get_music(self):
        return self.music
