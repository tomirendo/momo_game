#!/usr/local/bin/python3.5
import pygame
from sys import argv

if argv[-1] == "yotam":
    from RPG.rpg import RPG_minigame as minigame
elif argv[-1] == "neta":
    from Neta.greenGrocerGame import GreenGrocerGame
    minigame = GreenGrocerGame
else:
    from Naama.ChaseGame import ChaseGame
    minigame = ChaseGame

class Game():

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480

    ''' the main class for the Momo game'''

    def __init__(self,screen):
        '''create a new game object'''
        self.__screen = screen
        self.__minigame_list = list()
        self.__minigame_list.append(minigame(self))
        self.__current_minigame_loop = self.__minigame_list[0].get_loop()
        self.__current_minigame_number = 0
        self.__music = self.__minigame_list[self.__current_minigame_number].get_music()




    def get_keys_pressed(self):
        '''Get the list of buttons that were pressed'''
        return pygame.key.get_pressed()


    def advance_game(self):
        '''Advance to the next minigame'''
        self.__current_minigame_number += 1
        self.__current_minigame_loop = self.__minigame_list[self.__current_minigame_number].get_loop()
        self.__music = self.__minigame_list[self.__current_minigame_number].get_music()



    def get_loop(self):
        '''return the current game loop'''
        return self.__current_minigame_loop


    def get_screen(self):
        '''return the screen object'''
        return self.__screen

    def get_music(self):
        '''return the current music to play'''
        return self.__music


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    done = False
    screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
    game = Game(screen)
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        if not game.get_loop()():
            game.advance_game()
            filename = game.get_music()
            if (filename):
                bg_music = pygame.mixer.Sound(filename)
                bg_music.play()
        pygame.display.flip()
        clock.tick(60)
