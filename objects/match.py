import pygame
from objects.board import Board

class Match:
    def __init__(self):
        self.board=Board()
        self.score=0
        self.moves=0
    
    def move(self, d):
        nxt = Board()
        nxt.equal(self.board)

        print(d)

        score = 0
        
        match d:
            case 0:
                score=nxt.move_u()
            case 1:
                score=nxt.move_l()
            case 2:
                score=nxt.move_d()
            case 3:
                score=nxt.move_r()
        
        if self.board.is_equal(nxt):
            return True
        
        self.score+=2**score
        self.moves+=1

        self.board.equal(nxt)
        return self.board.push()

    def draw(self, screen, i, j):
        return

    