import sys
import random
import numpy as np
import math
import pygame as pg
import copy

########################### CONSTANTS ##############################
# -1 = NOT_VALID_SPACE
ICON = pg.image.load("ChineseChekersAI-master\hello.png")
BACKGROUND = (128, 128, 128)
# 0 = EMPTY_CELL
EMPTY_CELL = (213, 192, 155)
# 1 = PLAYER 1
PLAYER1_GREEN =(0,255,0)
# 2 = PLAYER 2
PLAYER2_YELLOW = (255,255,0)
# 3 = PLAYER 3
PLAYER3_ORANGE = (255, 165,0)
# 4 = PLAYER 4

PLAYER4_RED = (255, 0, 0)
# 5 = PLAYER 5

PLAYER5_PURPLE = (128,0,128)
# 6 = PLAYER 6
PLAYER6_BLUE = (0, 0, 255)
# HIGHLIGHT
HIGHLIGHT = (0, 255, 255)
# costants of the board
MARGIN_1 = 20
MARGIN_2 = 20
RADIUS = 20
DIAMETER = 2 * RADIUS
SPACING_1 = 8
SPACING_2 = 1
WINDOW_WIDTH = (MARGIN_1 * 2) + (DIAMETER * 13) + (SPACING_1 * 12)
WINDOW_HEIGHT = (MARGIN_2 * 2) + (DIAMETER * 17) + (SPACING_2 * 16)
VISITED = 30
NOT_VISITED = 20
########################### CONSTANTS ##############################


def display():
    CHOSEN = 0
    pg.init()
    display_surface = pg.display.set_mode((656,736))
    pg.display.set_caption("FCAI CHECKERS : CHOOSE DIFFICULTY")
    pg.display.set_icon(ICON)
    pg.display.update()
    display_surface.fill((0,0,0))
    font = pg.font.Font('freesansbold.ttf', 32)
    text1 = font.render("Easy",True,(0,0,0),(255,255,255))
    text1Rect = text1.get_rect()
    text1Rect.center =  (320,175)
    text2 = font.render("Medium",True,(0,0,0),(255,255,255))
    text3 = font.render("Hard",True,(0,0,0),(255,255,255))

    text2Rect = text2.get_rect()
    text2Rect.center =  (320,375)

    text3Rect = text3.get_rect()
    text3Rect.center =  (320,575)
    depth = 0
    left_mouse_counter = 0
    while True:
        pg.draw.rect(display_surface,(255,255,255), pg.Rect((220,100),(200,150)) )
        pg.draw.rect(display_surface,(255,255,255), pg.Rect((220,300),(200,150)) )
        pg.draw.rect(display_surface,(255,255,255), pg.Rect((220,500),(200,150)) )
        display_surface.blit(text1, text1Rect)
        display_surface.blit(text2, text2Rect)
        display_surface.blit(text3, text3Rect)
        
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_mouse_counter += 1
                    if left_mouse_counter == 2:
                        left_mouse_counter = 0
                        x,y = pg.mouse.get_pos()
                        if x > 220 and x < 420 and y > 100 and y < 250:
                            depth = 1
                            return depth
                        elif x > 220 and x < 420 and y > 300 and y < 450:
                            depth = 3
                            return depth
                        elif x > 220 and x < 420 and y > 500 and y < 650:
                            depth = 5
                            return depth
        pg.display.update()
depth = display()

#fills board coordinates 0 means empty and can play in
# 1 - 6 means occupied by this player number
# -1 means immovable in
def build_board_matrix():

    board = np.zeros((17, 25))

    board[:][:] = -1

    board[0][12] = 1
    board[1][11] = 1
    board[1][13] = 1
    board[2][10] = 1
    board[2][12] = 1
    board[2][14] = 1
    board[3][9] = 1
    board[3][11] = 1
    board[3][13] = 1
    board[3][15] = 1

    board[4][18] = 2
    board[4][20] = 2
    board[4][22] = 2
    board[4][24] = 2
    board[5][19] = 2
    board[5][21] = 2
    board[5][23] = 2
    board[6][20] = 2
    board[6][22] = 2
    board[7][21] = 2

    board[9][21] = 3
    board[10][20] = 3
    board[10][22] = 3
    board[11][19] = 3
    board[11][21] = 3
    board[11][23] = 3
    board[12][18] = 3
    board[12][20] = 3
    board[12][22] = 3
    board[12][24] = 3

    board[13][9] = 4
    board[13][11] = 4
    board[13][13] = 4
    board[13][15] = 4
    board[14][10] = 4
    board[14][12] = 4
    board[14][14] = 4
    board[15][11] = 4
    board[15][13] = 4
    board[16][12] = 4

    board[9][21 - 18] = 5
    board[10][20 - 18] = 5
    board[10][22 - 18] = 5
    board[11][19 - 18] = 5
    board[11][21 - 18] = 5
    board[11][23 - 18] = 5
    board[12][18 - 18] = 5
    board[12][20 - 18] = 5
    board[12][22 - 18] = 5
    board[12][24 - 18] = 5

    board[4][18 - 18] = 6
    board[4][20 - 18] = 6
    board[4][22 - 18] = 6
    board[4][24 - 18] = 6
    board[5][19 - 18] = 6
    board[5][21 - 18] = 6
    board[5][23 - 18] = 6
    board[6][20 - 18] = 6
    board[6][22 - 18] = 6
    board[7][21 - 18] = 6

    board[4][8] = 0
    board[4][10] = 0
    board[4][12] = 0
    board[4][14] = 0
    board[4][16] = 0

    board[5][7] = 0
    board[5][9] = 0
    board[5][11] = 0
    board[5][13] = 0
    board[5][15] = 0
    board[5][17] = 0

    board[6][6] = 0
    board[6][8] = 0
    board[6][10] = 0
    board[6][12] = 0
    board[6][14] = 0
    board[6][16] = 0
    board[6][18] = 0

    board[7][5] = 0
    board[7][7] = 0
    board[7][9] = 0
    board[7][11] = 0
    board[7][13] = 0
    board[7][15] = 0
    board[7][17] = 0
    board[7][19] = 0

    board[7][5] = 0
    board[7][7] = 0
    board[7][9] = 0
    board[7][11] = 0
    board[7][13] = 0
    board[7][15] = 0
    board[7][17] = 0
    board[7][19] = 0

    board[8][4] = 0
    board[8][6] = 0
    board[8][8] = 0
    board[8][10] = 0
    board[8][12] = 0
    board[8][14] = 0
    board[8][16] = 0
    board[8][18] = 0
    board[8][20] = 0

    board[9][5] = 0
    board[9][7] = 0
    board[9][9] = 0
    board[9][11] = 0
    board[9][13] = 0
    board[9][15] = 0
    board[9][17] = 0
    board[9][19] = 0

    board[10][6] = 0
    board[10][8] = 0
    board[10][10] = 0
    board[10][12] = 0
    board[10][14] = 0
    board[10][16] = 0
    board[10][18] = 0

    board[11][7] = 0
    board[11][9] = 0
    board[11][11] = 0
    board[11][13] = 0
    board[11][15] = 0
    board[11][17] = 0

    board[12][8] = 0
    board[12][10] = 0
    board[12][12] = 0
    board[12][14] = 0
    board[12][16] = 0

    return board


