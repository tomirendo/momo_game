import pygame
import os
import time
from momo_game.Neta.Shopper import Shopper
from momo_game.RPG.dialog import Dialog, DIALOG_BOX_SIZE
from momo_game.Neta.power_ups import PowerUps

POSITION = 'positiom'
IMAGE = 'image'
WIDTH = 'width'
HEIGHT = 'height'
SHOPPER = 'shopper'
GROCER = 'grocer'

TALKING = 'talking'
TEXT = 'text'

#vegetable constants:
CARROTS = 'carrots'
CARROT_POSITION = (14+150,114+150)
TOMATOES = 'tomatoes'
TOMATO_POSITION = (115+150,210+150)
CUCUMBERS = 'cucumbers'
CUCUMBER_POSITION = (211+150,331+150)
TOMATO_PRICE = 0.9
CARROT_PRICE = 1.1
CUCUMBER_PRICE = 0.5

speech_bubble_path = os.path.abspath('Neta/speechBubble.png')
SPEECH_BUBBLE_IMAGE = pygame.image.load(speech_bubble_path)


class GreenGrocerGame():
    '''The green Grocer minigame for the Momo game'''

    STEPSIZE = 3
    GROCER_IMAGE_WIDTH = 130
    GROCER_IMAGE_HEIGHT = 300


    def __init__(self,game):
        '''Initiate the game object'''
        self.__game = game
        image_path = os.path.abspath('Neta/temp_screen.jpg')
        self.__bg_image = pygame.image.load(image_path)
        self.__screen = self.__game.get_screen()
        self.initiate_grocer()
        self.initiate_stalls()
        self.__basket = list()
        self.__last_vegetable_added = time.time()
        self.__current_mission = None
        self.__can_move = True
        self.__first_shopper_position = self.__game.SCREEN_WIDTH - 220
        self.create_shoppers()
        self.__shopping_list = {TOMATOES: 0, CUCUMBERS : 0, CARROTS: 0}
        self.__vegetables_sold = {TOMATOES: 0, CUCUMBERS : 0, CARROTS: 0}
        self.__basket_text = None
        self.__font  = pygame.font.SysFont("monospace", 17)
        self.__money = 0
        self._start_time = time.time()
        self.__display_day_summary = False
        self.__doing_dialogue = False
        self.__last_enter = time.time()
        self.create_powerups()
        self.__message = None
        self.__message_time = time.time()
        self.__during_mission = False
        self.__last_down_press = time.time()



    def initiate_grocer(self):
        '''initiate the grocer object'''
        self.__grocer = {}
        human_image_path = os.path.abspath('Neta/yarkan.png')
        self.__grocer[IMAGE] = pygame.image.load(human_image_path)
        self.__grocer[POSITION] = (200,self.__game.SCREEN_HEIGHT - GreenGrocerGame.GROCER_IMAGE_HEIGHT - (self.__game.SCREEN_HEIGHT * DIALOG_BOX_SIZE))
        self.__grocer[WIDTH] = GreenGrocerGame.GROCER_IMAGE_WIDTH
        self.__grocer[HEIGHT] = GreenGrocerGame.GROCER_IMAGE_HEIGHT


    def initiate_stalls(self):
        '''initiate the stalls'''
        self.__stalls = {}
        self.__stalls[TOMATOES] = {}
        self.__stalls[TOMATOES][POSITION] = TOMATO_POSITION
        path = os.path.abspath('Neta/tomato.png')
        self.__stalls[TOMATOES][IMAGE] = pygame.image.load(path)

        self.__stalls[CARROTS] = {}
        self.__stalls[CARROTS][POSITION] = CARROT_POSITION
        path = os.path.abspath('Neta/carrot.png')
        self.__stalls[CARROTS][IMAGE] = pygame.image.load(path)

        self.__stalls[CUCUMBERS] = {}
        self.__stalls[CUCUMBERS][POSITION] = CUCUMBER_POSITION
        path = os.path.abspath('Neta/cucumber.png')
        self.__stalls[CUCUMBERS][IMAGE] = pygame.image.load(path)





    def check_keys(self):
        '''move the grocer according to pressed keys
        Add vegetables if needed'''
        pressed_keys = self.__game.get_keys_pressed()

        if pressed_keys[pygame.K_UP] and self.__display_day_summary == True:
            self.__display_day_summary = False
            self.__money = self.display_day_sum()
            self._start_time = time.time()
            self.create_shoppers()
            self.__basket = list()
            self.__shopping_list = {TOMATOES: 0, CUCUMBERS: 0, CARROTS: 0}
            self.__vegetables_sold = {TOMATOES: 0, CUCUMBERS: 0, CARROTS: 0}

        if pressed_keys[pygame.K_RETURN] and self.__doing_dialogue and (time.time() - self.__last_enter > 1):
            self.__dialog.press_enter()
            self.__last_enter = time.time()
            if (self.__dialog.get_done()):
                self.__can_move = True
                self.__basket_text = "Tomatoes: " + str(self.__shopping_list[TOMATOES]) + "     Cucumbers: " + str(
                    self.__shopping_list[CUCUMBERS]) + "     Carrots: " + str(self.__shopping_list[CARROTS])

        if (self.__can_move):
            if pressed_keys[pygame.K_LEFT] and self.__grocer[POSITION][0] >= 150:
                self.__grocer[POSITION] = (self.__grocer[POSITION][0] - GreenGrocerGame.STEPSIZE, self.__grocer[POSITION][1])

            if pressed_keys[pygame.K_RIGHT] and self.__grocer[POSITION][0] <= self.__first_shopper_position - self.__grocer[WIDTH] - 20:
                self.__grocer[POSITION] = (self.__grocer[POSITION][0] + GreenGrocerGame.STEPSIZE, self.__grocer[POSITION][1])


            if pressed_keys[pygame.K_DOWN] and (time.time() - self.__last_down_press > 3):
                if self.__grocer[POSITION][0] >= 0:
                    if (self.__during_mission):
                        self.check_basket()
                    else:
                        self.__during_mission = True
                        if not self.__basket:
                            self.start_basket()

                for vegetable in self.__stalls:
                    if (self.__grocer[POSITION][0] > self.__stalls[vegetable][POSITION][0] and self.__grocer[POSITION][0] < self.__stalls[vegetable][POSITION][1]):
                        if time.time() - self.__last_vegetable_added > 0.5 and len(self.__basket) <= 13:
                            self.__basket.append(vegetable)
                            self.__last_vegetable_added = time.time()


    def display_message(self):
        '''display messages on the screen'''
        if self.__message:
            message = self.__font.render(self.__message, True, (255,0,0))
            self.__screen.blit(message, (180,110))

        if (time.time() - self.__message_time > 3):
            self.__message = None

    def check_basket(self):
        '''check if the basket is as it should be.'''
        self.__during_mission = False
        if self.__shoppers:
            vegetables_in_basket = {TOMATOES : 0, CARROTS : 0, CUCUMBERS: 0}
            for vegetable in self.__basket:
                vegetables_in_basket[vegetable] += 1

            good_basket = True
            for vegetable in self.__basket:
                if self.__shopping_list[vegetable] != vegetables_in_basket[vegetable]:
                    good_basket = False

            if (good_basket):
                self.get_money()
            else:
                self.__message = "These are not the right vegetables"
                self.__message_time = time.time()

            self.__basket = list()
            self.__shopping_list = {TOMATOES: 0, CUCUMBERS: 0, CARROTS: 0}
            self.__shoppers.remove(self.__shoppers[0])
        else:
            self.display_day_sum = True


    def get_money(self):
        '''get money for the shopping list'''
        if self.__basket:
            self.__money += TOMATO_PRICE * self.__shopping_list[TOMATOES] + CARROT_PRICE * self.__shopping_list[CARROTS] + CUCUMBER_PRICE * self.__shopping_list[CUCUMBERS]
            for vegetable in self.__shopping_list:
                self.__vegetables_sold[vegetable] += self.__shopping_list[vegetable]




    def start_basket(self):
        '''start a new basket that you need to fill'''
        if self.__shoppers:
            self.__shopping_list = self.__shoppers[0].get_shopping_list()
            self.__dialog = Dialog(self.__shoppers[0].get_dialogue())
            self.__can_move = False
            self.__doing_dialogue = True
        else:
            self.__display_day_summary = True


    def display_basket(self):
        '''display the current basket'''
        if (self.__basket_text):
            text = self.__font.render(self.__basket_text,True,(0, 0, 139))
            self.__screen.blit(text, (170, 80))


    def display_sidebar(self):
        '''display the amount of money earned'''
        money_text = self.__font.render("Money: " + str("%.2f" % self.__money), True, (255,255,255))
        self.__screen.blit(money_text,(10, 80))

        if (not self.__display_day_summary):
            self.draw_powerups()

            current_time = int (time.time() - self._start_time)
            current_time *= 8
            hours = current_time // 60 + 9
            minutes = current_time % 60
            if (hours < 17):
                time_text = self.__font.render("Clock: " + str(hours) + ":" + str(minutes), True, (255,255,255))
                self.__screen.blit(time_text,(10, 110))
            else:
                self.__display_day_summary = True
        else:
            time_text = self.__font.render("Day Summary", True, (255, 255, 255))
            self.__screen.blit(time_text, (10, 110))



    def check_mouse_clicks(self):
        '''check the mouse clicks'''
        mouse_click,mouse_position = self.__game.get_mouse_click()
        if (mouse_click[0]):
            for powerup in self.__powerups:
                if powerup.hit_power_up(mouse_position):
                    if powerup.get_price() <= self.__money:
                        powerup.get_function()()
                        self.__powerups.remove(powerup)
                        self.__money -= powerup.get_price()
                    else:
                        self.__message = "You don't have enough money for that"
                        self.__message_time = time.time()


    def draw_vegetables(self):
        '''draw the vegetables to the screen'''
        currentPosition = 10
        for vegetable in self.__basket:
            self.__screen.blit(self.__stalls[vegetable][IMAGE], (currentPosition, 5))
            currentPosition += 55


    def main_loop(self):
        '''the main loop for the minigame'''
        self.__screen.fill((0, 0, 0))
        if not (self.__display_day_summary):
            self.__screen.blit(self.__bg_image,(150,60))
            self.__screen.blit(self.__grocer[IMAGE],self.__grocer[POSITION])
            self.draw_vegetables()
            self.draw_shoppers()
            self.display_basket()

            if self.__doing_dialogue:
                self.__dialog.draw_on_screen(self.__game.get_screen())
        else:
            self.display_day_sum()
        self.display_sidebar()
        self.check_keys()

        self.check_mouse_clicks()
        self.display_message()

        return True



    def display_day_sum(self):
        x_position = 150
        y_position = 100
        income = self.__money
        tomato_price = self.__vegetables_sold[TOMATOES] * (TOMATO_PRICE - 0.2)
        cucumber_price = self.__vegetables_sold[CUCUMBERS] * (CUCUMBER_PRICE - 0.2)
        carrot_price = self.__vegetables_sold[CARROTS] * (CARROT_PRICE - 0.2)
        text = ["Vegetables sold today:", str(self.__vegetables_sold[TOMATOES]) + " tomatoes" , str(self.__vegetables_sold[CARROTS]) + " carrots", str(self.__vegetables_sold[CUCUMBERS]) + " cucumbers" , "Expenses:" , "Tomatoes: " + str(tomato_price) , "Carrots: " + str(carrot_price) ,
               "Cucumbers: " + str(cucumber_price) ," " , "Net Income today: " + str( "%.2f" % (income - tomato_price - cucumber_price - carrot_price)), " ", " ", " ", "Click on powerups to buy them", " ", " ", "Press up key to begin the next day"]
        for line in text:
            text_to_print = self.__font.render(line,True,(255,255,255))
            self.__screen.blit(text_to_print, (x_position, y_position))
            y_position += 25

        return income - tomato_price - cucumber_price - carrot_price



    def get_music(self):
        '''get the game's background music'''
        return None


    def get_loop(self):
        '''get the game's main loop'''
        return self.main_loop


    def draw_shoppers(self):
        '''draw the line of shoppers'''
        current_x = self.__first_shopper_position
        for shopper in self.__shoppers:
            self.__screen.blit(shopper.get_image(), (current_x, self.__game.SCREEN_HEIGHT - shopper.HEIGHT - (self.__game.SCREEN_HEIGHT * DIALOG_BOX_SIZE)))
            current_x += shopper.WIDTH + 20

    def create_shoppers(self):
        '''create the shoppers'''
        self.__shoppers = list()
        for i in range(6):
            self.__shoppers.append(Shopper())

    def create_powerups(self):
        '''create the game's powerups'''
        current_y = 160
        self.__powerups = list()
        self.__powerups.append(PowerUps(self.local_ad,'Neta/ad.jpg',210,(47,current_y)))
        current_y += 65
        self.__powerups.append(PowerUps(self.sale,'Neta/sale.jpg',150,(47,current_y)))
        current_y += 65
        self.__powerups.append(PowerUps(self.gray_man,'Neta/dark_person.png',0,(47,current_y)))
        current_y += 65
        self.__powerups.append(PowerUps(self.organic,'Neta/organic.png',325,(47,current_y)))


    def draw_powerups(self):
        '''draw the powerups to the screen'''
        for powerup in self.__powerups:
            self.__screen.blit(powerup.get_image(),powerup.get_position())



    ##########################
        #Power up functions
    #########################

    def local_ad(self):
        print("ad")

    def sale(self):
        print("sale")

    def gray_man(self):
        print("gray man")

    def organic(self):
        print("organic")