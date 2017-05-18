import pygame
from os.path import abspath,join
font_path = abspath(join(".","RPG","Assistant.ttf"))
font_path = abspath(join(".","RPG","Zapfino.ttf"))

class Dialog:
    def __init__(self, text):
        self.text = text
        self.timer = 0
        self.myfont = pygame.font.Font(font_path, 10)

    def draw_on_screen(self,screen):
        screen_width, screen_height = screen.get_size()
        self.timer += 1
        self.draw_background(screen)
        label = self.myfont.render(self.text, 1, (255,255,255))
        screen.blit(label, (5, .85*screen_height))

    def draw_background(self, screen):
        screen_width, screen_height = screen.get_size()
        text_background = pygame.Surface((screen_width,screen_height * .2))  # the size of your rect
        text_background.set_alpha(40)                # alpha level
        text_background.fill((255,255,255))           # this fills the entire surface
        screen.blit(text_background, (0,.8*screen_height)) 