import pygame 
from pygame.transform import scale
from RPG.dialog import Dialog
from json import loads

class Character:
    def __init__(self, room, image, 
        screen_width, screen_height, 
        height_ratio, # Character Height / Screen Height
            initial_locaiton = 0):
        self.location = initial_locaiton
        self.room = room
        self.init_image(image, screen_width, screen_height, height_ratio)

    def init_image(self, image, screen_width, screen_height, height_ratio):
        image = pygame.image.load(image)
        width, height = image.get_size()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.height = self.screen_height * height_ratio 
        self.width = width/height *self.height
        self.image = scale(image, [int(self.width), int(self.height)])


    def step_right(self):
        if self.location < 1:
            self.location += 0.03
            
    def step_left(self):
        if self.location > 0 :
            self.location -= 0.03

    def get_position(self):
        x,y = self.room.get_position(self.location)
        y -= self.height
        x = (self.screen_width - self.width )/self.screen_width * x
        return (x,y)

    def draw_on_screen(self, screen):
        screen.blit(self.image, self.get_position())

    def middle(self):
        position = self.get_position()
        return (position[0]+self.width/2, 
                position[1]+self.height/2)

    def radius(self):
        return min([self.width, self.height])/3

class StaticCharacter:
    def __init__(self, image, 
        screen_width, screen_height, 
        height_ratio, # Character Height / Screen Height
            position, dialog_file = None):
        self.position = position
        self.x = position[0]*screen_width
        self.y = position[1]*screen_height
        self.init_image(image, screen_width, screen_height, height_ratio)
        if dialog_file:
            with open(dialog_file) as f:
                self.dialog = Dialog(loads(f.read()))
        else :
            self.dialog = None
        self.run_dialog = False

    def begin_dialog(self):
        if self.dialog:
            self.run_dialog = True

    def init_image(self, image, screen_width, screen_height, height_ratio):
        image = pygame.image.load(image)
        width, height = image.get_size()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.height = self.screen_height * height_ratio 
        self.width = width/height *self.height
        self.image = scale(image, [int(self.width), int(self.height)])

    def draw_on_screen(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def has_dialog(self):
        return bool(self.dialog)

    def is_dialog_done(self):
        return self.dialog.done

    def middle(self):
        return (self.x+self.width/2, 
                self.y+self.height/2)

    def radius(self):
        return min([self.width, self.height])/3



