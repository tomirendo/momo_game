from RPG.board import Board 
from RPG.theater import TheaterBoard
from RPG.path import street, theater

class StreetBoard(Board):
    def is_done(self):
        dark_person = self.static_characters[0]
        return dark_person.is_dialog_done()
    def next_board(self):
        return TheaterBoard(self.game, self.owner, "./RPG/theater.json", theater)
