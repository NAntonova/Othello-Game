# Natalia Antonova, 67443616
# Project 4 - Othello

'''
This modeule implements the user interface of the game Othello, which is simplified
'''

import othello_logic

convert_letters_to_int = {'N': 0, 'W': 1, 'B': 2}
convert_letters_to_full_words = {0: 'NONE', 1: 'WHITE', 2: 'BLACK'}
convert_int_to_letters = {0: 'N', 1: 'W', 2: 'B'}

def show_board(board: [[list]]) -> None:
    ''' Prints the game board '''
    for row in range(len(board[0])):
        for col in range(len(board)):
            print((((str(board[col][row])).replace('0', '.')).replace('1', 'W')).replace('2', 'B')+" ", end="")
        print()


def user_interface() -> None:
    ''' Function that implements the user interface of the game Othello '''
    
    print("FULL")
    # the user types his/her preferences of the game ----------------
    while True:
        try:
            rows = int(input())
            othello_logic.valid_number_of_rows_or_columns(rows)
            break
        except othello_logic.InvalidInput:
            print('Invalid input. It should be even integer between 4 and 16 (inclusive).')
    while True:
        try:
            columns = int(input())
            othello_logic.valid_number_of_rows_or_columns(columns)
            break
        except othello_logic.InvalidInput:
            print('Invalid input. It should be even integer between 4 and 16 (inclusive).')
    turn = convert_letters_to_int[input()]
    top_left = convert_letters_to_int[input()]
    criteria = input()

    # create the initial board -------------------------------------
    board = othello_logic.game_board(rows, columns, top_left)
    # --------------------------------------------------------------
    methods = othello_logic.Othello(board, turn)
    # Next 4 lines are only for the first steps of the game --------
    print('B: {} W: {}'.format(methods.number_discs()[2],  methods.number_discs()[1]))
    show_board(board)
    turn_num = methods.turn()
    print('TURN: {}'.format(convert_int_to_letters[turn_num]))

    while True:
        try:
            # SKIP MOVE? ---------------------
            turn_num_new = methods.skip_turn_if_needed()
            if turn_num_new != turn_num:
                print('TURN: {}'.format(convert_int_to_letters[turn_num_new]))
            # VALIDITY OF MOVE AND MAKE MOVE--
            move = input()
            move = {'row': int(move.split()[0])-1, 'col': int(move.split()[1])-1}
            board = methods.validity_and_flip(move)
            methods.make_move(move)
            print('VALID')
            # NUMBER OF BLACKs AND WHITEs-----
            print('B: {} W: {}'.format(methods.number_discs()[2], methods.number_discs()[1]))
            # BOARD --------------------------
            show_board(board)
            # WINNER IF GAME IS OVER ---------
            winner = methods.winner_by_criteria(criteria, methods.number_discs())
            # GAME OVER? ---------------------
            methods.is_game_over(methods.number_discs()[0], move)
            # TURN ---------------------------
            turn_num = methods.turn()
            print('TURN: {}'.format(convert_int_to_letters[turn_num]))

        except othello_logic.InvalidMoveError:
            print('INVALID')
        except othello_logic.GameOverError:
            print('WINNER: '+ convert_letters_to_full_words[winner])
            break
                       


if __name__ == '__main__':
    user_interface()
