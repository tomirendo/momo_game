import pygame
import random
import os
import json

json_file_path = os.path.abspath("Neta/Shopper1.json")
json_file = open(json_file_path)
json_str = json_file.read()
shopper_dictionary = json.loads(json_str)


DIALOGUE = 'Dialog'
ORDER = 'order'
class Shopper():
    '''a shopper at the store'''

    HEIGHT = 200
    WIDTH = 60
    SHOPPER_NUMBER = 1
    SHOPPER_LIST = list()

    def __init__(self, dummy):
        '''create a new shopper'''
        path = os.path.abspath('Neta/Human.jpg')
        self.__image = pygame.image.load(path)
        if (not dummy):
            self.__shopping_list = shopper_dictionary["shopper" + str(Shopper.SHOPPER_NUMBER)][ORDER]
            self.__dialogue = shopper_dictionary["shopper"+str(Shopper.SHOPPER_NUMBER)][DIALOGUE]
            Shopper.SHOPPER_NUMBER += 1
        else:
            self.__dialogue = shopper_dictionary["Dummy"].copy()
            self.__shopping_list = {"tomatoes" : random.randint(1,4), "carrots" : random.randint(1,4), "cucumbers" : random.randint(1,4)}



    def get_image(self):
        '''get the shopper's image'''
        return self.__image


    def get_shopping_list(self):
        '''get the shopper's shopping list'''
        return self.__shopping_list


    def get_dialogue(self):
        '''get the shopper's dialogue'''
        current_dialog = self.__dialogue
        while current_dialog['answers'][0]['next_dialog'] is not None:
            current_dialog = current_dialog['answers'][0]['next_dialog']
        current_dialog['text'] += "I'd like " + str(self.__shopping_list['tomatoes']) + " tomatoes, " + str(self.__shopping_list['carrots']) + " carrots and " + str(self.__shopping_list['cucumbers']) + " cucumbers, please."
        return self.__dialogue



