#!/usr/local/bin/python3.5
import pygame
import pygame.locals 

from RPG.character import Character
from RPG.path import street
from RPG.dialog import Dialog
from RPG.board import Board
from os import path
from json import loads

with open("./RPG/example_dialog.json") as f:
    dialog_dictionary = loads(f.read())
    print(dialog_dictionary)

class RPG_minigame:
    def __init__(self, game):
        self.game = game
        self.board = Board(game, "./RPG/street.json", street)
        self.screen = game.get_screen()
        self.screen_width = game.SCREEN_WIDTH
        self.screen_height = game.SCREEN_HEIGHT

    def get_music(self):
        return None

    def get_loop(self):
        def loop():
            pressed_keys =  pygame.key.get_pressed()


            if pressed_keys[pygame.K_RIGHT]: self.board.step_right()
            if pressed_keys[pygame.K_LEFT]: self.board.step_left()
            if pressed_keys[pygame.K_UP]: 
                self.board.move_up()
                pygame.time.delay(100)
            if pressed_keys[pygame.K_DOWN]:
                self.board.move_down()
                pygame.time.delay(100)
            if pressed_keys[pygame.K_RETURN]:
                selected_answer = self.board.press_enter()
                pygame.time.delay(100)
         
            self.screen.fill((0,0,0))
            self.board.draw()
            pygame.display.flip()

            return True
        return loop

