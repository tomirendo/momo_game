from json import loads 
from RPG.character import Character, StaticCharacter
from os import path
from json import loads
import pygame 
from pygame.transform import scale
from math import sqrt

def distance(p1, p2):
    return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

class Board:
    def __init__(self, game, owner, filename, room):
        with open(filename) as f:
            data = loads(f.read())

        self.room = room
        self.game = game
        self.owner = owner
        self.screen = game.get_screen()
        self.screen_width = game.SCREEN_WIDTH
        self.screen_height = game.SCREEN_HEIGHT
        self.current_dialog = None
        self.in_dialog = False
        self.background_image = scale(pygame.image.load(data['background']), (self.screen_width, self.screen_height))

        self.momo = Character(room(self.screen_width, self.screen_height)
            , path.abspath(data['momo']['image']), 
            screen_width = self.screen_width,
            screen_height = self.screen_height,
            height_ratio = data['momo']['height_ratio'])

        self.static_characters = []
        for static_character in data['additional_characters']:
            self.static_characters.append(StaticCharacter(image = static_character['image'],
                            screen_width = self.screen_width,
                            screen_height = self.screen_height,
                            height_ratio = static_character['height_ratio'],
                            position =  static_character['position'],
                            dialog_file = static_character['dialog_file']
                            ))

    def draw(self):
        self.screen.blit(self.background_image, (0,0))
        for character in self.static_characters:
            character.draw_on_screen(self.screen)
        self.momo.draw_on_screen(self.screen)
        if self.in_dialog:
            self.current_dialog.draw_on_screen(self.screen)
        

    def step_right(self):
        self.momo.step_right()

    def step_left(self):
        self.momo.step_left()

    def move_down(self):
        if self.current_dialog:
            self.current_dialog.move_down()

    def move_up(self):
        if self.current_dialog:
            self.current_dialog.move_up()

    def find_selected_character(self):
        momo_middle = self.momo.middle()
        for character in self.static_characters:
            if distance(character.middle(), momo_middle) < (character.radius() + self.momo.radius()):
                return character

    def press_enter(self):
        selected_character = self.find_selected_character()

        if selected_character is None:
            return 

        if selected_character.has_dialog():
            if not selected_character.is_dialog_done() and not self.in_dialog:
                selected_character.begin_dialog()
                self.in_dialog = True
                self.current_dialog = selected_character.dialog
            else :
                self.current_dialog.press_enter()
                self.in_dialog = not selected_character.is_dialog_done()



            

        #self.dialog = DialogBox("Test Dialog")