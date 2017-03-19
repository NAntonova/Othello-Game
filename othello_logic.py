# Natalia Antonova, 67443616
# Project 4 - Othello
# FULL VERSION

# Natalia Antonova, 67443616
# Project 4 - Othello

'''
This module contains the game logic that underlies a Othello game, which
is simplified. No user interface is included.
'''
#=================================================================
# Classes --------------------------------------------------------
class InvalidMoveError(Exception):
    '''Raised whenever an invalid move is made'''
    pass
    
class GameOverError(Exception):
    ''' Raised whenever an attempt is made to make a move after the game is
        already over '''
    pass

class InvalidInput(Exception):
    ''' Raised whenever the user types something that cannot be converted or
        used in the game Othello '''
    pass

class Othello:
    def __init__(self, board: [[int]], turn: int):
        self._turn = turn
        self._board = board

    def turn(self) -> int:
        ''' Changes turn '''
        num_discs_total = 0
        for col in self._board:
            for a in col:
                if a == 1 or a == 2:
                    num_discs_total += 1
        if num_discs_total == 4:
            return self._turn
        elif num_discs_total > 4:
            self._turn = _opposite_turn(self._turn)
            return self._turn

    def make_move(self, row_and_col_dict: dict) -> [[int]]:
        ''' Makes move '''
        self._board[row_and_col_dict['col']][row_and_col_dict['row']] = self._turn
        return self._board

    def number_discs(self) -> dict:
        ''' Calculates the number of specific tiles and returns three numbers in
            dictionary '''
        num = {0: 0, 1: 0, 2: 0}
        for col in self._board:
            for a in col:
                if a == 0:
                    num[0] += 1
                elif a == 1:
                    num[1] += 1
                elif a == 2:
                    num[2] += 1
        return num

    def is_game_over(self, number_of_zeros: dict, move: dict) -> int:
        ''' Checks if the game is over. '''
        lst_of_empty_tiles = []
        for col in range(len(self._board)):
            for row in range(len(self._board[0])):
                if self._board[col][row] == 0:
                    lst_of_empty_tiles.append({'col': col, 'row': row})
        # checks if the board is completely filled with tiles
        if number_of_zeros == 0:
            raise GameOverError
        # check if no open cells on the board are legal for either player
        lst_of_valid_moves_1 = []
        lst_of_valid_moves_2 = []
        for move in lst_of_empty_tiles:
            for valid_move in _list_of_adjacent_opposite_tiles(self._board, move, 1):
                lst_of_valid_moves_1.append(valid_move)
        for move in lst_of_empty_tiles:
            for valid_move in _list_of_adjacent_opposite_tiles(self._board, move, 2):
                lst_of_valid_moves_2.append(valid_move)              
        if lst_of_valid_moves_1 == [] and lst_of_valid_moves_2 == []:
            raise GameOverError

    def validity_and_flip(self, move: dict) -> [[int]] or None:
        ''' Function checks if the move is valid and if it is so, then the function
            returns the board with flipped tiles'''
        _is_move_in_board(self._board, move)
        _is_cell_empty(self._board, move)
        _has_adjacent_opposite_tiles(self._board, move, self._turn)
        _has_valid_moves_behind_adj(self._board, move, self._turn)
        self._board = _flip_tiles(_list_of_valid_moves(self._board, move, self._turn), self._board)
        return self._board

    def skip_turn_if_needed(self):
        if self._turn != _pass_move_and_switch_turn(self._board, self._turn):
            self._turn = _pass_move_and_switch_turn(self._board, self._turn)
        return self._turn

    def winner_by_criteria(self, criteria: str, dic_tiles: dict)->int:
        ''' Function determines the winning player, if any. It returns either
            0, 1, or 2. 0 means that nobody won the game. '''
        if criteria == '>':
            if dic_tiles[1] > dic_tiles[2]:
                winner = 1
            elif dic_tiles[1] < dic_tiles[2]:
                winner = 2
            elif dic_tiles[1] == dic_tiles[2]:
                winner = 0
        elif criteria == '<':
            if dic_tiles[1] > dic_tiles[2]:
                winner = 2
            elif dic_tiles[1] < dic_tiles[2]:
                winner = 1
            elif dic_tiles[1] == dic_tiles[2]:
                winner = 0
        return winner    

#=================================================================
# Functions that are used in the user interface --------------------
def game_board(rows: int, columns: int, arrangm: int) -> [[int]]:
    ''' Create a two-dimensional list that is a game board '''
    board = []
    for col in range(int(columns)):
        board.append([])
        for row in range(int(rows)):
            board[-1].append(0)
    board[int((columns/2)-1)][int((rows/2)-1):int((rows/2)+1)] = [arrangm, _opposite_turn(arrangm)]
    board[int(columns/2)][int((rows/2)-1):int((rows/2)+1)] = [_opposite_turn(arrangm), arrangm]
    return board

def valid_number_of_rows_or_columns(num: int) -> None:
    ''' Raises an InvalidMoveError if the user gave wrong number of columns
        or rows of the board. It whould be 4 or 6 or 8 or 10 or 12 or 14 or 16'''
    if num not in range(4, 17, 2):
        raise InvalidInput

