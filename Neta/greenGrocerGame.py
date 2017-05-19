import pygame
import os
import time
from momo_game.Neta.Shopper import Shopper
from momo_game.RPG.dialog import Dialog, DIALOG_BOX_SIZE
from momo_game.Neta.power_ups import PowerUps
import json

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
CARROT_POSITION = (11+150,124+150)
TOMATOES = 'tomatoes'
TOMATO_POSITION = (134+150,262+150)
CUCUMBERS = 'cucumbers'
CUCUMBER_POSITION = (265+150,515)

speech_bubble_path = os.path.abspath('Neta/speechBubble.png')
SPEECH_BUBBLE_IMAGE = pygame.image.load(speech_bubble_path)


class GreenGrocerGame():
    '''The green Grocer minigame for the Momo game'''

    STEPSIZE = 3
    GROCER_IMAGE_WIDTH = 90
    GROCER_IMAGE_HEIGHT = 300
    TOMATO_PRICE = 0.9
    CARROT_PRICE = 1.1
    CUCUMBER_PRICE = 0.5


    def __init__(self,game):
        '''Initiate the game object'''
        self.__game = game
        self.__ad = False
        self.__gray_man = False
        self.__salee = False
        self.__organic = False
        image_path = os.path.abspath('Neta/veg.png')
        self.__bg_image = pygame.image.load(image_path)
        self.__screen = self.__game.get_screen()
        self.initiate_grocer()
        self.initiate_stalls()
        self.__basket = list()
        self.__last_vegetable_added = time.time()
        self.__current_mission = None
        self.__can_move = True
        self.__first_shopper_position = self.__game.SCREEN_WIDTH - 150
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
        self.__number_of_days = 5
        self.__finished = False
        self.__morning = 9
        self.__night = 17
        self.__gray_man_dialogue = False



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
        path = os.path.abspath('gal/tom.png')
        self.__stalls[TOMATOES][IMAGE] = pygame.image.load(path)

        self.__stalls[CARROTS] = {}
        self.__stalls[CARROTS][POSITION] = CARROT_POSITION
        path = os.path.abspath('gal/carrot.png')
        self.__stalls[CARROTS][IMAGE] = pygame.image.load(path)

        self.__stalls[CUCUMBERS] = {}
        self.__stalls[CUCUMBERS][POSITION] = CUCUMBER_POSITION
        path = os.path.abspath('gal/cuc.png')
        self.__stalls[CUCUMBERS][IMAGE] = pygame.image.load(path)





    def check_keys(self):
        '''move the grocer according to pressed keys
        Add vegetables if needed'''
        pressed_keys = self.__game.get_keys_pressed()

        if pressed_keys[pygame.K_UP] and self.__display_day_summary == True:
            self.__display_day_summary = False
            self.__money = self.display_day_sum()
            self._start_time = time.time()
            self.__basket = list()
            self.__shopping_list = {TOMATOES: 0, CUCUMBERS: 0, CARROTS: 0}
            self.__vegetables_sold = {TOMATOES: 0, CUCUMBERS: 0, CARROTS: 0}
            self.create_shoppers()

        if pressed_keys[pygame.K_RETURN] and self.__doing_dialogue and (time.time() - self.__last_enter > 1):
            self.__dialog.press_enter()
            self.__last_enter = time.time()
            if (self.__dialog.get_done()):
                self.__can_move = True
                self.__gray_man_dialogue = False
                self.__basket_text = "Tomatoes: " + str(self.__shopping_list[TOMATOES]) + "     Cucumbers: " + str(
                    self.__shopping_list[CUCUMBERS]) + "     Carrots: " + str(self.__shopping_list[CARROTS])

        if (self.__can_move):
            if pressed_keys[pygame.K_LEFT] and self.__grocer[POSITION][0] >= 150:
                self.__grocer[POSITION] = (self.__grocer[POSITION][0] - GreenGrocerGame.STEPSIZE, self.__grocer[POSITION][1])

            if pressed_keys[pygame.K_RIGHT] and self.__grocer[POSITION][0] <= self.__first_shopper_position - self.__grocer[WIDTH] - 20:
                self.__grocer[POSITION] = (self.__grocer[POSITION][0] + GreenGrocerGame.STEPSIZE, self.__grocer[POSITION][1])


            if pressed_keys[pygame.K_DOWN]:
                if (time.time() - self.__last_down_press > 1):
                    self.__last_down_press = time.time()
                    if self.__grocer[POSITION][0] >= self.__game.SCREEN_WIDTH - 300:
                        if (self.__during_mission):
                            self.check_basket()
                        else:
                            self.start_basket()
                            self.__during_mission = True

                for vegetable in self.__stalls:
                    if (self.__grocer[POSITION][0]  > self.__stalls[vegetable][POSITION][0] - 10 and self.__grocer[POSITION][0] + self.__grocer[WIDTH] < self.__stalls[vegetable][POSITION][1]):
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
            for vegetable in self.__shopping_list:
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
            self.display_day_summary = True


    def get_money(self):
        '''get money for the shopping list'''
        if self.__basket:
            self.__money += GreenGrocerGame.TOMATO_PRICE * self.__shopping_list[TOMATOES] + GreenGrocerGame.CARROT_PRICE * self.__shopping_list[CARROTS] + GreenGrocerGame.CUCUMBER_PRICE * self.__shopping_list[CUCUMBERS]
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
        money_text = self.__font.render("Money: " + str("%.2f" % self.__money), True, (0,0,0))
        self.__screen.blit(money_text,(10, 80))

        if (not self.__display_day_summary):
            self.draw_powerups()

            current_time = int (time.time() - self._start_time)
            current_time *= 4
            hours = current_time // 60 + self.__morning
            minutes = current_time % 60
            if (hours < self.__night):
                time_text = self.__font.render("Clock: " + str(hours) + ":" + str(minutes), True, (0,0,0))
                self.__screen.blit(time_text,(10, 110))
            else:
                self.__display_day_summary = True
        else:
            time_text = self.__font.render("Day Summary", True, (0, 0, 0))
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
        self.__screen.fill((250, 250, 250))
        if not (self.__display_day_summary):
            self.__screen.blit(self.__bg_image,(150,120))
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

        if (self.__gray_man_dialogue):
            self.__screen.blit(pygame.image.load('Neta/gray_man.png'), (self.__grocer[POSITION][0] + self.__grocer[WIDTH] + 50, self.__grocer[POSITION][1]))

        return not self.__finished



    def display_day_sum(self):
        if self.__number_of_days <= 5:
            x_position = 150
            y_position = 100
            income = self.__money
            tomato_price = self.__vegetables_sold[TOMATOES] * (GreenGrocerGame.TOMATO_PRICE - 0.2)
            cucumber_price = self.__vegetables_sold[CUCUMBERS] * (GreenGrocerGame.CUCUMBER_PRICE - 0.2)
            carrot_price = self.__vegetables_sold[CARROTS] * (GreenGrocerGame.CARROT_PRICE - 0.2)
            text = ["Vegetables sold today:", str(self.__vegetables_sold[TOMATOES]) + " tomatoes" , str(self.__vegetables_sold[CARROTS]) + " carrots", str(self.__vegetables_sold[CUCUMBERS]) + " cucumbers" , "Expenses:" , "Tomatoes: " + str("%.2f" % tomato_price) , "Carrots: " + str("%.2f" % carrot_price) ,
                   "Cucumbers: " + str("%.2f" % cucumber_price) ," " , "Net Income today: " + str( "%.2f" % (income - tomato_price - cucumber_price - carrot_price)), " ", " ", " ", "Click on powerups to get them", " ", " ", "Press up key to begin the next day"]
            for line in text:
                text_to_print = self.__font.render(line,True,(0,0,0))
                self.__screen.blit(text_to_print, (x_position, y_position))
                y_position += 25
            return income - tomato_price - cucumber_price - carrot_price
        else:
            self.__finished = True



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
        if (self.__gray_man):
            for i in range(25):
                self.__shoppers.append(Shopper(True))

        else:
            for i in range(6):
                self.__shoppers.append(Shopper(False))

            if self.__ad is True:
                for i in range(10):
                    self.__shoppers.append(Shopper(True))

            if self.__salee:
                for shopper in self.__shoppers:
                    remainder = 12 - (shopper.get_shopping_list()[TOMATOES] + shopper.get_shopping_list()[CUCUMBERS] + shopper.get_shopping_list()[CARROTS])
                    shopper.get_shopping_list()[CUCUMBERS] += remainder



    def create_powerups(self):
        '''create the game's powerups'''
        current_y = 160
        self.__powerups = list()
        self.__powerups.append(PowerUps(self.local_ad,'Neta/ad.jpg',210,(5,current_y)))
        current_y += 65
        self.__powerups.append(PowerUps(self.sale,'Neta/sale.jpg',150,(5,current_y)))
        current_y += 65
        self.__powerups.append(PowerUps(self.gray_man,'Neta/dark_person.png',0,(5,current_y)))
        current_y += 65
        self.__powerups.append(PowerUps(self.organic,'Neta/organic.png',325,(5,current_y)))


    def draw_powerups(self):
        '''draw the powerups to the screen'''
        for powerup in self.__powerups:
            self.__screen.blit(powerup.get_image(),powerup.get_position())



    ##########################
        #Power up functions
    #########################

    def local_ad(self):
        self.__ad = True
        self.__message = "The ad is attracting new costumers to you store"

    def sale(self):
        self.__salee = True
        self.__message = "As a result of your sale, people are buying more vegetables"
        GreenGrocerGame.CARROT_PRICE -= 0.1
        GreenGrocerGame.CUCUMBER_PRICE -= 0.1
        GreenGrocerGame.TOMATO_PRICE -= 0.1

    def gray_man(self):
        self.__gray_man = True
        path = os.path.abspath('gal/angry_yarkan.png')
        self.__grocer[IMAGE] = pygame.image.load(path)
        bg_path = os.path.abspath('Neta/bg_gray.png')
        self.__bg_image = pygame.image.load(bg_path)
        self.__morning = 8
        self.night = 20
        self.create_shoppers()
        self.__can_move = False
        self.__doing_dialogue = True
        json_file_path = os.path.abspath("Neta/gray_man_grocer_conv.json")
        json_file = open(json_file_path)
        json_str = json_file.read()
        self.__dialog = Dialog(json.loads(json_str))
        self.__gray_man_dialogue = True




    def organic(self):
        self.__organic = True
        GreenGrocerGame.CARROT_PRICE += 0.5
        GreenGrocerGame.CUCUMBER_PRICE += 0.5
        GreenGrocerGame.TOMATO_PRICE += 0.5
        self.__message = "Organic vegetables will allow you to increase prices and attract more costumers"