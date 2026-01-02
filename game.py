# game.py

import pygame

from objects.board import Board
from objects.match import Match
from settings import WHITE

class Game:
    def __init__(self, screen):
        self.screen = screen

        self.dir=[0, 0, 0, 0]

        self.match=Match()
        self.b=Board()

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            return False

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
        self.screen.fill(WHITE)
        self.match.draw(self.screen)
        
        