def my_turn(player_turn , set_1, set_2, set_3 ,board , objective_1, objective_2, objective_3, player1_inv_home, player2_inv_home ,  player3_inv_home,display_surface):
    set_pieces, objectives_set, invalid_home = [], [], []
    left_button_counter = 0
    it = 0
    piece = 0
    if (player_turn == 1):
        set_pieces = set_1 
        objectives_set = objective_1
        invalid_home = player1_inv_home
    elif (player_turn == 2):
        set_pieces = set_2
        objectives_set = objective_2
        invalid_home = player2_inv_home
    elif (player_turn == 3):
        set_pieces = set_3
        objectives_set = objective_3
        invalid_home = player3_inv_home
    
    legal_moves = all_legal_moves(board, set_pieces, objectives_set, invalid_home)
    piece_chosen = False
    i = -1
    f = -1
    no_of_clicks_n = 0
    no_of_clicks_s = 0
    no_of_clicks_m = 0
    move = 0
    start_move = 0 
    piece = 0
    legal_for_piece = 0
    legal_for_piece_2 = 0
    turn_not_ended = 1
    mouse_choices = 0
    legal_for_piece = []
    legal_for_piece_2 = []
    x_y_pieces = []
    circle_x_y_pieces = []
    rectangles = []
    legal_moves_rectangle = []
    for i in range(len(set_pieces)):
        x_piece = set_pieces[i][0]
        y_piece = set_pieces[i][1]
        x_y_pieces.append([x_piece,y_piece])
        circle_x ,circle_y = find_circle(x_piece,y_piece) 
        circle_x_y_pieces.append([circle_x ,circle_y])
        my_rect = pg.Rect(circle_x - RADIUS, circle_y - RADIUS, DIAMETER, DIAMETER)
        rectangles.append(my_rect)
    
    
    
    
    pg.draw.ellipse(display_surface, (0,0,0), (circle_x_y_pieces[0][0] - RADIUS,circle_x_y_pieces[0][1]- RADIUS,
                                    DIAMETER, DIAMETER), 3)
    pg.display.update()
    while turn_not_ended:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_button_counter +=1
                if left_button_counter == 2:
                    pg.draw.ellipse(display_surface, BACKGROUND, (circle_x_y_pieces[0][0] - RADIUS,circle_x_y_pieces[0][1]- RADIUS,
                                    DIAMETER, DIAMETER), 3)
                    pg.display.update()
                    left_button_counter = 0
                    if mouse_choices != 0:
                        pg.draw.ellipse(display_surface, BACKGROUND, (circle_x_y_pieces[it][0] - RADIUS, circle_x_y_pieces[it][1] - RADIUS,DIAMETER,DIAMETER),3)
                        pg.display.update()
                        for [end_x,end_y] in legal_for_piece:
                            pg.draw.ellipse(display_surface, BACKGROUND, (end_x - RADIUS, end_y - RADIUS,
                                    DIAMETER, DIAMETER), 3)
                            pg.display.update()
                        legal_for_piece = []
                        legal_for_piece_2 = []
                    x,y = pg.mouse.get_pos()
                    for i in range(len(rectangles)):
                        if rectangles[i].collidepoint(x,y):
                            pg.draw.ellipse(display_surface, (0,0,0), (circle_x_y_pieces[i][0] - RADIUS, circle_x_y_pieces[i][1] - RADIUS,DIAMETER,DIAMETER),3)
                            it = i
                            pg.display.update()
                            mouse_choices += 1
                            piece = set_pieces[i]
                            start_move = [piece[0],piece[1]]
                            piece_chosen = 1
                            legal_moves_rectangle = []
                    
                    for j in legal_moves:
                            if j[0] == piece:
                                end_x, end_y = j[1][0], j[1][1]
                                legal_for_piece_2.append([end_x,end_y])
                                circle_end_x, circle_end_y = find_circle(end_x, end_y)
                                legal_for_piece.append([circle_end_x,circle_end_y])
                                pg.draw.ellipse(display_surface, (0,0,0), (circle_end_x - RADIUS, circle_end_y - RADIUS,
                                    DIAMETER, DIAMETER), 3)
                                pg.display.update()
                                my_rect = pg.Rect(circle_end_x - RADIUS, circle_end_y - RADIUS, DIAMETER, DIAMETER)
                                legal_moves_rectangle.append(my_rect)
                                
                    if mouse_choices > 0 and piece_chosen:
                        for i in range(len(legal_moves_rectangle)):
                            if legal_moves_rectangle[i].collidepoint(x,y):
                                move = [start_move,legal_for_piece_2[i]]
                                return move
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()       
# finds the best move by utilizing alphabeta pruning
def find_best_move(board, legal_moves, objectives_set, player_turn, set_pieces, set_1, set_2, set_3,
                   set_4, set_5, set_6):
    obj_left = [i for i in objectives_set + set_pieces if i not in objectives_set or i not in set_pieces]
    if len(obj_left) == 2:
        for move in legal_moves:
            start_move = move[0]
            end_move = move[1]
            if start_move == obj_left[1] and end_move == obj_left[0]:
                return move
    try:
        

        if player_turn == 1:
            pass
        elif player_turn == 3:
            pass
        elif player_turn == 5:
            
            score, best_move = alphabeta(board, depth, player_turn, player_turn, set_1, set_2,
                                         set_3, set_4, set_5, set_6, -1000, 1000)
        elif player_turn == 2:
            pass
        elif player_turn == 4:
            
            score, best_move = alphabeta(board, depth, player_turn, player_turn, set_1, set_2,
                                      set_3, set_4, set_5, set_6, -1000, 1000)
        elif player_turn == 6:
            
            score, best_move = alphabeta(board, depth, player_turn, player_turn, set_1, set_2,
                                         set_3, set_4, set_5, set_6, -1000, 1000)

    except Exception:
        return

    return best_move