#=================================================================
# Functions that are not used in the user interface

def _pass_move_and_switch_turn(board: [[int]], turn: int) -> int:
    ''' Function passes if the move cannot be made by that turn '''
    lst_of_empty_tiles = []
    for col in range(len(board)):
        for row in range(len(board[0])):
            if board[col][row] == 0:
                lst_of_empty_tiles.append({'col': col, 'row': row})
    lst_of_valid_moves = []
    for move in lst_of_empty_tiles:
        for valid_move in _list_of_valid_moves(board, move, turn):
            lst_of_valid_moves.append(valid_move)
    if lst_of_valid_moves == []:
        if turn == 1:
            turn = 2
        elif turn == 2:
            turn = 1
    return turn

def _require_game_not_over(board: [[int]], turn: int)-> None:
    ''' Raises a GameOverError if the given game state represents a situation
        where the game is over (i.e., there is a winning player) '''
    if winner(board, turn) != 0:
        raise GameOverError()
    
def _is_move_in_board(board: [[int]], move: dict):
    ''' Raises an InvalidMoveError if the user gave coordinates of non-existed
        cell in the board '''
    if (move['row'] < 0 or move['row'] >= len(board[0]) or move['col'] < 0 or move['col'] >= len(board)):
        raise InvalidMoveError

def _is_cell_empty(board: [[int]], move: dict) -> None:
    ''' Raises a InvalidMoveError if the cell is not empty '''
    if board[move['col']][move['row']] != 0:
        raise InvalidMoveError

def _has_adjacent_opposite_tiles(board: [[int]], move: dict, turn: int) -> None:
    ''' Raises an InvalidMoveError if no adjacent tiles of opposite color'''
    if _list_of_adjacent_opposite_tiles(board, move, turn) == []:
        raise InvalidMoveError

def _has_valid_moves_behind_adj(board: [[int]], move: dict, turn: int) -> None:
    ''' Raises an InvalidMoveError if no valid tiles '''
    if _list_of_valid_moves(board, move, turn) == []:
        raise InvalidMoveError

def _list_of_adjacent_opposite_tiles(board: [[int]], move: dict, turn: int) -> [dict]:
    ''' Function checks if there are any adjacent tiles that have opposite color
        and returns the list of dictionaroes that contain information about each
        adjacent tile that has opposite color'''

    max_col = len(board)
    max_row = len(board[0])
    
    results = []
    for col in [-1,0,1]:
        for row in [-1,0,1]:
            new_col = move['col'] + col
            new_row = move['row'] + row
            if (col == 0 and row == 0):
                continue
            if (new_col >= 0 and new_col < max_col and new_row >= 0 and new_row < max_row):
                if board[new_col][new_row] == _opposite_turn(turn):
                    results.append({'col': new_col, 'row': new_row,
                                    'direction': {'col': col, 'row': row},
                                    'color': board[new_col][new_row]})
    return results

def _list_of_valid_moves(board: [[int]], move: dict, turn: int) -> [dict]:
    lst_of_adj_opp_tiles = _list_of_adjacent_opposite_tiles(board, move, turn)
    results = []
    for tile in lst_of_adj_opp_tiles:
        for validmove in _get_list_of_discs_to_flip_in_one_direction(board, tile['col'],tile['row'],tile['direction'],tile['color']):
            results.append(validmove)
    return results
            
board = [[0,2,0,0],[0,0,1,0],[2,1,1,0],[0,0,0,0]]       
move = {'col': 2, 'row': 3}
turn = 2

def _opposite_turn(num_color: int) -> int:
    '''Given the player whose turn it is now, returns the opposite player'''
    if num_color == 1:
        return 2
    else:
        return 1
    
def _flip_tiles(list_of_tiles_to_flip: [dict], board: [[int]]):
    ''' Function flips the needed tiles '''
    for tile in list_of_tiles_to_flip:
        board[tile['col']][tile['row']] = _opposite_turn(board[tile['col']][tile['row']])
    return board


def _get_list_of_discs_to_flip_in_one_direction(board, col, row, direction, color):
    ''' Get the list of opposite tiles that needed to be flipped in the specific direction
        from one of 8 (valid) cells around the cell, where the user wants to put the tile'''
    lst = []
    if _does_it_has_needed_tiles_to_flip(board, col, row, direction, color, '') == True:
        while True:
            if board[col][row] == color:
                lst.append({'col': col, 'row': row})
                col += direction['col']
                row += direction['row']
            else:
                break
    return lst

def _does_it_has_needed_tiles_to_flip(board, col, row, direction, color, a):
    ''' Function checks if the tiles in one direction are ...'''
    a = a

    max_col = len(board)
    max_row = len(board[0])

    old_col = col
    old_row = row
    col += direction['col']
    row += direction['row']

    if col < max_col and col >= 0 and row < max_row and row >= 0:
        if board[col][row] == color:
            a = _does_it_has_needed_tiles_to_flip(board,col,row,direction,color,a)
        elif board[col][row] == _opposite_turn(color):
            a = True
        else:
            a = False
    else:
        a = False
    return a

