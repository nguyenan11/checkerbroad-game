'''
An Nguyen
CS 5001, Fall 2020 - Checker Broad Game

This file handles everything related to the game state as well as all logic.
x, y, a, b were used a lot in this file; where x, y are referred as the
starting coordinate (the initial click), and a, b as the ending coordinate
(the click after the first one).
'''
import turtle
from drawing import Drawing
from piece import Piece
from move import Move
import random
from constants import BLACK, RED, EMPTY, BOUNDS, CAPTURE, SINGLE_PLAY,\
    KING_BLACK_QUALIFIER, KING_RED_QUALIFIER, SQUARE, HALF_NUM_SQUARE, PROMPT


class GameState:
    '''
    Class -- GameState
        The state of the game.
    Attributes:
        squares -- A nested list storing the state of each square on the board
        coordinate -- A list storing maximum 4 integer values (from clicks)
        hint_coordinate -- A list storing Move object as hints
        next_required_capture -- A list storing Move objects with higher
        priority than possible_moves
        possible_moves -- A list storing all possible Move objects
        red_moves -- A list storing all Move objects of Red pieces
        black_moves -- A list storing all Move objects of Black pieces
        ai_start -- A list with 2 values of coordinate; where AI starts
        ai_en -- A list with 2 values of coordinate; where AI ends up
        ai_in_process -- A boolean value of whether AI's in process
        more_capture_avail -- A boolean value of if more capture is available
        turn -- Whose turn it is, a string
        play_mode -- An integer of either 1 (player) or 2 (players)
        drawing -- The current Drawing object
        screen -- The Turtle's screen
        test_mode -- A boolean value of whether GameState is in test mode
    Methods:
        piece_belong -- Checks if selected piece belongs to current player.
        game_over -- Checks whether the game is over.
        update_all_moves -- Updates all the possible moves in the game at once.
        add_move -- Adds a Move object to the desired GameState's attribute.
        prioritize_capture -- Updates the list with capturing move(s) only, if
        applicable.
        check_king_status -- Checks if a piece qualified to be a King.
        convert -- Converts a click coordinate to a square location.
        get_hint -- Gets a hint coordinate from object's possible_moves.
        ai_select_move -- AI to select a random move from assigned list.
        ai_first_move -- AI initialized its move, displaying on UI.
        ai_second_move -- AI finished its move.
        ai_move -- AI makes a move with a small delay during first and second
        move, by calling other 3 AI methods.
        delay_for_ai_move -- Ensures AI to complete moving even when human
        tries to mess with it.
        valid_next_move -- Validates if a move is possible.
        must_continue_check -- Checks if there's more capture move after 1 just
        made.
        move_pieces -- Moves piece across broad with significant UI's drawings
        and game's logics.
        click_handler -- The click event listener
    '''

    square = [
            [EMPTY, BLACK, EMPTY, BLACK, EMPTY, BLACK, EMPTY, BLACK],
            [BLACK, EMPTY, BLACK, EMPTY, BLACK, EMPTY, BLACK, EMPTY],
            [EMPTY, BLACK, EMPTY, BLACK, EMPTY, BLACK, EMPTY, BLACK],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [RED, EMPTY, RED, EMPTY, RED, EMPTY, RED, EMPTY],
            [EMPTY, RED, EMPTY, RED, EMPTY, RED, EMPTY, RED],
            [RED, EMPTY, RED, EMPTY, RED, EMPTY, RED, EMPTY]
            ]
    '''
    As far as how the game goes, each square can be accessed by
    square[col][row], which is different than a usual square[row][col]
    '''
    coordinate, hint_coordinate = [], []
    next_required_capture, possible_moves = [], []
    red_moves, black_moves = [], []
    ai_start, ai_end = [], []
    ai_in_process = False
    more_capture_avail = False

    def __init__(self, test_mode):
        '''
        Constructor -- Creates a new instance of GameState
        Parameters:
            self -- The current GameState object
            test_mode -- True if GameState object is in test mode (pytest),
            False for regular game as in main
        '''
        self.turn = "Black's turn"
        # Black's turn (or human player) always starts first
        self.test_mode = test_mode
        if not self.test_mode:
            # A True value will allow pytest to run without popping up UI
            self.drawing = Drawing()
            self.drawing.initial_setup()
            self.update_all_moves()
            self.screen = turtle.Screen()
            self.screen.title("Checker")
            self.play_mode = round(self.screen.numinput("Play mode?",
                                   PROMPT, 1, minval=1, maxval=2))
            self.drawing.write_to_screen(self.turn, self.more_capture_avail,
                                         "Click on board to Start\n     " +
                                         str(self.play_mode) + " player mode")
            self.screen.onclick(self.click_handler)
            turtle.done()

    def piece_belong(self, x, y):
        '''
        Method -- piece_belong
            Checks if selected piece belongs to current player.
        Parameters:
            self -- the current GameState object
            x -- the X coordinate of the click, an int
            y -- the Y coordinate of the click, an int
        Returns:
            True if piece matches current player, False otherwise.
        '''
        try:
            if x in BOUNDS and y in BOUNDS:
                click = self.square[y][x]
                if self.turn == "Black's turn":
                    return click.color == "black"
                return click.color == "red"
            return False
        except TypeError:  # abusive, non-stop clicks will crash the game
            return False

    def game_over(self):
        '''
        Method -- game_over
            Checks whether the game is over.
        Parameters:
            self -- the current GameState object
        Returns:
            A string informing Game Over and who won when it's over, None when
            it's not.
        '''
        OVER = 0
        black_counts = sum(row.count(BLACK) for row in self.square)
        red_counts = sum(row.count(RED) for row in self.square)
        if black_counts == OVER or self.black_moves == []:
            return "Game over!\nRed Won"
        elif red_counts == OVER or self.red_moves == []:
            return "Game over!\nBlack Won"
        return None

    def update_all_moves(self):
        '''
        Method -- update_all_moves
            Updates all the possible moves in the game at once.
        Parameters:
            self -- the current GameState object
        Returns:
            Nothing. This is helper method to add Move objects to GameState
            object's black_moves, red_moves, and possible_moves.
        '''
        self.red_moves, self.black_moves = [], []
        for row in BOUNDS:
            for col in BOUNDS:
                next_row, next_col = None, None
                click = self.square[col][row]
                move = None
                for direction in click.direction:
                    try:
                        move_col = col + direction[0]
                        move_row = row + direction[1]
                        next_click = self.square[move_col][move_row]
                        if next_click.color == "empty":
                            self.add_move(row, col, move_row, move_col, False)
                        elif next_click.color != click.color:
                            move_col += direction[0]
                            move_row += direction[1]
                            next_click = self.square[move_col][move_row]
                            if next_click.color == "empty":
                                self.add_move(row, col, move_row, move_col,
                                              True)
                    except IndexError:
                        pass
        self.red_moves = self.prioritize_capture(self.red_moves)
        self.black_moves = self.prioritize_capture(self.black_moves)
        self.possible_moves = self.red_moves + self.black_moves

    def add_move(self, row, col, move_row, move_col, capturing_move):
        '''
        Method -- add_move
            Adds a Move object to the desired GameState's attribute.
        Parameters:
            self -- the current GameState object
            row -- the X coordinate of the current piece, an int
            col -- the Y coordinate of the current piece, an int
            move_row -- the X coordinate of where piece can possibly move to,
            an int
            move_col -- the Y coordinate of where piece can possibly move to,
            an int
            capturing_move -- a boolean value of whether this move is capturing
            move
        Returns:
            Nothing. This is another helper method to add a Move object to
            GameState object's black_moves and red_moves.
        '''
        if move_row in BOUNDS and move_col in BOUNDS:
            color = self.square[col][row].color
            move = Move([row, col], [move_row, move_col], capturing_move)
            if color == "black":
                self.black_moves.append(move)
            elif color == "red":
                self.red_moves.append(move)

    def prioritize_capture(self, list_of_moves):
        '''
        Method -- prioritize_capture
            Updates the list with capturing move(s) only, if applicable.
        Parameters:
            self -- the current GameState object
            list_of_moves -- A list contains Move objects
        Returns:
            A filtered list with capturing moves, if they exist; the original
            otherwise.
        '''
        capturing_list = []
        for move in list_of_moves:
            if move.capturing_move:
                capturing_list.append(move)
        if capturing_list != []:
            return capturing_list
        return list_of_moves

    def check_king_status(self, color, b):
        '''
        Method -- check_king_status
            Checks if a piece qualified to be a King.
        Parameters:
            self -- the current GameState object
            color -- the color of the piece, a string
            b -- the ending Y coordinate, an int
        Returns:
            True if piece has reached the end of enemy's side, False otherwise.
        '''
        if color == "black":
            return b == KING_BLACK_QUALIFIER
        return b == KING_RED_QUALIFIER

    def change_turn(self):
        if self.turn == "Black's turn":
            self.turn = "Red's turn"
        else:
            self.turn = "Black's turn"

    def convert(self, coordinate):
        '''
        Method -- convert
            Converts a click coordinate to a square location.
        Parameters:
            self -- the current GameState object
            coordinate -- one of the coordinate of click (x or y), a float
        Returns:
            The index of the square that was clicked. Works for row and col.
        '''
        return int(coordinate) // SQUARE + HALF_NUM_SQUARE

    def get_hint(self, x, y):
        '''
        Method -- get_hint
            Gets a hint coordinate from object's possible_moves.
        Parameters:
            self -- the current GameState object
            x -- the X coordinate of the clicked piece, an int
            y -- the Y coordinate of the clicked piece, an int
        Returns:
            Nothing. This is helper method to add Move objects to GameState
            object's hint_coordinate
        '''
        if not self.more_capture_avail:
            for move in self.possible_moves:
                if move.start == [x, y]:
                    self.hint_coordinate.append(move)
        else:
            for move in self.next_required_capture:
                self.hint_coordinate.append(move)

    def ai_select_move(self):
        '''
        Method -- ai_select_move
            AI to select a random move from assigned list.
        Parameters:
            self -- the current GameState object
        Returns:
            Nothing. This is helper method taken no arguments so it can be
            called by screen.ontimer. Current object's ai_start and ai_end will
            be updated with a list containing coordinate (X and Y).
        '''
        self.update_all_moves()
        if self.more_capture_avail:
            selection = random.choice(self.next_required_capture)
        else:
            selection = random.choice(self.red_moves)
        self.ai_start = selection.start
        self.ai_end = selection.end

    def ai_first_move(self):
        '''
        Method -- ai_first_move
            AI initialized its move, displaying on UI.
        Parameters:
            self -- the current GameState object
        Returns:
            Nothing. This is helper method taken no arguments so it can be
            called by screen.ontimer. A hint square and tiny hint circle will
            be displayed.
        '''
        self.drawing.draw_small_square(self.ai_end[0], self.ai_end[1],
                                       "yellow")
        self.drawing.draw_hint_circle(self.ai_start[0], self.ai_start[1])

    def ai_second_move(self):
        '''
        Method -- ai_second_move
            AI finished its move.
        Parameters:
            self -- the current GameState object
        Returns:
            Nothing. This is helper method taken no arguments so it can be
            called by screen.ontimer. Piece will move from ai_start to ai_end.
        '''
        self.move_pieces(self.ai_start[0], self.ai_start[1],
                         self.ai_end[0], self.ai_end[1])

    def ai_move(self):
        '''
        Method -- ai_move
            AI makes a move with a small delay during first and second move,
            by calling other 3 AI methods.
        Parameters:
            self -- the current GameState object
        Returns:
            Nothing. This is helper method called other helper methods of AI so
            it can successfully move without being disturbed.
        '''
        self.ai_select_move()
        self.screen.ontimer(self.ai_first_move, 1000)
        self.screen.ontimer(self.ai_second_move, 2000)
        self.screen.ontimer(self.delay_for_ai_move, 2300)
        # delay for self.more_capture_avail to be updated accurately

    def delay_for_ai_move(self):
        '''
        Method -- delay_for_ai_move
            Ensures AI to complete moving when human tries to mess with it.
        Parameters:
            self -- the current GameState object
        Returns:
            Nothing. This is helper method taken no arguments so it can be
            called by screen.ontimer. If more capture(s) is available, ai_move
            will be called again.
        '''
        if not self.more_capture_avail:
            self.ai_in_process = False
            # True value will prevent human from interacting with AI
        elif self.more_capture_avail:
            self.ai_move()

    def valid_next_move(self, x, y, a, b):
        '''
        Method -- valid_next_move
            Validates if a move is possible.
        Parameters:
            self -- the current GameState object
            x -- the X coordinate of the initial click, an int
            y -- the Y coordinate of the initial click, an int
            a -- the X coordinate of the second click, an int
            b -- the Y coordinate of the second click, an int
        Returns:
            True if move can be made, False otherwise.
        '''
        next_move = Move([x, y], [a, b])
        if self.more_capture_avail:
            return next_move in self.next_required_capture
        return next_move in self.possible_moves

    def must_continue_check(self, a, b):
        '''
        Method -- must_continue_check
            Checks if there's more capture move after 1 just made.
        Parameters:
            self -- the current GameState object
            a -- the X coordinate of the second click, an int
            b -- the Y coordinate of the second click, an int
        Returns:
            Nothing. This is helper method to add Move objects to GameState
            object's list of next_require_capture and change the boolean value
            of more_capture_avail
        '''
        self.update_all_moves()
        self.next_required_capture = []
        for move in self.possible_moves:
            if move.start == [a, b] and move.capturing_move:
                self.next_required_capture.append(move)
        if self.next_required_capture != []:
            self.more_capture_avail = True
        else:
            self.more_capture_avail = False

    def move_pieces(self, x, y, a, b):
        '''
        Method -- move_pieces
            Moves piece across broad with significant UI's drawings and game's
            logics.
        Parameters:
            self -- the current GameState object
            x -- the X coordinate of the initial click, an int
            y -- the Y coordinate of the initial click, an int
            a -- the X coordinate of the second click, an int
            b -- the Y coordinate of the second click, an int
        Returns:
            Nothing. This is major helper method to allow piece go from one
            coordinate to another. Piece objects, and list of square will be
            updated accordingly.
        '''
        color = self.square[y][x].color
        self.square[b][a] = self.square[y][x]
        self.square[y][x] = EMPTY
        self.drawing.draw_small_square(x, y, "black")
        if self.check_king_status(color, b):
            self.square[b][a] = Piece(color, True)
            self.square[b][a].assign_direction()
        self.drawing.draw_small_square(a, b, "black")
        self.drawing.draw_small_circle(self.square[b][a], a, b)
        if abs(a - x) == CAPTURE:  # same as abs(b - y)
            self.square[(y+b) // 2][(x+a) // 2] = EMPTY
            self.drawing.draw_small_square((x + a)/2, (y+b)/2, "black")
            self.must_continue_check(a, b)
        if not self.more_capture_avail:
            self.change_turn()
        self.update_all_moves()
        self.drawing.write_to_screen(self.turn, self.more_capture_avail,
                                     self.game_over())

    def click_handler(self, x, y):
        '''
        Method -- click_handler
            The click event listener. Initial coordinate will be saved into
            object's attribute coordinate. If conditions are met though helper
            method, additional click will be taken after. Object's coordinate
            will be reset if conditions not met or 2 pairs are taken.
        Parameters:
            self -- the current Board object
            x -- The X coordinate of the click
            y -- The Y coordinate of the click
        Returns:
            Nothing. Handles all the logic of process of the game.
        '''
        self.drawing.write_to_screen(self.turn, self.more_capture_avail,
                                     self.game_over())
        if self.game_over() is None and not self.ai_in_process:
            self.coordinate.append(self.convert(x))
            self.coordinate.append(self.convert(y))
            x, y = self.coordinate[0], self.coordinate[1]
            self.get_hint(x, y)
            if len(self.coordinate) == 2:
                if self.piece_belong(x, y):
                    for hint in self.hint_coordinate:
                        if hint.start == [x, y]:
                            self.drawing.draw_small_square(hint.end[0],
                                                           hint.end[1],
                                                           "yellow")
                    self.drawing.draw_hint_circle(x, y)
                else:
                    self.coordinate, self.hint_coordinate = [], []
            elif len(self.coordinate) == 4:
                for hint in self.hint_coordinate:
                    self.drawing.draw_small_square(hint.end[0], hint.end[1],
                                                   "black")
                self.drawing.draw_small_circle(self.square[y][x], x, y)
                a, b = self.coordinate[2], self.coordinate[3]
                if self.valid_next_move(x, y, a, b):
                    self.move_pieces(x, y, a, b)
                self.coordinate, self.hint_coordinate = [], []
                if self.turn == "Red's turn" and self.play_mode == SINGLE_PLAY:
                    self.ai_in_process = True
                    self.ai_move()
