
import pygame
from pygame.locals import *
from Runner import Runner
from Chaser import Chaser
from Obstacle import Obstacle
from Stuff import Stuff


class ChaseGame:

    MAX_SCORE = 30

    def __innit__(self, game):
        self.game = game
        self.screen = game.get_screen()
        self.screen_width = game.SCREEN_WIDTH
        self.screen_height = game.SCREEN_HEIGHT
        self.background = pygame.image.load('llama.jpg')
        self.background_up_left_coors = 0
        self.background_speed = 10
        self.continue_game = True

        self.scores = self.runner.get_scores()
        self.runner = Runner()
        self.chaser = Chaser()


    def handle_event(self, event):
        if pygame.KEYDOWN:
            if event == pygame.QUIT:
                self.continue_game = False
            elif event.type == pygame.K_SPACE:
                self.runner.jump()
            elif event.type == pygame.K_UP:
                self.runner.flip()
        else:
            self.runner.land()

        return

    def manage_background(self):
        return

    def manage_obstacles(self):
        return

    def run_round(self):
        if self.runner.get_scores() <= self.MAX_SCORE:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.runner.get_image(), self.runner.get_position)
            for event in self.game.get_keys_pressed():
                self.handle_event(event)
            self.manage_obstacles()
            self.manage_background()
            pygame.display.update()
        else:
            self.continue_game = False

        return self.continue_game

    def get_loop(self):
        return self.run_round()