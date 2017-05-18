from RPG.board import Board

class TheaterBoard(Board):
    def find_selected_character(self):
        return self.static_characters[0]
    def is_done(self):
        return self.static_characters[0].is_dialog_done()
    def next_board(self):
        return None
