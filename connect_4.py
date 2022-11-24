''' Python game Connect 4 '''
import sys
import math
import pygame
import numpy as np
import constants as const

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0


def get_next_open_row(board, col):
    for a_row in range(ROW_COUNT):
        if board[a_row][col] == 0:
            return a_row


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for a_col in range(COLUMN_COUNT-3):
        for a_row in range(ROW_COUNT):
            if (board[a_row][a_col] == piece
                and board[a_row][a_col+1] == piece
                and board[a_row][a_col+2] == piece
                    and board[a_row][a_col+3] == piece):
                return True

    # Check vertical locations for win
    for a_col in range(COLUMN_COUNT):
        for a_row in range(ROW_COUNT-3):
            if (board[a_row][a_col] == piece
                and board[a_row+1][a_col] == piece
                and board[a_row+2][a_col] == piece
                    and board[a_row+3][a_col] == piece):
                return True

    # Check positively sloped diaganols
    for a_col in range(COLUMN_COUNT-3):
        for a_row in range(ROW_COUNT-3):
            if (board[a_row][a_col] == piece
                and board[a_row+1][a_col+1] == piece
                and board[a_row+2][a_col+2] == piece
                    and board[a_row+3][a_col+3] == piece):
                return True

    # Check negatively sloped diaganols
    for a_col in range(COLUMN_COUNT-3):
        for a_row in range(3, ROW_COUNT):
            if (board[a_row][a_col] == piece
                and board[a_row-1][a_col+1] == piece
                and board[a_row-2][a_col+2] == piece
                    and board[a_row-3][a_col+3] == piece):
                return True


def draw_board(board, screen, radius_of_slot, height):
    ''' display the board to put pieces '''
    for a_col in range(COLUMN_COUNT):
        for a_row in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (a_col*const.SQUARESIZE, a_row *
                             const.SQUARESIZE+const.SQUARESIZE, const.SQUARESIZE, const.SQUARESIZE))
            pygame.draw.circle(screen, BLACK,
                               (int(a_col*const.SQUARESIZE+const.SQUARESIZE/2),
                                int(a_row*const.SQUARESIZE+const.SQUARESIZE+const.SQUARESIZE/2)),
                               radius_of_slot)

    for a_col in range(COLUMN_COUNT):
        for a_row in range(ROW_COUNT):
            if board[a_row][a_col] == 1:
                pygame.draw.circle(screen, RED,
                                   (int(a_col*const.SQUARESIZE+const.SQUARESIZE/2),
                                    height-int(a_row*const.SQUARESIZE+const.SQUARESIZE/2)),
                                   radius_of_slot)
            elif board[a_row][a_col] == 2:
                pygame.draw.circle(screen, YELLOW,
                                   (int(a_col*const.SQUARESIZE+const.SQUARESIZE/2),
                                    height-int(a_row*const.SQUARESIZE+const.SQUARESIZE/2)),
                                   radius_of_slot)
    pygame.display.update()


def initiate():
    ''' Start game '''
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    pygame.init()


    width = COLUMN_COUNT * const.SQUARESIZE
    height = (ROW_COUNT+1) * const.SQUARESIZE

    size = (width, height)

    radius_of_slot = int(const.SQUARESIZE/2 - 5)

    screen = pygame.display.set_mode(size)
    draw_board(board, screen, radius_of_slot, height)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, const.SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(
                        screen, RED, (posx, int(const.SQUARESIZE/2)), radius_of_slot)
                else:
                    pygame.draw.circle(
                        screen, YELLOW, (posx, int(const.SQUARESIZE/2)), radius_of_slot)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, const.SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx/const.SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        board[row][col] = 1 # drop_piece

                        if winning_move(board, 1):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (25, 10))
                            game_over = True

                # # Ask for Player 2 Input
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx/const.SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        board[row][col] = 2 # drop_piece

                        if winning_move(board, 2):
                            label = myfont.render("Player 2 wins!!", 1, YELLOW)
                            screen.blit(label, (25, 10))
                            game_over = True

                print_board(board)
                draw_board(board, screen, radius_of_slot, height)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)

initiate() # will start the game
