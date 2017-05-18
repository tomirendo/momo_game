import pygame 

class Character:
    def __init__(self, location , room, image, screen_width, screen_height):
        self.location = 0
        self.room = room
        self.image = pygame.image.load(image)
        self.width, self.height = self.image.get_size()
        self.screen_width = screen_width
        self.screen_height = screen_height

    def step_right(self):
        if self.location < 1:
            self.location += 0.01
            
    def step_left(self):
        if self.location > 0 :
            self.location -= 0.01

    def get_position(self):
        x,y = self.room.get_position(self.location)
        y -= self.height
        x = (self.screen_width - self.width )/self.screen_width * x
        return (x,y)

    def draw_on_screen(self, screen):
        screen.blit(self.image, self.get_position())


from path import street
momo = Character(0, street, "./momo.png", 1024,768)