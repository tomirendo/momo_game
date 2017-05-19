import pygame
import random
import os
import json

json_file_path = os.path.abspath("Neta/Shopper1.json")
json_file = open(json_file_path)
json_str = json_file.read()
shopper_dictionary = json.loads(json_str)

img1 = "Neta/shopper1.png"
img1_path = os.path.abspath(img1)
img2 = "Neta/shopper2.png"
img2_path = os.path.abspath(img2)
img3 = "Neta/shopper3.png"
img3_path = os.path.abspath(img3)
img4 = "Neta/shopper4.jpg"
img4_path = os.path.abspath(img4)
img6 = "Neta/shopper6.png"
img6_path = os.path.abspath(img6)
img7 = "Neta/shopper7.png"
img7_path = os.path.abspath(img7)
img8 = "Neta/shopper8.jpeg"
img8_path = os.path.abspath(img8)
img9 = "Neta/shopper9.png"
img9_path = os.path.abspath(img9)

img_list = list()
img_list.append(pygame.image.load(img1_path))
img_list.append(pygame.image.load(img2_path))
img_list.append(pygame.image.load(img3_path))
img_list.append(pygame.image.load(img4_path))
img_list.append(pygame.image.load(img6_path))
img_list.append(pygame.image.load(img7_path))
img_list.append(pygame.image.load(img8_path))
img_list.append(pygame.image.load(img9_path))

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
        img_num = random.randint(0,len(img_list) - 1)
        self.__image = img_list[img_num]

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



