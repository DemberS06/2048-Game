# Board.py
import pygame
import random
from settings import W_CELLS, H_CELLS

class Board:
    def __init__(self):
        self.W, self.H=W_CELLS, H_CELLS
        self.board=self.create_board()
        self.push()
        self.push()

    def create_board(self):
        return [[0]*self.H for _ in range(self.W)]
    
    def push(self):
        empty_cells = [
            (i, j)
            for i in range(self.H)
            for j in range(self.W)
            if self.board[i][j] == 0
        ]
        if not empty_cells:
            return False

        i, j = random.choice(empty_cells)
        self.board[i][j] = 2 if random.random() < 0.1 else 1
        return True
    
    def equal(self, nxt):
        for i in range(self.H):
            for j in range(self.W):
                self.board[i][j]=nxt.board[i][j]

    def is_equal(self, nxt):
        for i in range(self.H):
            for j in range(self.W):
                if self.board[i][j] != nxt.board[i][j]:
                    return False
        return True
    
    def move_r(self):
        score = 0
        
        for i in range(self.H):
            for j in range(self.W):
                x=j
                if self.board[i][x] == 0: continue
                for k in range(self.W-j-1):
                    y=j+k+1
                    if self.board[i][y] == 0: continue
                    if self.board[i][x] != self.board[i][y]: break
                    score+=self.board[i][x]
                    self.board[i][x]+=1
                    self.board[i][y]=0
                    break

        for i in range(self.H):
            for j in range(self.W):
                x=self.W-j-1 
                if self.board[i][x] == 0: continue
                for k in range(j):
                    y=self.W-k-1
                    if self.board[i][y] != 0: continue
                    self.board[i][y]=self.board[i][x]
                    self.board[i][x]=0
                    break

        return score

    def move_l(self):
        score = 0
        
        for i in range(self.H):
            for j in range(self.W):
                x=self.W-j-1
                if self.board[i][x] == 0: continue
                for k in range(self.W-j-1):
                    y=x-k-1
                    if self.board[i][y] == 0: continue
                    if self.board[i][x] != self.board[i][y]: break
                    score+=self.board[i][x]
                    self.board[i][x]+=1
                    self.board[i][y]=0
                    break

        for i in range(self.H):
            for j in range(self.W):
                x=j
                if self.board[i][x] == 0: continue
                for k in range(j):
                    y=k
                    if self.board[i][y] != 0: continue
                    self.board[i][y]=self.board[i][x]
                    self.board[i][x]=0
                    break

        return score

    def move_d(self):
        score = 0
        
        for i in range(self.W):
            for j in range(self.H):
                x=j
                if self.board[x][i] == 0: continue
                for k in range(self.H-j-1):
                    y=j+k+1
                    if self.board[y][i] == 0: continue
                    if self.board[x][i] != self.board[y][i]: break
                    score+=self.board[x][i]
                    self.board[x][i]+=1
                    self.board[y][i]=0
                    break

        for i in range(self.W):
            for j in range(self.H):
                x=self.H-j-1 
                if self.board[x][i] == 0: continue
                for k in range(j):
                    y=self.H-k-1
                    if self.board[y][i] != 0: continue
                    self.board[y][i]=self.board[x][i]
                    self.board[x][i]=0
                    break

        return score

    def move_u(self):
        score = 0
        
        for i in range(self.W):
            for j in range(self.H):
                x=self.H-j-1
                if self.board[x][i] == 0: continue
                for k in range(self.H-j-1):
                    y=x-k-1
                    if self.board[y][i] == 0: continue
                    if self.board[x][i] != self.board[y][i]: break
                    score+=self.board[x][i]
                    self.board[x][i]+=1
                    self.board[y][i]=0
                    break

        for i in range(self.W):
            for j in range(self.H):
                x=j
                if self.board[x][i] == 0: continue
                for k in range(j):
                    y=k
                    if self.board[y][i] != 0: continue
                    self.board[y][i]=self.board[x][i]
                    self.board[x][i]=0
                    break

        return score

    