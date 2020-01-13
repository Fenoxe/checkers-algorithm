import pygame
import GameLogic as GL
from Containers import PendingMove, Vector2
import Minimax as ALG
import time

DEPTH = 10

# initialize
pygame.init()

# load assets
checker_icon = pygame.image.load("checker_icon.png")
board_bg = pygame.image.load("checkers_bg.png")
red_checker = pygame.image.load("checker_red.png")
black_checker = pygame.image.load("checker_black.png")
red_checker_king = pygame.image.load("checker_red_king.png")
black_checker_king = pygame.image.load("checker_black_king.png")

# configure settings
pygame.display.set_icon(checker_icon)
pygame.display.set_caption("checkers AI")
board_screen = pygame.display.set_mode((1000,1000))

# initialize board
board = GL.create_board()

# helper functions
checker_locs = [12 + 125*i for i in range(8)]

def render():
    board_screen.blit(board_bg, (0,0))
    for y in range(8):
        for x in range(8):
            tile = GL.get_piece(board, Vector2(x,y))
            if tile == GL.EMPTY:
                continue
            elif tile == GL.RED:
                board_screen.blit(red_checker, (checker_locs[x], checker_locs[y]))
            elif tile == GL.BLACK:
                board_screen.blit(black_checker, (checker_locs[x], checker_locs[y]))
            elif tile == GL.RED * GL.KING:
                board_screen.blit(red_checker_king, (checker_locs[x], checker_locs[y]))
            elif tile == GL.BLACK * GL.KING:
                board_screen.blit(black_checker_king, (checker_locs[x], checker_locs[y]))

    pygame.display.flip()

def get_grid_tile(px_x, px_y):
    return Vector2(px_x // 125, px_y // 125)

curr_player = GL.BLACK
is_running = True
pending_move = PendingMove(board, curr_player)

# debugging
show_mouse_moves = False

while is_running:

    if curr_player == GL.RED:
        start_s = time.time()
        move = ALG.minimax(board, DEPTH, float('-inf'), float('inf'), True)[0]
        end_s = time.time()
        print('move found in ' + str(round(end_s-start_s,4)) + ' seconds')
        GL.execute_move(board, move)
        pending_move.switch_player()
        curr_player *= -1
        gm = GL.game_over(board, curr_player)
        if gm:
            print([None, 'Red', 'Black'][gm] + ' Won!')
            is_running = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            is_running = False
            break

        if event.type == pygame.KEYDOWN: # debugging
            if event.key == pygame.K_m:
                ms = GL.get_all_potential_moves(board, curr_player)
                if len(ms) == 0:
                    print('no moves!')
                for m in ms:
                    print(m)
                print()
            
            if event.key == pygame.K_p:
                print(board)
            
            if event.key == pygame.K_t:
                print('Turn: ' + [None, 'Red', 'Black'][curr_player])
            
            if event.key == pygame.K_l:
                show_mouse_moves = not show_mouse_moves
                print('Toggled ' + ['Off', 'On'][show_mouse_moves] + ' Show Mouse Moves')

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            from_vec = get_grid_tile(x, y)
            if show_mouse_moves:
                print("from: " + str(from_vec))
            pending_move.set_start(from_vec)

        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            to_vec = get_grid_tile(x, y)
            if show_mouse_moves:
                print("to: " + str(to_vec))
            pending_move.set_end(to_vec)
            
            if pending_move.is_valid():
                if show_mouse_moves:
                    print('VALID')
                    print()
                GL.execute_move(board, pending_move)
                pending_move.switch_player()
                curr_player *= -1
                gm = GL.game_over(board, curr_player)
                if gm:
                    print([None, 'Red', 'Black'][gm] + ' Won!')
                    is_running = False
            else:
                if show_mouse_moves:
                    print('NOT VALID')
                    print()
                pending_move.reset()
        
    render()


pygame.display.quit()
pygame.quit()
exit()