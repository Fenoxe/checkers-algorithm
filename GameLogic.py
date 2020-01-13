import numpy as np
from copy import deepcopy
from Containers import PotentialMove, Vector2, PendingMove

BLACK = -1
RED = 1
EMPTY = 0
CHECKER = 1

KING = 2

GBL_MOVE_OFFSETS = [Vector2(1,-1), Vector2(1,1), Vector2(-1,-1), Vector2(-1,1)]

def create_board():
    board = np.zeros(shape=(8,8), dtype=int)

    for y in range(3):
        for x in range((y + 1) % 2, 8, 2):
            board[y,x] = RED

    for y in range(5,8):
        for x in range((y + 1) % 2, 8, 2):
            board[y,x] = BLACK
        
    return board

def get_piece(board, pos):
    if pos.x < 0 or pos.x > 7 or pos.y < 0 or pos.y > 7:
        return None
    return board[pos.y,pos.x]

def get_team(piece):
    if piece is None:
        return None
    elif piece * RED > 0:
        return RED
    elif piece * BLACK > 0:
        return BLACK
    return EMPTY

def remove_piece(board, pos):
    board[pos.y,pos.x] = EMPTY

def add_piece(board, pos, piece):
    board[pos.y,pos.x] = piece

# add all conditions, be thorough
def game_over(board, player_turn):

    red_has_pieces = False
    black_has_pieces = False

    for y in range(8):
        for x in range(8):
            team = get_team(get_piece(board, Vector2(x,y)))
            if team == RED:
                red_has_pieces = True
            elif team == BLACK:
                black_has_pieces = True
            if black_has_pieces and red_has_pieces:
                break
        if black_has_pieces and red_has_pieces:
            break
    
    if not red_has_pieces:
        return BLACK
    if not black_has_pieces:
        return RED

    for y in range(8):
        for x in range(8):
            pos = Vector2(x,y)
            
            if get_team(get_piece(board, pos)) == player_turn and len(get_potential_moves(board, pos)) > 0:
                return False

    return -1 * player_turn

def move_piece(board, start_pos, end_pos, create_king=False):
    piece = get_piece(board, start_pos)
    remove_piece(board, start_pos)
    if create_king:
        add_piece(board, end_pos, (piece // abs(piece)) * 2)
    else:
        add_piece(board, end_pos, piece)

def get_potential_moves(board, pos):

    out = []

    piece = get_piece(board, pos)
    team = get_team(piece)
    is_king = (team != piece)
    opposite_team = -1 * team

    if is_king:
        offsets = GBL_MOVE_OFFSETS
    else:
        offsets = GBL_MOVE_OFFSETS[(team + 1) // 2::2]

    can_jump = False
    
    for offset_vec in offsets:
        potential_move = pos + offset_vec
        
        potential_move_team = get_team(get_piece(board, potential_move))

        if potential_move_team is None: # if out of bounds, skip
            continue

        if not can_jump and potential_move_team == EMPTY:
            out.append(PotentialMove(pos, potential_move))
        elif not can_jump and potential_move_team == team:
            continue
        elif potential_move_team == opposite_team:
            # check next tile to be blank
            captured_vec = potential_move
            potential_move += offset_vec
            if get_piece(board, potential_move) == EMPTY:
                # start search process
                if not can_jump:
                    out = []
                can_jump = True
                captured = [captured_vec]
                new_board = deepcopy(board)
                remove_piece(new_board, captured_vec)
                remove_piece(new_board, pos)
                search_jumps(new_board, pos, potential_move, offsets, team, captured, out)
    return out

def search_jumps(board, original_pos, curr_pos, offsets, team, captured, out):
    
    final_move = True

    opposite_team = -1 * team

    for offset_vec in offsets:
        check_tile_pos = curr_pos + offset_vec
        
        check_tile_team = get_team(get_piece(board, check_tile_pos))

        if check_tile_team is None: # skip if out of bounds
            continue

        if check_tile_team == opposite_team:
            captured_vec = check_tile_pos
            potential_move = check_tile_pos + offset_vec
            if get_piece(board, potential_move) == EMPTY:
                # recursively search
                final_move = False
                new_captured = deepcopy(captured)
                new_board = deepcopy(board)
                remove_piece(new_board, captured_vec)
                new_captured.append(captured_vec)
                search_jumps(new_board, original_pos, potential_move, offsets, team, new_captured, out)
    
    if final_move:
        out.append(PotentialMove(original_pos, curr_pos, captured))

def get_all_potential_moves(board, player):
    out = []

    for y in range(8):
        for x in range(8):
            vec = Vector2(x, y)
            if get_team(get_piece(board, vec)) == player:
                for pm in get_potential_moves(board, vec):
                    out.append(pm)
    
    captured_out = list(filter(lambda pm: pm.captured, out))

    if len(captured_out) > 0:
        return captured_out
    return out

def execute_move(board, pending_move): # Also works with PotentialMove objs
    from_vec = pending_move.start_vec
    to_vec = pending_move.end_vec

    king = to_vec.y in [0,7]

    move_piece(board, from_vec, to_vec, create_king=king)

    if pending_move.captured is not None:
        for piece_vec in pending_move.captured:
            remove_piece(board, piece_vec)

def can_capture(board, player):
    for y in range(8):
        for x in range(8):
            vec = Vector2(x, y)
            if get_team(get_piece(board, vec)) == player:
                for pm in get_potential_moves(board, vec):
                    if pm.captured:
                        return True
    
    return False
