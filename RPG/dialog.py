import pygame
from os.path import abspath,join
font_path = abspath(join(".","RPG","Zapfino.ttf"))
font_path = abspath(join(".","RPG","Assistant.ttf"))
font_path = abspath(join(".","RPG","Times.ttf"))
NON_SELECTED_ANSWER_COLOR = (0,0,0)
SELECTED_ANSWER_COLOR = (100, 30, 170)
FONT_SIZE = 15
SPACTING_OF_ANSWERS = FONT_SIZE*2
SPACING_FROM_BOURDER = 20
FIRST_ANSWER_LOCATION = 0.83
DIALOG_BOX_SIZE = 0.2

class Dialog:
    def __init__(self, dialog_dictionary):
        self.dict = dialog_dictionary
        self.init_dialog()
        self.done = False

    def init_dialog(self):
        text = self.dict['text']
        answers = [i['answer_text'] for i in self.dict['answers']]
        self.dialog_box = DialogBox(text, answers)

    def draw_on_screen(self, screen):
        if not self.done:
            self.dialog_box.draw_on_screen(screen)

    def move_up(self):
        self.dialog_box.move_up()

    def move_down(self):
        self.dialog_box.move_down()

    def press_enter(self):
        selected_answer = self.dialog_box.end_dialog()
        if self.dict['answers'][selected_answer].get('next_dialog') is not None:
            self.dict = self.dict['answers'][selected_answer]['next_dialog']
            self.init_dialog()
        else :
            self.done = True

    def get_done(self):
        '''return True if the dialogue is done, False otherwise'''
        return self.done

class DialogBox:
    def __init__(self, text, answers = ["Press any ENTER to continue..."]):
        self.text = text
        self.timer = 0
        self.myfont = pygame.font.Font(font_path, FONT_SIZE)
        self.last_render = None
        self.selected_answer = 0
        self.answers = answers
        self.render_answers()
        self.number_of_answers = len(answers)
        self.done = False

    def render_answers(self):
        self.rendered_answers = []
        for index, ans in enumerate(self.answers):
            if index == self.selected_answer:
                color = SELECTED_ANSWER_COLOR
            else :
                color = NON_SELECTED_ANSWER_COLOR
            self.rendered_answers.append(self.myfont.render(ans, 1, color))

    def draw_answers(self, screen):
        screen_width, screen_height = screen.get_size()
        for index, answer in enumerate(self.rendered_answers):
            screen.blit(answer, (SPACING_FROM_BOURDER, 
                        FIRST_ANSWER_LOCATION*screen_height + (index+1)*SPACTING_OF_ANSWERS))

    def is_timer_done(self):
        return self.timer > len(self.text)

    def draw_on_screen(self,screen):
        self.timer += 1
        if self.done == False:
            self.draw_background(screen)
            self.draw_text(screen)
            if self.is_timer_done():
                self.draw_answers(screen)

    def draw_text(self, screen):
        screen_width, screen_height = screen.get_size()
        if self.last_render and self.is_timer_done():
            label = self.last_render
        else :
            label = self.myfont.render(self.text[:self.timer], 
            1, (0,0,0))
            self.last_render = label
        screen.blit(label, (SPACING_FROM_BOURDER, 
                FIRST_ANSWER_LOCATION*screen_height))

    def draw_background(self, screen):
        screen_width, screen_height = screen.get_size()
        text_background = pygame.Surface((screen_width,screen_height * DIALOG_BOX_SIZE ))  # the size of your rect
        text_background.set_alpha(200)                # alpha level
        text_background.fill((255,255,255))           # this fills the entire surface
        screen.blit(text_background, (0,(1-DIALOG_BOX_SIZE)*screen_height)) 

    def move_up(self):
        self.selected_answer = (self.selected_answer+1)%self.number_of_answers
        self.render_answers()

    def move_down(self): 
        self.selected_answer = (self.selected_answer-1)%self.number_of_answers
        self.render_answers()

    def end_dialog(self):
        """
            Ends the dialog and returns the selected answer
        """
        self.done = True
        return self.selected_answer










