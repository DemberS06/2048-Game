import pygame
from objects.board import Board
from IA.buffer import Buffer

from settings import (
    BORDER_LN, CELL_LN, EDGE_LN, DATA_LN,
    BLACK, WHITE, R_MN, R_MX, L_R, G_MN, G_MX, L_G, B_MN, B_MX, L_B, UL,
    INVALID_PENALTY, GAME_OVER_PENALTY, WIN_REWARD, TIME_PENALTY, MERGE_SCALE, CLIP_MIN, CLIP_MAX, BONUS
)

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
    
    def IA_move(self, d, IA):
        nxt = Board()
        nxt.equal(self.board)

        print(d)

        score = 0
        buffer = Buffer()
        buffer.A.equal(self.board)
        buffer.mov=d
        
        match d:
            case 0:
                score=nxt.move_u()
            case 1:
                score=nxt.move_l()
            case 2:
                score=nxt.move_d()
            case 3:
                score=nxt.move_r()
        
        buffer.B.equal(nxt)
        buffer.R=MERGE_SCALE*score
        
        if self.board.is_equal(nxt):
            buffer.R=INVALID_PENALTY
            IA.remember(buffer)
            return False
        
        self.score+=2**score
        self.moves+=1

        nxt.push()

        self.board.equal(nxt)
        self.board.push()

        ok = nxt.push()

        if ok == False:
            ok = ok or (nxt.move_u()>0)
            ok = ok or (nxt.move_l()>0)
            ok = ok or (nxt.move_d()>0)
            ok = ok or (nxt.move_r()>0)

        if ok:
            cnt=0
            for v in self.board.board:
                for u in v:
                    cnt+=(u==0)
            buffer.R+=TIME_PENALTY+BONUS*cnt
            buffer.done=0
        else:
            buffer.R=GAME_OVER_PENALTY
            buffer.done=1
        
        if buffer.R>CLIP_MAX: buffer.R=CLIP_MAX
        if buffer.R<CLIP_MIN: buffer.R=CLIP_MIN
            
        IA.remember(buffer)
        return ok

    def draw(self, screen):
        font=pygame.font.SysFont("Arial", 48)
        txt=font.render("SCORE: "+str(self.score)+"  MOVES: "+str(self.moves), True, BLACK)
        screen.blit(txt, (0,0))

        for i in range(self.board.H):
            for j in range(self.board.W):
                X=BORDER_LN + j*(CELL_LN+EDGE_LN)
                Y=BORDER_LN + DATA_LN + i*(CELL_LN+EDGE_LN)

                cur=self.board.board[i][j]
                sz=self.board.H*self.board.W+2
                cell_color = (R_MN+cur*(R_MX-R_MN)/sz, G_MN+cur*(G_MX-G_MN)/sz, B_MN+cur*(B_MX-B_MN)/sz)
                
                cell = pygame.Rect(X, Y, CELL_LN, CELL_LN)
                pygame.draw.rect(screen, cell_color, cell)
                
                light = L_R*cell_color[0] + L_G*cell_color[1] + L_B*cell_color[2] 
                text_color = BLACK
                if light < UL: text_color = WHITE

                txt=font.render(str(2**self.board.board[i][j]), True, text_color)
                rect_txt=txt.get_rect()
                rect_txt.center=(X+CELL_LN/2, Y+CELL_LN/2)
                if self.board.board[i][j]!=0:
                    screen.blit(txt, rect_txt)
        return

    