def isWin(set_pieces, objectives_set):

    game_end = True

    for piece in set_pieces:
        if piece not in objectives_set:
            game_end = False

    return game_end



#builds starting piece positions in the board "Board pieces initialization"
def build_sets():

    set_1 = [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]]
    set_2 = [[4, 18], [4, 20], [4, 22], [4, 24], [5, 19], [5, 21], [5, 23], [6, 20], [6, 22], [7, 21]]
    set_3 = [[9, 21], [10, 20], [10, 22], [11, 19], [11, 21], [11, 23], [12, 18], [12, 20], [12, 22], [12, 24]]
    set_4 = [[13, 9], [13, 11], [13, 13], [13, 15], [14, 10], [14, 12], [14, 14], [15, 11], [15, 13], [16, 12]]
    set_5 = [[9, 3], [10, 2], [10, 4], [11, 1], [11, 3], [11, 5], [12, 0], [12, 2], [12, 4], [12, 6]]
    set_6 = [[4, 0], [4, 2], [4, 4], [4, 6], [5, 1], [5, 3], [5, 5], [6, 2], [6, 4], [7, 3]]

    return set_1, set_2, set_3, set_4, set_5, set_6

#builds objective sets for each player during game start "Goal pieces initialization"
def build_objectives_sets():
    objective_1 = [[16, 12], [15, 11], [15, 13], [14, 10], [14, 14], [14, 12], [13, 9], [13, 15], [13, 13], [13, 11]]
    objective_2 = [[12, 0], [11, 1], [12, 2], [10, 2], [12, 4], [11, 3], [9, 3], [12, 6], [11, 5], [10, 4]]
    objective_3 = [[4, 0], [4, 2], [5, 1], [4, 4], [6, 2], [5, 3], [4, 6], [7, 3], [6, 4], [5, 5]]
    objective_4 = [[0, 12], [1, 13], [1, 11], [2, 14], [2, 10], [2, 12], [3, 15], [3, 9], [3, 11], [3, 13]]
    objective_5 = [[4, 24], [5, 23], [4, 22], [6, 22], [4, 20], [5, 21], [7, 21], [4, 18],  [5, 19], [6, 20]]
    objective_6 = [[12, 24], [12, 22], [11, 23], [12, 20], [10, 22], [11, 21], [12, 18], [9, 21], [10, 20], [11, 19]]

    return objective_1, objective_2, objective_3, objective_4, objective_5, objective_6

#builds homes that players can't enter "Forbidden zones initialization"
def get_invalid_homes(set_1, set_2, set_3, set_4, set_5, set_6, objective_1, objective_2, objective_3, objective_4, objective_5, objective_6):


    player1_invalid_house = set_2 + objective_2 + set_6 + objective_6
    player2_invalid_house = set_1 + objective_1 + set_6 + objective_6
    player3_invalid_house = set_2 + objective_2 + set_4 + objective_4
    player4_invalid_house = set_5 + objective_5 + set_6 + objective_6
    player5_invalid_house = set_4 + objective_4 + set_3 + objective_3
    player6_invalid_house = set_4 + objective_4 + set_5 + objective_5

    return player1_invalid_house, player2_invalid_house, player3_invalid_house, player4_invalid_house, player5_invalid_house, player6_invalid_house

