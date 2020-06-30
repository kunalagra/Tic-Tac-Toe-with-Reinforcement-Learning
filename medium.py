import random
import pygame as pg 
import sys 
import time 
from pygame.locals import *

width, height = 400, 400

POSITIONS = list(zip([30, width / 3 + 30, width / 3 * 2 + 30] * 3, [30] * 3 + [height / 3 + 30] * 3 + [height / 3 * 2 + 30] * 3))

LIMITS = list(zip([width / 3, width / 3 * 2, width] * 3, [height / 3] * 3 + [height / 3 * 2] * 3 + [height] * 3))
                
ROW1 = (0, 1, 2)
ROW2 = (3, 4, 5)
ROW3 = (6, 7, 8)

COL1 = (0, 3, 6)
COL2 = (1, 4, 7)
COL3 = (2, 5, 8)

LDIAG = (0, 4, 8)
RDIAG = (2, 4, 6)
 
CHECK = [ROW1, ROW2, ROW3, COL1, COL2, COL3, LDIAG, RDIAG]
               
white = (255, 255, 255) 

line_color = (0, 0, 0) 

CROSS = 'x'
NOUGHT = 'o'

pg.init() 

fps = 30

CLOCK = pg.time.Clock() 

screen = pg.display.set_mode((width, height + 100), 0, 32) 

pg.display.set_caption("Tic Tac Toe") 

LINEARGS = {
    ROW1 : (screen, (250, 0, 0), (20, height / 6), (width - 20, height / 6), 4),
    ROW2 : (screen, (250, 0, 0), (20, height / 2), (width - 20, height / 2), 4),
    ROW3 : (screen, (250, 0, 0), (20, height / 6 * 5), (width - 20, height / 6 * 5), 4),
    COL1 : (screen, (250, 0, 0), (width / 6, 20), (width / 6, height - 20), 4),
    COL2 : (screen, (250, 0, 0), (width / 2, 20), (width / 2, height - 20), 4),
    COL3 : (screen, (250, 0, 0), (width / 6 * 5, 20), (width / 6 * 5, height - 20), 4),
    LDIAG: (screen, (250, 70, 70), (50, 50), (350, 350), 4),
    RDIAG: (screen, (250, 70, 70), (350, 50), (50, 350), 4)
    }

initiating_window = pg.image.load("bg1.png") 
x_img = pg.image.load("cross.jpg") 
y_img = pg.image.load("nought.png") 

initiating_window = pg.transform.scale(initiating_window, (width, height + 100)) 
x_img = pg.transform.scale(x_img, (80, 80)) 
o_img = pg.transform.scale(y_img, (80, 80)) 

ICON = {CROSS : x_img, NOUGHT : o_img}

def game_initiating_window(): 
    
    screen.blit(initiating_window, (0, 0)) 
    
    pg.display.update() 
    time.sleep(3)                    
    screen.fill(white) 

    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7) 
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7) 

    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7) 
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7) 

def check_win(board):
    for line in CHECK:
        if board[line[0]] is None:
            continue
        if all(board[play] == board[line[0]] for play in line[1:]):
            pg.draw.line(*LINEARGS[line])
            return board[line[0]]
    return None

def check_draw(board):
    return all(play is not None for play in board)

def game_status(draw, winner, XO): 
    
    if winner is None: 
        message = XO.upper() + "'s Turn"
    else: 
        message = winner.upper() + " won !"
    if draw and winner is None: 
        message = "Game Draw !"

    font = pg.font.Font(None, 30) 
    
    text = font.render(message, 1, (255, 255, 255)) 

    screen.fill((0, 0, 0), (0, 400, 500, 100)) 
    text_rect = text.get_rect(center =(width / 2, 500-50)) 
    screen.blit(text, text_rect) 
    pg.display.update() 
    
    
def drawXO(pos, board, XO): 
    posx, posy = POSITIONS[pos]
    board[pos] = XO 
    
    screen.blit(ICON[XO], (posx, posy))
    pg.display.update() 
    return board, flip(XO)

def get_square(): 
    x, y = pg.mouse.get_pos() 
    for idx, limit in enumerate(LIMITS):
        xlim, ylim = limit
        if x < xlim and y < ylim:
            return idx
    return None

def user_click(board, XO, winner, draw):
    pos = get_square()
    if pos is not None and board[pos] is None: 
        board, XO = drawXO(pos, board, XO) 
        winner = check_win(board)
        draw = check_draw(board)
        game_status(draw, winner, XO)
    return board, XO, winner, draw
        
def flip(XO):
    return CROSS if XO == NOUGHT else NOUGHT

def available(board):
    return [idx for idx, item in enumerate(board) if item is None]

def win_move(board):
    for line in CHECK:
        p1, p2, p3 = line
        squares = [board[p1], board[p2], board[p3]]
        if squares.count(NOUGHT) == 2 and squares.count(None) == 1:
            if board[p1] is None:
                return p1
            if board[p2] is None:
                return p2
            return p3
    return None

def block_move(board):
    for line in CHECK:
        p1, p2, p3 = line
        squares = [board[p1], board[p2], board[p3]]
        if squares.count(CROSS) == 2 and squares.count(None) == 1:
            if board[p1] is None:
                return p1
            if board[p2] is None:
                return p2
            return p3
    return None

def comp_move(board, XO, winner, draw):
    pos = win_move(board)
    if pos is None:
        pos = block_move(board)
    if pos is None:
        pos = random.sample(available(board), 1)[0]
    board, XO = drawXO(pos, board, XO)
    winner = check_win(board)
    draw = check_win(board)
    game_status(draw, winner, XO)
    return board, XO, winner, draw

#driver code

XO = CROSS

winner = None

draw = False

board = [None] * 9

game_initiating_window() 
game_status(draw, winner, XO)

while(True): 
    for event in pg.event.get(): 
        if event.type == QUIT: 
            pg.quit() 
            sys.exit() 
        elif event.type is MOUSEBUTTONDOWN: 
            board, XO, winner, draw = user_click(board, XO, winner, draw) 
            if XO == NOUGHT and not winner and not draw:
                time.sleep(0.5)
                board, XO, winner, draw = comp_move(board, XO, winner, draw)
            if winner or draw:
                time.sleep(2)
                XO, winner, draw, board = CROSS, None, False, [None] * 9 
                game_initiating_window()
                game_status(draw, winner, XO)
    pg.display.update() 
    CLOCK.tick(fps) 
