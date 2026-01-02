# game.py

import pygame

from objects.board import Board
from settings import (
    BORDER_LN, CELL_LN, EDGE_LN, DATA_LN
)

class Game:
    def __init__(self, screen):
        self.screen = screen

        self.b=Board()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.b.move_r()
            self.b.push()
        if keys[pygame.K_a]:
            self.b.move_l()
            self.b.push()
        if keys[pygame.K_s]:
            self.b.move_d()
            self.b.push()
        if keys[pygame.K_w]:
            self.b.move_u()
            self.b.push()

    def draw(self):
        self.screen.fill((0,0,0))
        for i in range(4):
            for j in range(4):
                X=BORDER_LN + j*(CELL_LN+EDGE_LN)
                Y=BORDER_LN + DATA_LN + i*(CELL_LN+EDGE_LN)
                font=pygame.font.SysFont("Arial", 48)
                NUM=font.render(str(2**self.b.board[i][j]), True, (255,255,255))
                if self.b.board[i][j]!=0:
                    self.screen.blit(NUM, (X, Y))
        