#during each turn assign the set that has the move to play
def bind_set(player_turn, set_1, set_2, set_3, set_4, set_5, set_6):

    set_player = set_1

    if player_turn == 1:
        set_player = set_1
    if player_turn == 2:
        set_player = set_2
    if player_turn == 3:
        set_player = set_3
    if player_turn == 4:
        set_player = set_4
    if player_turn == 5:
        set_player = set_5
    if player_turn == 6:
        set_player = set_6

    return set_player

#during each turn assign the objective of the playing pieces
def bind_objectives_set(player_turn, objective_1, objective_2, objective_3, objective_4, objective_5, objective_6):

    objectives_set = objective_1

    if player_turn == 1:
        objectives_set = objective_1
    if player_turn == 2:
        objectives_set = objective_2
    if player_turn == 3:
        objectives_set = objective_3
    if player_turn == 4:
        objectives_set = objective_4
    if player_turn == 5:
        objectives_set = objective_5
    if player_turn == 6:
        objectives_set = objective_6

    return objectives_set

# during each turn assign the forbidden areas of the player
def bind_invalid_homes_array(player_turn, player1_invalid_home, player2_invalid_home, player3_invalid_home, player4_invalid_home, player5_invalid_home, player6_invalid_home):

    invalid_homes_array = player1_invalid_home

    if player_turn == 1:
        invalid_homes_array = player1_invalid_home
    if player_turn == 2:
        invalid_homes_array = player2_invalid_home
    if player_turn == 3:
        invalid_homes_array = player3_invalid_home
    if player_turn == 4:
        invalid_homes_array = player4_invalid_home
    if player_turn == 5:
        invalid_homes_array = player5_invalid_home
    if player_turn == 6:
        invalid_homes_array = player6_invalid_home

    return invalid_homes_array

#after each turn concludes, update the player set to match current state
def update_player_set(set_pieces, player_turn, set_1, set_2, set_3, set_4, set_5, set_6):

    if player_turn == 1:
        set_1 = set_pieces
    if player_turn == 2:
        set_2 = set_pieces
    if player_turn == 3:
        set_3 = set_pieces
    if player_turn == 4:
        set_4 = set_pieces
    if player_turn == 5:
        set_5 = set_pieces
    if player_turn == 6:
        set_6 = set_pieces

    return set_1, set_2, set_3, set_4, set_5, set_6

# brute forces all legal moves for the players turn 
def all_legal_moves(board, set_pieces, objectives_set, invalid_homes_array):


    valid_moves = []

    for piece in set_pieces:

        #if piece not in objectives_set:
        color_board = np.full(board.shape, NOT_VISITED)
        valid_moves = check_moves(board, color_board, piece, 0, piece, valid_moves)
    valid_moves = moves_in_house(valid_moves, objectives_set)
    valid_moves = dont_stop_in_house(valid_moves, invalid_homes_array)

    return valid_moves


def check_moves(board, color_board, start, depth, origin, v_moves):

    [x_v0, y_v0] = start
    color_board[x_v0][y_v0] = VISITED

    neighbors_list = find_neighbors(start)

    for x_v1, y_v1 in neighbors_list:

        # append all neighbors that are not visited in current board to valid moves
        if depth == 0 and board[x_v1][y_v1] == 0:
            v_moves.append([start, [x_v1, y_v1]])

        if depth == 0 and board[x_v1][y_v1] > 0:
            x_v2, y_v2 = jumps(start, x_v1, y_v1)
            if board[x_v2][y_v2] == 0:
                v_moves.append([start, [x_v2, y_v2]])
                v_moves = check_moves(board, color_board, [x_v2, y_v2], depth + 1, origin, v_moves)

        if depth > 0 and board[x_v1][y_v1] > 0:
            x_v2, y_v2 = jumps(start, x_v1, y_v1)
            if board[x_v2][y_v2] == 0 and color_board[x_v2][y_v2] == NOT_VISITED:
                v_moves.append([origin, [x_v2, y_v2]])
                v_moves = check_moves(board, color_board, [x_v2, y_v2], depth + 1, origin, v_moves)

    return v_moves

# find all directly neighboring nodes
def find_neighbors(node):

    [x, y] = node

    neighbors_list = []

    nb = [x, y + 2]
    if 0 <= nb[1] <= 24:
        neighbors_list.append([x, y + 2])

    nb = [x, y - 2]
    if 0 <= nb[1] <= 24:
        neighbors_list.append([x, y - 2])

    nb = [x + 1, y + 1]
    if 0 <= nb[0] <= 16 and 0 <= nb[1] <= 24 :
        neighbors_list.append([x + 1, y + 1])

    nb = [x + 1, y - 1]
    if 0 <= nb[0] <= 16 and 0 <= nb[1] <= 24:
        neighbors_list.append([x + 1, y - 1])

    nb = [x - 1, y + 1]
    if 0 <= nb[0] <= 16 and 0 <= nb[1] <= 24:
        neighbors_list.append([x - 1, y + 1])

    nb = [x - 1, y - 1]
    if 0 <= nb[0] <= 16 and 0 <= nb[1] <= 24:
        neighbors_list.append([x - 1, y - 1])

    return neighbors_list

