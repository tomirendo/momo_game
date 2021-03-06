#!/usr/local/bin/python3.5
import pygame
from sys import argv

try: #Import modules to play video game files
    import imageio

    imageio.plugins.ffmpeg.download()
    from moviepy.editor import VideoFileClip
except:
    pass

try:
    from Neta.greenGrocerGame import GreenGrocerGame
except :
    pass

from RPG.rpg import RPG_minigame as minigame
from AVi.coloredBoxes import *
from naama.ChaseGame import ChaseGame

if argv[-1] == "yotam":
    from RPG.rpg import RPG_minigame as minigame
elif argv[-1] == "neta":
    minigame = GreenGrocerGame
elif argv[-1] == "avi":
    from AVi.coloredBoxes import *
    from AVi.coloredBoxes import *
    minigame = coloredGame
else:
    from naama.ChaseGame import *
    minigame = ChaseGame

class Game():

    ''' the main class for the Momo game'''
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600


    def __init__(self,screen):
        '''create a new game object'''
        self.__screen = screen
        self.__minigame_list = list()
        try :
            self.__minigame_list.append(GreenGrocerGame(self))
        except :
            pass
        self.__minigame_list.append(minigame(self))
        self.__minigame_list.append(ChaseGame(self))
        self.__minigame_list.append(coloredGame(self))
        self.__current_minigame_loop = self.__minigame_list[0].get_loop()
        self.__current_minigame_number = 0
        self.__music = self.__minigame_list[self.__current_minigame_number].get_music()


    def get_mouse_click(self):
        '''return a tuple containing two elements:
        1. a series of three boolean values : MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
        2. the position of the mouse'''
        return (pygame.mouse.get_pressed(), pygame.mouse.get_pos())

    def get_keys_pressed(self):
        '''Get the list of buttons that were pressed'''
        return pygame.key.get_pressed()


    def advance_game(self):
        '''Advance to the next minigame'''
        self.__current_minigame_number += 1
        self.__current_minigame_loop = self.__minigame_list[self.__current_minigame_number].get_loop()
        print(self.__minigame_list[self.__current_minigame_number])
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
    pygame.font.init()
    clock = pygame.time.Clock()
    done = False
    screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT))
    game = Game(screen)
    try:  # Attempt to play intro video
        clip = VideoFileClip('momo-intro.mp4')
        clip.preview()
    except:
        pass

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
