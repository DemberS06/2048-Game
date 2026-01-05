from objects.board import Board

class Buffer:
    def __init__(self):
        self.A = Board()
        self.B = Board()
        self.mov = -1
        self.R = 0
        self.done = 0