# find if there is a jump over a node
def jumps(start, x_v1, y_v1):

    [start_x, start_y] = start

    x_v2 = x_v1 + (x_v1 - start_x)
    y_v2 = y_v1 + (y_v1 - start_y)

    if 0 <= x_v2 <= 16 and 0 <= y_v2 <= 24:
        return x_v2, y_v2
    else:
        return 0, 0

# find all valid moves that are inside the objective home "Unknown formulas"
def moves_in_house(valid_moves, objectives_set):

    moves_to_remove = []

    for valid_move in valid_moves:

        start_move = valid_move[0]
        end_move = valid_move[1]

        if start_move in objectives_set:

            square_start_y = (start_move[1] * 14.43) / 25
            square_end_y = (end_move[1] * 14.43) / 25
            central_pos = (12 * 14.43) / 25

            start_diag = math.sqrt(((8 - start_move[0]) ** 2) + ((central_pos - square_start_y) ** 2))
            end_diag = math.sqrt(((8 - end_move[0]) ** 2) + ((central_pos - square_end_y) ** 2))

            if start_diag > end_diag:
                moves_to_remove.append(valid_move)

    new_valid_moves = [i for i in valid_moves + moves_to_remove if i not in valid_moves or i not in moves_to_remove]

    return new_valid_moves

# don't move in invalid homes
def dont_stop_in_house(valid_moves, invalid_homes_array):

    moves_to_remove = []

    for valid_move in valid_moves:

        end_move = valid_move[1]

        if end_move in invalid_homes_array:
            moves_to_remove.append(valid_move)

    new_valid_moves = [i for i in valid_moves + moves_to_remove if i not in valid_moves or i not in moves_to_remove]

    return new_valid_moves

# after figuring out the best move, apply it on the board
def do_move(board, best_move, set_pieces):

    [start_x, start_y] = best_move[0]
    [end_x, end_y] = best_move[1]

    piece = board[start_x][start_y]
    board[start_x][start_y] = 0
    board[end_x][end_y] = piece

    
    piece_to_remove = [[start_x, start_y]]
    new_set_pieces = [i for i in set_pieces + piece_to_remove if i not in set_pieces or i not in piece_to_remove]

    # set_pieces.remove([start_x, start_y])
    new_set_pieces.append([end_x, end_y])

    return board, new_set_pieces



# initialize the window
def initialize_board():
    pg.init()
    display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption('FCAI CHECKERS')
    pg.display.set_icon(ICON)
    return display_surface


def draw_board(board, display_surface):
    #fills the whole board with the background color
    display_surface.fill(BACKGROUND)

    # the initial y_posinate
    y_pos = MARGIN_2 + RADIUS

    #destination of the target circles "indicates the goal for each circle"
    destinations = [[2, 0], [0, 8], [2, 24], [14, 24], [16, 16], [14, 0]]

    for row in range(0, 17):
        #long is used in drawing even rows which can contain "empty cells 'filled with a color' , invalid cells 'filled with background color', player cells filled with marble color"
        x_pos_long = MARGIN_1 + RADIUS
        #used in odd rows which are all invalid cells
        x_pos_short = int(MARGIN_1 + DIAMETER + (SPACING_1 / 2))

        for circle_in_a_row in range(0, 13):
            if row % 2 == 0:

                board_value = board[row][circle_in_a_row * 2]
                if [row, circle_in_a_row * 2] in destinations:
                    color_destination(display_surface, x_pos_long, y_pos, row, circle_in_a_row, destinations)
                else:
                    color_circle(board_value, display_surface, x_pos_long, y_pos)

                x_pos_long = x_pos_long + DIAMETER + SPACING_1

            elif row % 2 != 0 and circle_in_a_row != 12:
    
                board_value = board[row][circle_in_a_row * 2 + 1]
                color_circle(board_value, display_surface, x_pos_short, y_pos)

                x_pos_short = x_pos_short + DIAMETER + SPACING_1

        y_pos = y_pos + DIAMETER + SPACING_2

def color_circle(board_value, display_surface, x_pos, y_pos):

    if board_value == -1:
        pg.draw.circle(display_surface, BACKGROUND, (x_pos, y_pos), RADIUS, 0)
    if board_value == 0:
        pg.draw.circle(display_surface, EMPTY_CELL, (x_pos, y_pos), RADIUS, 0)
    if board_value == 1:
        pg.draw.circle(display_surface, PLAYER1_GREEN, (x_pos, y_pos), RADIUS, 0)
    if board_value == 2:
        pg.draw.circle(display_surface, PLAYER2_YELLOW, (x_pos, y_pos), RADIUS, 0)
    if board_value == 3:
        pg.draw.circle(display_surface, PLAYER3_ORANGE, (x_pos, y_pos), RADIUS, 0)
    if board_value == 4:
        pg.draw.circle(display_surface, PLAYER4_RED, (x_pos, y_pos), RADIUS, 0)
    if board_value == 5:
        pg.draw.circle(display_surface, PLAYER5_PURPLE, (x_pos, y_pos), RADIUS, 0)
    if board_value == 6:
        pg.draw.circle(display_surface, PLAYER6_BLUE, (x_pos, y_pos), RADIUS, 0)

