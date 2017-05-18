#!/usr/local/bin/python3.5
import pygame
import pygame.locals 

from RPG.character import Character
from RPG.path import street
from RPG.dialog import DialogBox
from os import path

class RPG_minigame:
    def __init__(self, game):
        self.game = game
        self.screen = game.get_screen()
        self.screen_width = game.SCREEN_WIDTH
        self.screen_height = game.SCREEN_HEIGHT
        self.momo = Character(street(self.screen_width, self.screen_height)
            , path.abspath("./RPG/momo.png"), 
            screen_width = self.screen_width,
            screen_height = self.screen_height,
            height_ratio = 0.6
            )
        # self.momo = Character(street(self.screen_width, self.screen_height)
        #     , path.abspath("./RPG/momo.png"), 
        #     screen_width = self.screen_width,
        #     screen_height = self.screen_height,
        #     height_ratio = 0.4
        #     )
        self.dialog = DialogBox("Test Dialog")

    def get_music(self):
        return None

    def get_loop(self):
        def loop():
            pressed_keys =  pygame.key.get_pressed()


            if pressed_keys[pygame.K_RIGHT]: self.momo.step_right()
            if pressed_keys[pygame.K_LEFT]: self.momo.step_left()
            if pressed_keys[pygame.K_UP]: 
                self.dialog.move_up()
                pygame.time.delay(100)
            if pressed_keys[pygame.K_DOWN]:
                self.dialog.move_down()
                pygame.time.delay(100)
            if pressed_keys[pygame.K_RETURN]:
                selected_answer = self.dialog.end_dialog()
         
            self.screen.fill((0,0,0))
            self.momo.draw_on_screen(self.screen)
            self.dialog.draw_on_screen(self.screen)
            pygame.display.flip()

            return True
        return loop

