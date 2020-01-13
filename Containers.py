import GameLogic as GL

class PotentialMove:
    
    def __init__(self, start_vec, end_vec, captured=None):
        self.start_vec = start_vec
        self.end_vec = end_vec
        self.captured = captured
    
    def __eq__(self, other):
        if type(other) is tuple:
            return self.start_vec == other[0] and self.end_vec == other[1]
        assert type(other) is PotentialMove
        return self.start_vec == other.start_vec and self.end_vec == other.end_vec
    
    def __str__(self):
        return '<PotentialMove | start: ' + str(self.start_vec) + ' end: ' + str(self.end_vec) + 'captured: ' + str(self.captured) + '>'
    
    def __repr__(self):
        return '<PotentialMove | start: ' + str(self.start_vec) + ' end: ' + str(self.end_vec) + 'captured: ' + str(self.captured) + '>'

class PendingMove:

    def __init__(self, board, player):
        self.board = board
        self.start_vec = None
        self.end_vec = None
        self.player = player
        self.captured = None
    
    def set_start(self, vec):
        self.start_vec = vec

    def set_end(self, vec):
        self.end_vec = vec

    def is_valid(self):
        if self.start_vec is None or self.end_vec is None: # check if one hasnt been set yet
            return False

        start_piece = GL.get_piece(self.board, self.start_vec)
        end_piece = GL.get_piece(self.board, self.end_vec)

        if GL.get_team(start_piece) != self.player: # make sure you're moving your own pieces
            return False
        if end_piece != GL.EMPTY: # you must move to an empty square
            return False
        
        move_tup = (self.start_vec, self.end_vec)

        temp = GL.get_potential_moves(self.board, self.start_vec)

        for potential_move in temp:
            if potential_move == move_tup:
                self.captured = potential_move.captured
                if GL.can_capture(self.board, self.player) and not self.captured:
                    return False
                return True

        return False
    
    def reset(self):
        self.start_vec = None
        self.end_vec = None
        self.captured = None
    
    def switch_player(self):
        self.player *= -1
        self.reset()

class Vector2:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        assert type(other) is Vector2
        return Vector2(self.x+other.x, self.y+other.y)
    
    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __eq__(self, other):
        assert type(other) is Vector2
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return '<Vec2 | x: ' + str(self.x) + ' y: ' + str(self.y) + '>'
    
    def __repr__(self):
        return '<Vec2 | x: ' + str(self.x) + ' y: ' + str(self.y) + '>'