def color_destination(display_surface, x_pos_long, y_pos, row, circle_in_a_row, destinations):

    if [row, circle_in_a_row * 2] == destinations[0]:
        pg.draw.circle(display_surface, PLAYER3_ORANGE, (x_pos_long, y_pos), RADIUS, 0)
    if [row, circle_in_a_row * 2] == destinations[1]:
        pg.draw.circle(display_surface, PLAYER4_RED, (x_pos_long, y_pos), RADIUS, 0)
    if [row, circle_in_a_row * 2] == destinations[2]:
        pg.draw.circle(display_surface, PLAYER5_PURPLE, (x_pos_long, y_pos), RADIUS, 0)
    if [row, circle_in_a_row * 2] == destinations[3]:
        pg.draw.circle(display_surface, PLAYER6_BLUE, (x_pos_long, y_pos), RADIUS, 0)
    if [row, circle_in_a_row * 2] == destinations[4]:
        pg.draw.circle(display_surface, PLAYER1_GREEN, (x_pos_long, y_pos), RADIUS, 0)
    if [row, circle_in_a_row * 2] == destinations[5]:
        pg.draw.circle(display_surface, PLAYER2_YELLOW, (x_pos_long, y_pos), RADIUS, 0)

def highlight_best_move(best_move, display_surface):

    [start_x, start_y] = best_move[0]
    [end_x, end_y] = best_move[1]

# find the coordinates of the start circle in the board 
    circle_start_x, circle_start_y = find_circle(start_x, start_y)
    pg.draw.ellipse(display_surface, HIGHLIGHT, (circle_start_x - RADIUS, circle_start_y - RADIUS,
                                                 DIAMETER, DIAMETER), 5)

# find the coordinates of the end circle in the board 
    circle_end_x, circle_end_y = find_circle(end_x, end_y)
    pg.draw.ellipse(display_surface, HIGHLIGHT, (circle_end_x - RADIUS, circle_end_y - RADIUS,
                                                 DIAMETER, DIAMETER), 5)

# find the coordinates of the circle in the board 
def find_circle(x, y):

    if x % 2 == 0:
        circle_x = int(MARGIN_1 + RADIUS + (DIAMETER + SPACING_1) * (y / 2))
    else:
        circle_x = int(MARGIN_1 + DIAMETER + (SPACING_1 / 2) + (DIAMETER + SPACING_1) * ((y - 1)
                                                                                                                / 2))
    circle_y = MARGIN_2 + RADIUS + (DIAMETER + SPACING_2) * x

    return circle_x, circle_y

set_1, set_2, set_3, set_4, set_5, set_6 = build_sets()
objective_1, objective_2, objective_3, objective_4, objective_5, objective_6 = build_objectives_sets()
player1_inv_homes, player2_inv_homes, player3_inv_homes, player4_inv_homes, player5_inv_homes, player6_inv_homes = \
    get_invalid_homes(set_1, set_2, set_3, set_4, set_5, set_6, objective_1,
                             objective_2, objective_3, objective_4, objective_5, objective_6)


def alphabeta(board, depth, player, first_player, set_1, set_2, set_3, set_4, set_5,
              set_6, alpha, beta):

    # create a copied board
    board_copy = board[:][:]


    if depth == 0:
        board_score = calculate_board_score(first_player, set_1, set_2, set_3, set_4,
                                            set_5, set_6)
        # there is no moves because you are in the current state and the function calculate only the score 
        return board_score, None


    # get the set of the player's turn 
    set_pieces = bind_set(player, set_1, set_2, set_3, set_4, set_5, set_6)

    # get the objectives_set of the player's turn
    objectives_set = bind_objectives_set(player, objective_1, objective_2, objective_3, objective_4,
                             objective_5, objective_6)

    # get the invalid_homes_array of the player's turn
    invalid_homes = bind_invalid_homes_array(player, player1_inv_homes, player2_inv_homes, player3_inv_homes,
                                             player4_inv_homes, player5_inv_homes, player6_inv_homes)

    # get all legal moves of the player's set
    valid_moves = all_legal_moves(board_copy, set_pieces, objectives_set, invalid_homes)

    scores = []
    moves = []


    if player == first_player:

        for move in valid_moves:
            
            # Create a new copy of my board to apply the best move and store it to use it in the next deapth 
            board_copy_again = copy.copy(board_copy)
            
            # after figuring out the best move, apply it on the board
            new_board, new_set_pieces = do_move(board_copy_again, move, set_pieces)

            # Update players sets 
            set_1, set_2, set_3, set_4, set_5, set_6 = \
                update_player_set(new_set_pieces, player, set_1, set_2, set_3, set_4,
                                  set_5, set_6)

            # change the turn of the player by the next player
            next_player = player + 1
            
            # reach to the last player "6"
            if next_player == 7:
                next_player = 1


            score, something = alphabeta(new_board, depth - 1, next_player, first_player, set_1, set_2,
                                         set_3, set_4, set_5, set_6, alpha, beta)
 
            scores.append(score)
            moves.append(move)
            

            alpha = max(score, alpha)
            if beta <= alpha:
                break

        # when stuck happen
        if len(scores) == 0:
            return
        
        max_score_index = scores.index(max(scores))
        best_move = moves[max_score_index]
        return scores[max_score_index], best_move

    else:

        for move in valid_moves:
            board_copy_again = copy.copy(board_copy)
            new_board, new_set_pieces = do_move(board_copy_again, move, set_pieces)

            set_1, set_2, set_3, set_4, set_5, set_6 = \
                update_player_set(new_set_pieces, player, set_1, set_2, set_3, set_4,
                                  set_5, set_6)

            next_player = player + 1
            if next_player == 7:
                next_player = 1

            score, something = alphabeta(new_board, depth - 1, next_player, first_player, set_1, set_2,
                                         set_3, set_4, set_5, set_6, alpha, beta)

            scores.append(score)
            moves.append(move)
            

            beta = min(score, beta)
            if beta <= alpha:
                break

        if len(scores) == 0:
            return
        min_score_index = scores.index(min(scores))
        worst_opponent_move = moves[min_score_index]

        return scores[min_score_index], worst_opponent_move

