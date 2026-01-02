# game.py

import pygame

from objects.board import Board
from objects.match import Match
from settings import (
    BORDER_LN, CELL_LN, EDGE_LN, DATA_LN
)

class Game:
    def __init__(self, screen):
        self.screen = screen

        self.dir=[0, 0, 0, 0]

        self.match=Match()
        self.b=Board()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dir = [0, 0, 0, 0]
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dir[0]=1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dir[1]=1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dir[2]=1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dir[3]=1

        if dir[0]+dir[1]+dir[2]+dir[3]>1: return True

        for i in range(4):
            if dir[i] and self.dir[i]:
                return True
            if dir[i]:
                ok = self.match.move(i)
                self.dir=dir
                return ok
            
        self.dir=dir
        return True
        

    def draw(self):
        self.screen.fill((0,0,0))
        for i in range(4):
            for j in range(4):
                X=BORDER_LN + j*(CELL_LN+EDGE_LN)
                Y=BORDER_LN + DATA_LN + i*(CELL_LN+EDGE_LN)
                font=pygame.font.SysFont("Arial", 48)
                NUM=font.render(str(2**self.match.board.board[i][j]), True, (255,255,255))
                if self.match.board.board[i][j]!=0:
                    self.screen.blit(NUM, (X, Y))
        
