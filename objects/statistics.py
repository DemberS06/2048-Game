# statistics.py
import pygame

from IA.buffer import Buffer
from settings import NORM, STATISTICS_SIZE, BLACK, DATA_LN, BORDER_LN

class Statistics:
    def __init__(self):
        self.final_games = 0
        self.first_time = []
        self.max_val = [0]
        self.moves = [0]
        self.invalid = [0]

        for _ in range(NORM):
            self.first_time.append(-1)

    def push(self, Buff = Buffer(), moves = 0):
        if Buff.done==0:
            return
        self.final_games+=1
        mx = 0
        for v in Buff.A.board:
            for u in v:
                if mx<u:mx=u
        
        self.max_val.append(mx)
        self.moves.append(moves)
        self.invalid.append(Buff.invalid)

        if self.first_time[mx]==-1: self.first_time[mx] = self.final_games

        if len(self.max_val)>STATISTICS_SIZE:
            del self.max_val[0]
            del self.moves[0]
            del self.invalid[0]
        
    def draw(self, screen):
        moves = 0
        invalid = 0
        fr = []
        for _ in range(NORM):
            fr.append(0)
        
        for x in self.moves: moves+=x
        for x in self.invalid: invalid+=x
        for x in self.max_val: fr[x]+=1

        if self.final_games>0:moves/=len(self.moves)

        font=pygame.font.SysFont("Arial", 15)

        for i in range(NORM-1):
            x=i+1
            txt=font.render(str(2**x)+" -> FT: "+str(self.first_time[x])+"  Fr: "+str(fr[x]), True, BLACK)
            screen.blit(txt, (0,17*x+DATA_LN))

        txt=font.render("MOV_INV: "+str(invalid)+"  MOV_MEAN: "+str(moves), True, BLACK)
        screen.blit(txt, (BORDER_LN,DATA_LN+17))



        