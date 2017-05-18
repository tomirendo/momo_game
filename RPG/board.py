from json import loads 
from RPG.character import Character, StaticCharacter
from os import path

class Board:
    def __init__(self, game, filename, room):
        with open(filename) as f:
            data = loads(f.read())

        self.room = room
        self.game = game
        self.screen = game.get_screen()
        self.screen_width = game.SCREEN_WIDTH
        self.screen_height = game.SCREEN_HEIGHT
        self.in_dialog = False
        

        self.momo = Character(room(self.screen_width, self.screen_height)
            , path.abspath("./RPG/momo.png"), 
            screen_width = self.screen_width,
            screen_height = self.screen_height,
            height_ratio = 0.6)

        self.static_characters = []
        for static_character in data['additional_characters']:
            self.static_characters.append(StaticCharacter(image = static_character['image'],
                            screen_width = self.screen_width,
                            screen_height = self.screen_height,
                            height_ratio = static_character['height_ratio'],
                            position =  static_character['position'],
                            ))

    def draw(self):
        for character in self.static_characters:
            character.draw_on_screen(self.screen)
        self.momo.draw_on_screen(self.screen)
    def step_right(self):
        self.momo.step_right()
    def step_left(self):
        self.momo.step_left()
    def move_down(self):
        pass
    def move_up(self):
        pass
    def press_enter(self):
        if self.static_character[0].is_dialog_done():
            

            

        #self.dialog = DialogBox("Test Dialog")