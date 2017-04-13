import tkinter
import othello_logic

DEFAULT_FONT = ('Helvetica', 20)
BG_COLOR = '#C5C1C0'




class Configurations:
    def __init__(self):
        ''' Create the window with configurations for othello'''
        self._config_window = tkinter.Tk()
        self._config_window.configure(background= BG_COLOR)
        # Configurations ---------------------------------
        config_label = tkinter.Label(
            master = self._config_window, text = 'Configurations',
            font = DEFAULT_FONT,
            bg = BG_COLOR)
        config_label.grid(
            row = 0, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.E + tkinter.W)
        # Rows -------------------------------------------
        num_rows_label = tkinter.Label(
            master = self._config_window, text = 'Rows (4,6,8,10,12,14,16): ',
            font = DEFAULT_FONT,
            bg = BG_COLOR)
        num_rows_label.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._rows_entry = tkinter.Entry(
            master = self._config_window, width = 20, font = DEFAULT_FONT)
        self._rows_entry.grid(
            row = 1, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)
        
        # Columns -----------------------------------------
        num_columns_label = tkinter.Label(
            master = self._config_window, text = 'Columns (4,6,8,10,12,14,16): ',
            font = DEFAULT_FONT,
            bg = BG_COLOR)
        num_columns_label.grid(
            row = 2, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._columns_entry = tkinter.Entry(
            master = self._config_window, width = 20, font = DEFAULT_FONT)
        self._columns_entry.grid(
            row = 2, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        
        # Who begins -------------------------------------
        who_begins_label = tkinter.Label(
            master = self._config_window, text = 'Who begins (black or white): ',
            font = DEFAULT_FONT,
            bg = BG_COLOR)
        who_begins_label.grid(
            row = 3, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)       
        
        self._who_begins_entry = tkinter.Entry(
            master = self._config_window, width = 20, font = DEFAULT_FONT)
        self._who_begins_entry.grid(
            row = 3, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)
        
        # Top-left cell -----------------------------------
        top_left_label = tkinter.Label(
            master = self._config_window, text = 'Top-left cell (black or white): ',
            font = DEFAULT_FONT,
            bg = BG_COLOR)
        top_left_label.grid(
            row = 4, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._top_left_entry = tkinter.Entry(
            master = self._config_window, width = 20, font = DEFAULT_FONT)
        self._top_left_entry.grid(
            row = 4, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)
        
        # Who wins ----------------------------------------
        who_wins_label = tkinter.Label(
            master = self._config_window, text = 'Win condition (more or less): ',
            font = DEFAULT_FONT,
            bg = BG_COLOR)
        who_wins_label.grid(
            row = 5, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)

        self._who_wins_entry = tkinter.Entry(
            master = self._config_window, width = 20, font = DEFAULT_FONT)
        self._who_wins_entry.grid(
            row = 5, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        # Ok button -------------------------------------
        ok_button = tkinter.Button(
            master = self._config_window, text = 'OK', font = DEFAULT_FONT,
            command = self.on_ok_button)
        ok_button.grid(row = 6, column = 0, columnspan = 2, padx = 10, pady = 10,
                       sticky = tkinter.E)

        self._ok_clicked = False
        self._rows = 0
        self._columns = 0
        self._who_begins = 0
        self._top_left = 0
        self._who_wins = 0

    def run(self) -> None:
        self._config_window.mainloop()

    def get_rows(self) -> int:
        return int(self._rows)

    def get_columns(self) -> int:
        return int(self._columns)

    def get_who_begins(self) -> int:
        if self._who_begins.lower() == 'black':
            return 2
        elif self._who_begins.lower() == 'white':
            return 1
        
    def get_top_left(self) -> int:
        if self._top_left.lower() == 'black':
            return 2
        elif self._top_left.lower() == 'white':
            return 1
        
    def get_who_wins(self) -> int:
        if self._who_wins.lower() == 'more':
            a = '>'
            return a
        elif self._who_wins.lower() == 'less':
            a = '<'
            return a
            
    def on_ok_button(self) -> None:
        ''' If clicked on OK, get the information for creating othello board,
            and call for othello window (aka open it)'''
        self._ok_clicked = True

        convert_to_num = {'none': 0, 'white': 1, 'black': 2}
        convert_criteria = {'more': '>', 'less': '<'}

        rows = int(self._rows_entry.get())
        columns = int(self._columns_entry.get())
        who_begins = convert_to_num[self._who_begins_entry.get().lower()]
        top_left = convert_to_num[self._top_left_entry.get().lower()]
        who_wins = convert_criteria[self._who_wins_entry.get().lower()]
        self._config_window.destroy()
        
        othello = OthelloApplication(rows, columns, who_begins, top_left, who_wins)
        othello.show()

        

class OthelloApplication:
    def __init__(self, rows, columns, who_begins, top_left, who_wins):
        ''' Create the window with Othello canvas'''
        self._othello_window = tkinter.Tk()
        self._othello_window.configure(background= BG_COLOR)

        self._rows = rows
        self._columns = columns
        self._turn = who_begins
        self._top_left = top_left
        self._who_wins = who_wins

        self._board = othello_logic.game_board(self._rows, self._columns, self._top_left)
        self._methods = othello_logic.Othello(self._board, self._turn)

        convert_to_words = {0: 'None', 1: 'White', 2: 'Black'}
        
        # WHOSE TURN
        self._whose_turn_text = tkinter.StringVar()
        self._whose_turn_text.set('Turn: {}'.format(convert_to_words[self._turn]))

        whose_turn_label = tkinter.Label(
            master = self._othello_window, textvariable = self._whose_turn_text,
            font = DEFAULT_FONT)

        whose_turn_label.grid(
            row = 0, column = 0, columnspan = 4, padx = 10, pady = 10,
            sticky = tkinter.E + tkinter.W)
                             
        # WHITE
        self._turn_white_text = tkinter.IntVar()
        self._turn_white_text.set('White: {}'.format(self._methods.number_discs()[1]))

        turn_white_label = tkinter.Label(
            master = self._othello_window, textvariable = self._turn_white_text,
            font = DEFAULT_FONT)
        turn_white_label.grid(
            row = 1, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W + tkinter.E + tkinter.N)
                             
        # BLACK
        self._turn_black_text = tkinter.IntVar()
        self._turn_black_text.set('Black: {}'.format(self._methods.number_discs()[2]))

        turn_black_label = tkinter.Label(
            master = self._othello_window, textvariable = self._turn_black_text,
            font = DEFAULT_FONT)
        turn_black_label.grid(
            row = 1, column = 2, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.E + tkinter.W)
        
        # BOARD
        self._canvas = tkinter.Canvas(
            master = self._othello_window, background = '#F7CE3E',
            width = 150*(self._columns), height = 150*(self._rows))

        self._canvas.grid(
            row = 2, column = 0, columnspan = 4, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)

        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        
        # WINNER
        self._who_win_text = tkinter.StringVar()
        self._who_win_text.set('')

        who_win_label = tkinter.Label(
            master = self._othello_window, textvariable = self._who_win_text,
            font = DEFAULT_FONT)

        who_win_label.grid(
            row = 3, column = 0, columnspan = 4, padx = 10, pady = 10,
            sticky = tkinter.E + tkinter.W)
        
        # FULL
        self._full_text = tkinter.StringVar()
        self._full_text.set('Full')

        full_label = tkinter.Label(
            master = self._othello_window, textvariable = self._full_text,
            font = ('Helvetica', 15))

        full_label.grid(
            row = 4, column = 0, columnspan = 4, padx = 10, pady = 10,
            sticky = tkinter.E+tkinter.W)
        
        ################################################
        self._othello_window.rowconfigure(0, weight = 0)
        self._othello_window.rowconfigure(1, weight = 0)
        self._othello_window.rowconfigure(2, weight = 1)
        self._othello_window.rowconfigure(3, weight = 0)
        self._othello_window.rowconfigure(4, weight = 0)
        self._othello_window.columnconfigure(0, weight = 1)
        self._othello_window.columnconfigure(1, weight = 1)
        self._othello_window.columnconfigure(2, weight = 1)
        self._othello_window.columnconfigure(3, weight = 1)


    def show(self) -> None:
        ''' Show the the main othello window (with the board) '''
        self._othello_window.grab_set()
        self._othello_window.wait_window()
        

    def _on_canvas_clicked(self, event: tkinter.Event) -> None:
        ''' If clicked somewhere on canvas, do all logic of othello'''
        convert_to_words = {0: 'None', 1: 'White', 2: 'Black'}
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        row_width = canvas_width/self._columns
        column_height = canvas_height/self._rows

        frac_x = event.x/canvas_width
        frac_y = event.y/canvas_height
        try:
            for col in range(self._columns):
                for row in range(self._rows):
                    if frac_x >= (col * row_width)/canvas_width and frac_x < ((col+1)*row_width)/canvas_width and frac_y >= (row * column_height)/canvas_height and frac_y < ((row+1)*column_height)/canvas_height:
                        move = {'row': row, 'col': col}
                        self._board = self._methods.validity_and_flip(move)
                        self._methods.make_move(move)
                        self._turn_white_text.set('White: {}'.format(self._methods.number_discs()[1]))
                        self._turn_black_text.set('Black: {}'.format(self._methods.number_discs()[2]))
                        self._winner = self._methods.winner_by_criteria(self._who_wins, self._methods.number_discs())
                        self._methods.is_game_over(self._methods.number_discs()[0], move)
                        self._turn = self._methods.turn()
                        self._turn_new = self._methods.skip_turn_if_needed()
                        if self._turn_new != self._turn:
                            self._whose_turn_text.set('Turn: {}'.format(convert_to_words[self._turn_new]))
                        else:
                            self._whose_turn_text.set('Turn: {}'.format(convert_to_words[self._turn]))
                            
        except othello_logic.InvalidMoveError:
            pass

        except othello_logic.GameOverError:
            self._who_win_text.set('Winner: {}'.format(convert_to_words[self._winner]))

        self._redraw_all()
                                   

    def _on_canvas_resized(self, event: tkinter.Event) -> None:
        '''Whenever the canvas' size changes, redraw everything,
            since sizes of everything has changed. '''
        self._redraw_all()          

    def _redraw_all(self) -> None:
        ''' Delete and redraw everything. Create new tiles if needed. '''
        self._canvas.delete(tkinter.ALL)

        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        row_width = canvas_width/self._columns
        column_height = canvas_height/self._rows

        for x in range(self._columns):
            for y in range(self._rows):
                self._canvas.create_line(row_width * x, 0,
                                         row_width * x, canvas_height, fill = '#000000')
                self._canvas.create_line(0, column_height * y,
                                         canvas_width, column_height * y, fill = '#000000')

        for col in range(len(self._board)):
            for row in range(len(self._board[0])):
                if self._board[col][row] == 1:
                    self._canvas.create_oval(
                        row_width * col, column_height * row,
                        row_width * (col+1), column_height * (row+1),
                        fill = '#FFFFFF')
                if self._board[col][row] == 2:
                    self._canvas.create_oval(
                        row_width * col, column_height * row,
                        row_width * (col+1), column_height * (row+1),
                        fill = '#000000')

if __name__ == '__main__':
    Configurations().run()
