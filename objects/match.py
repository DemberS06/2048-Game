import pygame
from objects.board import Board
from objects.statistics import Statistics
from IA.buffer import Buffer

from settings import (
    BORDER_LN, CELL_LN, EDGE_LN, DATA_LN,
    BLACK, WHITE, R_MN, R_MX, L_R, G_MN, G_MX, L_G, B_MN, B_MX, L_B, UL,
    INVALID_PENALTY, GAME_OVER_PENALTY, TIME_PENALTY, CLIP_MIN, CLIP_MAX, 
    MERGE_SCALE, STRUCT_SCALE, BONUS_SCALE, FATAL_FACTOR, FATAL_BIASE,
    W_EMPTY, W_CORNER, W_MONO, W_SNAKE, W_MERGE_POT, CHAIN_ALPHA, LINE_BASE_WEIGHT, NORM
)

class Match:
    def __init__(self, st = Statistics()):
        self.board=Board()
        self.score=0
        self.moves=0
        self.st=st
        self.mx=0
        self.get_val()
    
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
    
    def get_val(self):
        old_mx = self.mx
        mx = 0
        empties = 0
        H = self.board.H
        W = self.board.W
        B = self.board.board
        for i in range(H):
            for j in range(W):
                v = B[i][j]
                if v == 0:
                    empties += 1
                if v > mx:
                    mx = v
        empty_score = empties / (H * W)
        corners = 0
        corners += 1 if B[0][0] == mx else 0
        corners += 1 if B[0][W-1] == mx else 0
        corners += 1 if B[H-1][0] == mx else 0
        corners += 1 if B[H-1][W-1] == mx else 0
        if corners == 1:
            corner_score = 1.0
        elif corners > 1:
            corner_score = -1.0
        else:
            corner_score = 0.0
        mono_acc = 0.0
        mono_cnt = 0
        norm_mx = max(1.0, mx)
        for i in range(H):
            for j in range(W - 2):
                a = B[i][j]
                b = B[i][j + 1]
                c = B[i][j + 2]
                if b == 0:
                    continue
                dsum = (b - a) + (c - b)
                if dsum > 0:
                    sign = 1.0
                elif dsum < 0:
                    sign = -1.0
                else:
                    sign = 0.0
                lit = abs(dsum) / norm_mx
                mono_acc += sign * lit
                mono_cnt += 1
        for j in range(W):
            for i in range(H - 2):
                a = B[i][j]
                b = B[i + 1][j]
                c = B[i + 2][j]
                if b == 0:
                    continue
                dsum = (b - a) + (c - b)
                if dsum > 0:
                    sign = 1.0
                elif dsum < 0:
                    sign = -1.0
                else:
                    sign = 0.0
                lit = abs(dsum) / norm_mx
                mono_acc += sign * lit
                mono_cnt += 1
        mono_score = (mono_acc / mono_cnt) if mono_cnt > 0 else 0.0
        def snake_lines_from_corner(B, H, W, corner):
            lines = []
            if corner == 0:
                for i in range(H):
                    row = [B[i][j] for j in range(W)]
                    if i % 2 == 1:
                        row = list(reversed(row))
                    lines.append(row)
            elif corner == 1:
                for i in range(H):
                    row = [B[i][j] for j in range(W-1, -1, -1)]
                    if i % 2 == 1:
                        row = list(reversed(row))
                    lines.append(row)
            elif corner == 2:
                for idx, i in enumerate(range(H-1, -1, -1)):
                    row = [B[i][j] for j in range(W-1, -1, -1)]
                    if idx % 2 == 1:
                        row = list(reversed(row))
                    lines.append(row)
            else:
                for idx, i in enumerate(range(H-1, -1, -1)):
                    row = [B[i][j] for j in range(W)]
                    if idx % 2 == 1:
                        row = list(reversed(row))
                    lines.append(row)
            return lines
        def line_pendents(line, mx):
            s_sum = 0.0
            s_cnt = 0
            mag_sum = 0.0
            mag_cnt = 0
            L = len(line)
            norm = max(1.0, mx)
            for k in range(L - 2):
                a = line[k]
                b = line[k+1]
                c = line[k+2]
                if b == 0:
                    continue
                dsum = (c - a)
                if dsum > 0:
                    s = 1.0
                elif dsum < 0:
                    s = -1.0
                else:
                    s = 0.0
                lit = abs(dsum) / norm
                s_sum += s
                s_cnt += 1
                mag_sum += lit
                mag_cnt += 1
            sign_mean = (s_sum / s_cnt) if s_cnt > 0 else 0.0
            mag_mean = (mag_sum / mag_cnt) if mag_cnt > 0 else 0.0
            return sign_mean, mag_mean
        def snake_chain_score(B, H, W, mx, corner):
            lines = snake_lines_from_corner(B, H, W, corner)
            total = 0.0
            weight_sum = 0.0
            prev_perf = 0.0
            prev_sign = None
            for idx, line in enumerate(lines):
                sign_mean, mag_mean = line_pendents(line, mx)
                if prev_sign is None:
                    sign_alignment = sign_mean
                else:
                    sign_alignment = -sign_mean * prev_sign
                chain_mult = 1.0 + CHAIN_ALPHA * prev_perf
                line_score = sign_alignment * mag_mean * chain_mult * LINE_BASE_WEIGHT
                total += line_score
                weight_sum += (abs(chain_mult) * LINE_BASE_WEIGHT)
                prev_perf = abs(sign_alignment * mag_mean)
                if sign_mean != 0.0:
                    prev_sign = sign_mean
            return (total / (weight_sum + 1e-9)) if weight_sum > 0 else 0.0
        snake_scores = []
        is_corner = (B[0][0] == mx) or (B[0][W-1] == mx) or (B[H-1][0] == mx) or (B[H-1][W-1] == mx)
        if is_corner:
            for c in range(4):
                sc = snake_chain_score(B, H, W, mx, c)
                snake_scores.append(sc)
            snake_score = max(snake_scores)
        else:
            snake_score = snake_chain_score(B, H, W, mx, 0)
        merge_pot = 0.0
        for i in range(H):
            for j in range(W):
                v = B[i][j]
                if v == 0:
                    continue
                if j + 1 < W and B[i][j + 1] == v:
                    merge_pot += v
                if i + 1 < H and B[i + 1][j] == v:
                    merge_pot += v
        merge_pot_score = merge_pot / (norm_mx * (H * W))
        raw = (W_EMPTY * empty_score +
            W_CORNER * corner_score +
            W_MONO * mono_score +
            W_SNAKE * snake_score +
            W_MERGE_POT * merge_pot_score)
        total_w = (W_EMPTY + W_CORNER + W_MONO + W_SNAKE + W_MERGE_POT)
        val = raw / (total_w + 1e-9)
        self.val = val
        self.mx = mx
        if mx > old_mx:
            return mx/NORM
        return 0


    def IA_move(self, d, IA):
        nxt = Board()
        nxt.equal(self.board)

        #print(d)

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
        equal=self.board.is_equal(nxt)
        
        nxt.push()
        self.board.equal(nxt)
        
        buffer.R-=STRUCT_SCALE*self.val
        new_merge = self.get_val()
        buffer.R+=STRUCT_SCALE*self.val
        
        if equal or self.val<FATAL_BIASE+FATAL_FACTOR*self.mx:
            buffer.R, buffer.invalid, buffer.done = INVALID_PENALTY, 1, 1
            
            IA.remember(buffer)
            self.st.push(buffer, self.moves)

            if equal:
                print("Invalid Move")
            else:
                print("Fatal board")

            return False
        
        buffer.R+=MERGE_SCALE*score/NORM + BONUS_SCALE*new_merge
        
        self.score+=2**score
        self.moves+=1

        ok = nxt.push()

        if ok == False:
            ok = ok or (nxt.move_u()>0)
            ok = ok or (nxt.move_l()>0)
            ok = ok or (nxt.move_d()>0)
            ok = ok or (nxt.move_r()>0)
        
        if not ok:
            buffer.R+=GAME_OVER_PENALTY
            buffer.done=1
        
        if buffer.R>CLIP_MAX: buffer.R=CLIP_MAX
        if buffer.R<CLIP_MIN: buffer.R=CLIP_MIN

        IA.remember(buffer)
        self.st.push(buffer, self.moves)

        print("R :"+str(buffer.R))
        print("G :"+str(self.val))

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

    