def calculate_board_score(player_turn, p1_pieces, p2_pieces, p3_pieces, p4_pieces, p5_pieces, p6_pieces):

    p1_avg_distance = find_avg_distance(p1_pieces, objective_1, 16, 12)
    p2_avg_distance = find_avg_distance(p2_pieces, objective_2, 12, 0)
    p3_avg_distance = find_avg_distance(p3_pieces, objective_3, 4, 0)
    p4_avg_distance = find_avg_distance(p4_pieces, objective_4, 0, 12)
    p5_avg_distance = find_avg_distance(p5_pieces, objective_5, 4, 24)
    p6_avg_distance = find_avg_distance(p6_pieces, objective_6, 12, 24)
    score = calculate_score(player_turn, p1_avg_distance, p2_avg_distance, p3_avg_distance, p4_avg_distance,
                            p5_avg_distance, p6_avg_distance)

    return score

def find_avg_distance(p_pieces, p_obj, p_x, p_y):

    total_distance = 0
    obj_x = p_x
    obj_y = p_y
    for obj_piece in p_obj:
        if obj_piece not in p_pieces:
            [obj_x, obj_y] = obj_piece
            break

    for piece in p_pieces:

        [x, y] = piece

        square_y = (y * 14.43) / 25
        square_obj_y = (obj_y * 14.43) / 25

        distance_diag = math.sqrt(((obj_x - x) ** 2) + ((square_obj_y - square_y) ** 2))

        total_distance = total_distance + distance_diag

    avg_distance = total_distance / 10

    return avg_distance

def calculate_score(player_turn, p1_avg_distance, p2_avg_distance, p3_avg_distance, p4_avg_distance, p5_avg_distance,
                    p6_avg_distance):
    score = 0

    if player_turn == 1:
        # print("-- loop player 1")
        pturn_avg_distance = p1_avg_distance
        score = ((p2_avg_distance - pturn_avg_distance) +
                 (p3_avg_distance - pturn_avg_distance) +
                 (p4_avg_distance - pturn_avg_distance) +
                 (p5_avg_distance - pturn_avg_distance) +
                 (p6_avg_distance - pturn_avg_distance)) / 5
    elif player_turn == 2:
        # print("-- loop player 2")
        pturn_avg_distance = p2_avg_distance
        score = ((p1_avg_distance - pturn_avg_distance) +
                 (p3_avg_distance - pturn_avg_distance) +
                 (p4_avg_distance - pturn_avg_distance) +
                 (p5_avg_distance - pturn_avg_distance) +
                 (p6_avg_distance - pturn_avg_distance)) / 5
    elif player_turn == 3:
        pturn_avg_distance = p3_avg_distance
        score = ((p2_avg_distance - pturn_avg_distance) +
                 (p1_avg_distance - pturn_avg_distance) +
                 (p4_avg_distance - pturn_avg_distance) +
                 (p5_avg_distance - pturn_avg_distance) +
                 (p6_avg_distance - pturn_avg_distance)) / 5
    elif player_turn == 4:
        pturn_avg_distance = p4_avg_distance
        score = ((p2_avg_distance - pturn_avg_distance) +
                 (p3_avg_distance - pturn_avg_distance) +
                 (p1_avg_distance - pturn_avg_distance) +
                 (p5_avg_distance - pturn_avg_distance) +
                 (p6_avg_distance - pturn_avg_distance)) / 5
    elif player_turn == 5:
        pturn_avg_distance = p5_avg_distance
        score = ((p2_avg_distance - pturn_avg_distance) +
                 (p3_avg_distance - pturn_avg_distance) +
                 (p4_avg_distance - pturn_avg_distance) +
                 (p1_avg_distance - pturn_avg_distance) +
                 (p6_avg_distance - pturn_avg_distance)) / 5
    elif player_turn == 6:
        pturn_avg_distance = p6_avg_distance
        score = ((p2_avg_distance - pturn_avg_distance) +
                 (p3_avg_distance - pturn_avg_distance) +
                 (p4_avg_distance - pturn_avg_distance) +
                 (p5_avg_distance - pturn_avg_distance) +
                 (p1_avg_distance - pturn_avg_distance)) / 5

    return score

