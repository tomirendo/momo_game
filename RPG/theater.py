from RPG.board import Board

class TheaterBoard(Board):
    def find_selected_character(self):
        return self.static_characters[0]
