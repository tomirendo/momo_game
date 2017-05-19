
import os
import pygame
import random
from naama.Runner import Runner
from naama.Obstacle import Obstacle
from naama.Flower import Flower


class ChaseGame:

    MAX_SCORE = 25
    BACKGROUND_SPEED = 10
    END_GAME_MESSAGE_1 = "Oh my, seems like the Men in Grey got you."
    END_GAME_MESSAGE_2 = "You must try again Momo, you must save our town!"
    OBSTACLE_FREQUENCY = 200
    RESET_DURATION = 200

    TRASH_CAN = pygame.image.load(os.path.abspath('naama\\trash_can.png'))
    TRASH_BAG = pygame.image.load(os.path.abspath('naama\\trash_bag.png'))
    OLD_MAN_1 = pygame.image.load(os.path.abspath('naama\\old_man.png'))
    OLD_MAN_2 = pygame.image.load(os.path.abspath('naama\\man.png'))
    OLD_WOMAN = pygame.image.load(os.path.abspath('naama\\old_woman.png'))
    GREY_GENTEMAN = pygame.image.load(os.path.abspath('naama\\dark_person.png'))
    FLOWER = pygame.image.load(os.path.abspath('naama\\flower.png'))
    END_DELAY = 100

    def __init__(self, game):
        self.game = game
        self.screen = game.get_screen()
        self.screen_width = game.SCREEN_WIDTH
        self.screen_height = game.SCREEN_HEIGHT
        self.background_1 = pygame.image.load('naama\\city_final.jpg')
        self.background_2 = pygame.image.load('naama\\city_final.jpg')
        self.background_1_x_pos = 0
        self.background_2_x_pos = self.screen_width
        self.music = pygame.mixer.music.load(os.path.abspath('naama\\The Sound of Silence.mp3'))
        self.continue_game = True
        self.font = pygame.font.SysFont('monospace', 16, (0, 0, 0))
        self.__reset_countdown = 0
        self.__end_delay = 0

        self.runner = Runner()
        self.obstacles = []
        self.flower = []

    def manage_events(self):
        keys_pressed = self.game.get_keys_pressed()
        if keys_pressed[pygame.QUIT]:
            self.continue_game = False
        elif keys_pressed[pygame.K_SPACE]:
            self.runner.jump()
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
        random_choice = random.randint(0, 700)
        if self.obstacles == [] or random_choice == 101:
            self.create_obstacle()
        else:
            for obstacle in self.obstacles:
                obstacle.move()

    def manage_flowers(self):
        rand_choice = random.randint(0, 30)
        if rand_choice == 0:
            new_flower = Flower(self.FLOWER)
            self.flower.append(new_flower)
        for flower in self.flower:
            if flower.get_x_pos() > 0:
                flower.move()
            else:
                self.flower.remove(flower)

    def create_obstacle(self):
        random_obstacle_choice = random.randint(0, 5)
        if random_obstacle_choice == 0:
            obstacle = Obstacle(self.TRASH_CAN, self.runner.GROUND_LEVEL, self.runner.FIXED_X_POSITION,
                                    self.screen_width, self.BACKGROUND_SPEED)
        elif random_obstacle_choice == 1:
            obstacle = Obstacle(self.TRASH_BAG, self.runner.GROUND_LEVEL, self.runner.FIXED_X_POSITION,
                                     self.screen_width, self.BACKGROUND_SPEED)
        elif random_obstacle_choice == 2:
            obstacle = Obstacle(self.OLD_MAN_2, self.runner.GROUND_LEVEL, self.runner.FIXED_X_POSITION,
                                     self.screen_width, self.BACKGROUND_SPEED)
        elif random_obstacle_choice == 3:
            obstacle = Obstacle(self.OLD_WOMAN, self.runner.GROUND_LEVEL, self.runner.FIXED_X_POSITION,
                                     self.screen_width, self.BACKGROUND_SPEED)
        else:
            obstacle = Obstacle(self.OLD_MAN_1, self.runner.GROUND_LEVEL, self.runner.FIXED_X_POSITION,
                                     self.screen_width, self.BACKGROUND_SPEED)
        self.obstacles.append(obstacle)
        self.__obstacle_cooldown_count = self.OBSTACLE_FREQUENCY

    def check_collisions(self):
        for obstacle in self.obstacles:
            runner_position = self.runner.get_position()
            runner_top_right_corner = (runner_position[0] + 80, runner_position[1])
            runner_bottom_right = (runner_position[0] + 80, runner_position[1] + 115)
            runner_bottom_left = (runner_position[0] , runner_position[1] + 115)
            corners = [runner_position,runner_bottom_left,runner_bottom_right,runner_top_right_corner]

            obst_position = obstacle.get_position()
            collision = False
            for corner in corners:
                if corner[0] >= obst_position[0] and corner[0] <= obst_position[0] + 30:
                    if corner[1] >= obst_position[1] and corner[1] <= obst_position[1] + 50:
                        collision = True
            if collision:
                self.reset_game()

    def check_flower_collisions(self):
        for flower in self.flower:
            flower_position = flower.get_position()
            flower_top_right_corner = (flower_position[0] + 50, flower_position[1])
            flower_bottom_right = (flower_position[0] + 50, flower_position[1] + 50)
            flower_bottom_left = (flower_position[0] , flower_position[1] + 50)
            corners = [flower_position, flower_top_right_corner,flower_bottom_right,flower_bottom_left]

            obst_position = self.runner.get_position()
            collision = False
            for corner in corners:
                if corner[0] >= obst_position[0] and corner[0] <= obst_position[0] + 80:
                    if corner[1] >= obst_position[1] and corner[1] <= obst_position[1] + 80:
                        collision = True
            if collision:
                self.flower.remove(flower)
                self.runner.update_scores()

    def reset_game(self):
        self.print_end_message()
        self.__reset_countdown = self.RESET_DURATION
        self.background_1_x_pos = 0
        self.background_2_x_pos = self.screen_width
        self.runner.reset_state()
        self.obstacles = []

    def print_end_message(self):
        if self.__reset_countdown > 0:
            text_surface_obj = self.font.render(self.END_GAME_MESSAGE_1, True, (0, 0, 0))
            self.screen.blit(text_surface_obj, (150, 60))
            self.__reset_countdown -= 1

            text_surface_obj = self.font.render(self.END_GAME_MESSAGE_2, True, (0, 0, 0))
            self.screen.blit(text_surface_obj, (200, 90))
            self.__reset_countdown -= 1

    def run_round(self):
        if self.runner.get_scores() <= self.MAX_SCORE:
            if not self.__reset_countdown != 0:
                self.manage_background()
                self.screen.blit(self.background_1, (self.background_1_x_pos, 0))
                self.screen.blit(self.background_2, (self.background_2_x_pos, 0))
                self.screen.blit(self.GREY_GENTEMAN, (5, 120))
                self.screen.blit(self.runner.get_image(), self.runner.get_position())
                self.manage_events()
                self.manage_obstacles()
                self.check_flower_collisions()
                self.manage_flowers()
                for flower in self.flower:
                    self.screen.blit(flower.get_image(), flower.get_position())
                scores_text = self.font.render("scores: " + str(self.runner.get_scores()), True, (0, 0, 0))
                self.screen.blit(scores_text, (680, 570))
                for obstacle in self.obstacles:
                    self.screen.blit(obstacle.get_image(), obstacle.get_position())
                self.check_collisions()
            else:
                self.print_end_message()
            pygame.display.update()

        else:
            if self.__end_delay < self.END_DELAY:
                self.screen.blit(self.background_1, (self.background_1_x_pos, 0))
                self.screen.blit(self.background_2, (self.background_2_x_pos, 0))
                self.screen.blit(self.runner.get_image(), self.runner.get_position())
                self.screen.blit(self.GREY_GENTEMAN, (5, 120))
                scores_text = self.font.render("You did it! You may actually save us all!", True, (0, 0, 0))
                self.screen.blit(scores_text, (100, 300))
            else:
                self.continue_game = False
        return self.continue_game

    def get_loop(self):
        return self.run_round

    def get_music(self):
        return self.music