def main():
    p1_win = 0
    p2_win = 0
    p3_win = 0
    p4_win = 0
    p5_win = 0
    p6_win = 0
    
    stuck_counter = 0
    restart_time = 5000 
    move_time = 100

    # build a 2D array 
    board = build_board_matrix()
    
    # Initialize the obj, set and invalid_homes Lists for each player 
    set_1, set_2, set_3, set_4, set_5, set_6 = build_sets()
    objective_1, objective_2, objective_3, objective_4, objective_5, objective_6 = build_objectives_sets()
    player1_invalid_home, player2_invalid_home, player3_invalid_home, player4_invalid_home, player5_invalid_home, \
        player6_invalid_home = get_invalid_homes(set_1, set_2, set_3, set_4,
                                                        set_5, set_6, objective_1, objective_2,
                                                        objective_3, objective_4, objective_5, objective_6)

    # Initialize the board
    display_surface = initialize_board()

    # player decision
    player_turn = 0

    # game start
    game_over = False
    first_turn = True
    first_round = True
    save_first_p = 100

    # events from pygame 
    next_move = pg.USEREVENT + 1
    restart_game = pg.USEREVENT + 2
    # Initialize the event as next move
    event = pg.event.Event(next_move)
    pg.event.post(event)


    # infinite loop used to run the game 
    while True:
        # Used to reiterate and draw the game surface each frame 
        draw_board(board, display_surface)

        # gets all events that happened in the game window 
        for event in pg.event.get():

            # exit button 
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            # when the game is stuck , then restart the game 
            if event.type == restart_game:
                
                pg.time.wait(restart_time)

                board = build_board_matrix()
                set_1, set_2, set_3, set_4, set_5, set_6 = build_sets()
                objective_1, objective_2, objective_3, objective_4, objective_5, objective_6 = build_objectives_sets()
                player1_invalid_home, player2_invalid_home, player3_invalid_home, player4_invalid_home, \
                    player5_invalid_home, player6_invalid_home = get_invalid_homes(
                        set_1, set_2, set_3, set_4, set_5, set_6, objective_1,
                        objective_2, objective_3, objective_4, objective_5, objective_6)
                display_surface = initialize_board()

                # player decision
                player_turn = 0

                draw_board(board, display_surface)
                pg.display.update()

                # game restart
                game_over = False
                first_turn = True
                first_round = True
                save_first_p = 100

                event = pg.event.Event(next_move)
                pg.event.post(event)

                break

            if event.type == next_move and not game_over:

                pg.time.wait(move_time)

                # change player turn
                player_turn = player_turn + 1
                if player_turn == 7:
                    player_turn = 1

                # randomize first move
                if player_turn == save_first_p:
                    first_round = False
                if first_turn:
                    save_first_p = player_turn
                    first_turn = False


                # consider the pieces of the player of this turn
                set_pieces = bind_set(player_turn, set_1, set_2, set_3, set_4,
                                        set_5, set_6)

                # identify homes of the player of this turn
                invalid_homes_array = bind_invalid_homes_array(player_turn, player1_invalid_home,
                                                             player2_invalid_home, player3_invalid_home,
                                                             player4_invalid_home, player5_invalid_home,
                                                             player6_invalid_home)

                # assign objective set of positions
                objectives_set = bind_objectives_set(player_turn, objective_1, objective_2, objective_3, objective_4,
                                         objective_5, objective_6)

                legal_moves = all_legal_moves(board, set_pieces, objectives_set, invalid_homes_array)

                # choose the best move
                if first_round:
                    if player_turn > 3:
                        best_move_index = random.randint(0, len(legal_moves) - 1)
                        best_move = legal_moves[best_move_index]
                    else:
                        best_move = my_turn(player_turn , set_1, set_2, set_3 ,board , objective_1, objective_2, objective_3, player1_invalid_home, player2_invalid_home ,  player3_invalid_home,display_surface)
                    
                else:
                    if player_turn > 3:
                        best_move = find_best_move(board, legal_moves, objectives_set, player_turn, set_pieces,
                                               set_1, set_2, set_3, set_4, set_5,
                                               set_6)
                    else:
                        best_move = my_turn(player_turn , set_1, set_2, set_3 ,board , objective_1, objective_2, objective_3, player1_invalid_home, player2_invalid_home ,  player3_invalid_home,display_surface)
                    

                if best_move is None:

                    game_over = True
                    stuck_counter = stuck_counter + 1
                    print('Game stuck counter:', stuck_counter)
                    

                    # declre the eent 
                    event = pg.event.Event(restart_game)
                    
                    # put the enent in the events list 
                    pg.event.post(event)

                    break

                # highlight the move chosen
                highlight_best_move(best_move, display_surface)
                pg.display.update()

                # do the best move
                board, set_pieces = do_move(board, best_move, set_pieces)

                # update set
                set_1, set_2, set_3, set_4, set_5, set_6 = \
                    update_player_set(set_pieces, player_turn, set_1, set_2, set_3, set_4,
                                      set_5, set_6)

                # check if the player has won
                game_over = isWin(set_pieces, objectives_set)

                if game_over:

                    if player_turn == 1:
                        p1_win = p1_win + 1
                    if player_turn == 2:
                        p2_win = p2_win + 1
                    if player_turn == 3:
                        p3_win = p3_win + 1
                    if player_turn == 4:
                        p4_win = p4_win + 1
                    if player_turn == 5:
                        p5_win = p5_win + 1
                    if player_turn == 6:
                        p6_win = p6_win + 1

                    print('Player 1 wins:', p1_win)
                    print('Player 2 wins:', p2_win)
                    print('Player 3 wins:', p3_win)
                    print('Player 4 wins:', p4_win)
                    print('Player 5 wins:', p5_win)
                    print('Player 6 wins:', p6_win)

                    event = pg.event.Event(restart_game)
                    pg.event.post(event)

                else:

                    event = pg.event.Event(next_move)
                    pg.event.post(event)



main()
