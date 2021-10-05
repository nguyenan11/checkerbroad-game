'''
An Nguyen
CS 5001, Fall 2020 - Checker Broad Game

This file handles all drawings of UI. Nothing in this file can be tested.
'''
import turtle
from constants import NUM_SQUARES, SQUARE, HALF_SQUARE, BROAD_SIZE, \
    HALF_BROAD, CORNER, WINDOW_SIZE, NO_CIRCLE_ROW_1, NO_CIRCLE_ROW_2, \
    SQUARE_COLOR, CIRCLE_COLORS, ORIGIN, KING_FACTOR, HINT_FACTOR


class Drawing:
    '''
    Class -- Drawing
        Represents all the drawings of UI.
    Attributes:
        None
    Methods:
        initial_setup -- Draws game's outline and all players' pieces.
        write_to_screen -- Writes message to the screen regarding the state
        of the game.
        draw_square -- Draws a square of a given size.
        draw_circle -- Draws a circle with a given radius.
        draw_small_square -- Draws a small square at given coordinate.
        draw_hint_circle -- Draws a tiny circle inside existing circle at given
        coordinate.
        draw_small_circle -- Draws a circle or 2 at given coordinate.
    '''

    def __init__(self):
        '''
        Constructor -- Creates a new instance of Drawing
        Parameters:
            self -- The current Drawing object.
        '''
        pass

    def initial_setup(self):
        '''
        Method -- initial_setup
            Draws game's outline and all players' pieces.
        Parameters:
            self -- the current Drawing object
        Returns:
            Nothing but the drawings.
        '''
        turtle.setup(WINDOW_SIZE, WINDOW_SIZE)
        turtle.screensize(BROAD_SIZE, BROAD_SIZE)
        turtle.bgcolor("white")
        turtle.tracer(ORIGIN, ORIGIN)

        pen = turtle.Turtle()
        pen.penup()
        pen.hideturtle()

        # The board outline
        pen.color("black", "white")
        pen.setposition(CORNER, CORNER)
        self.draw_square(pen, BROAD_SIZE)

        # Players' pieces
        for col in range(NUM_SQUARES):
            for row in range(NUM_SQUARES):
                if col % 2 != row % 2:
                    pen.color("black", SQUARE_COLOR)
                    pen.setposition(CORNER + SQUARE*col, CORNER + SQUARE*row)
                    self.draw_square(pen, SQUARE)
                    if row < NO_CIRCLE_ROW_1 or row > NO_CIRCLE_ROW_2:
                        color = CIRCLE_COLORS[row // 4]
                        pen.color(color, color)
                        self.draw_circle(pen, HALF_SQUARE)

    def write_to_screen(self, turn, more_capture, game_over):
        '''
        Method -- write_to_screen
            Writes message to the screen regarding the state of the game.
        Parameters:
            self -- the current Drawing object
            turn -- whose turn it is, a string
            more_capture -- boolean value whether more capture's available
            game_over -- boolean value whether the game is over
        Returns:
            Nothing. Writes a message in the graphics window at appropriate
            position.
        '''
        BIG_SIZE = 32
        turtle.clear()
        if game_over is not None:
            turtle.penup()
            turtle.setposition(ORIGIN, - BIG_SIZE)
            turtle.color("teal")
            turtle.write(game_over, align="center",
                         font=("Comic Sans MS", BIG_SIZE, "normal", "bold"))
        else:
            if more_capture:
                turn += " - more capture(s) found, same piece must continue!"
            turtle.setposition(CORNER, HALF_BROAD)
            turtle.color("black")
            turtle.write(turn, font=("Times New Roman", 14, "normal"))

    def draw_square(self, a_turtle, size):
        '''
        Method -- draw_square
            Draws a square of a given size.
        Parameters:
            self -- the current Drawing object
            a_turtle -- an instance of Turtle
            size -- the length of each side of the square
        Returns:
            Nothing. Draws a square in the graphics window.
        '''
        RIGHT_ANGLE = 90
        a_turtle.begin_fill()
        a_turtle.pendown()
        for i in range(4):
            a_turtle.forward(size)
            a_turtle.left(RIGHT_ANGLE)
        a_turtle.end_fill()
        a_turtle.penup()

    def draw_circle(self, a_turtle, radius):
        '''
        Method -- draw_circle
            Draws a circle with a given radius.
        Parameters:
            self -- the current Drawing object
            a_turtle -- an instance of Turtle
            radius -- the radius of the circle
        Returns:
            Nothing. Draws a circle in the graphics window.
        '''
        a_turtle.forward(radius)
        a_turtle.begin_fill()
        a_turtle.pendown()
        a_turtle.circle(radius)
        a_turtle.end_fill()
        a_turtle.penup()

    def draw_small_square(self, x, y, color):
        '''
        Method -- draw_small_square
            Draws a small square at given coordinate.
        Parameters:
            self -- the current Drawing object
            x -- the X coordinate of the click
            y -- the Y coordinate of the click
            color -- the assigned color
        Returns:
            Nothing. Draws a small square in the graphics window.
        '''
        pen = turtle.Turtle()
        pen.penup()
        pen.hideturtle()
        pen.color(color, SQUARE_COLOR)
        pen.setposition(CORNER + SQUARE * x, CORNER + SQUARE * y)
        self.draw_square(pen, SQUARE)

    def draw_hint_circle(self, x, y):
        '''
        Method -- draw_hint_circle
            Draws a tiny circle inside existing circle at given coordinate.
            Couldn't possibly combine with draw_small_circle because that would
            overlap drawings when piece is king and requires extra unnecessary
            code.
        Parameters:
            self -- the current Drawing object
            x -- the X coordinate of the click
            y -- the Y coordinate of the click
        Returns:
            Nothing. Draws a tiny circle in graphics window.
        '''
        pen = turtle.Turtle()
        pen.penup()
        pen.hideturtle()
        pen.setposition(CORNER + SQUARE * x + HALF_SQUARE * HINT_FACTOR,
                        CORNER + SQUARE * y + HALF_SQUARE * HINT_FACTOR)
        pen.color("yellow", "yellow")
        self.draw_circle(pen, HALF_SQUARE * (1 - HINT_FACTOR))

    def draw_small_circle(self, piece, x, y):
        '''
        Method -- draw_small_circle
            Draws a circle or 2 at given coordinate.
        Parameters:
            self -- the current Drawing object
            piece -- the current Piece object
            x -- the X coordinate of the click
            y -- the Y coordinate of the click
        Returns:
            Nothing. Draws a small circle in graphics window. If piece is king,
            a smaller circle will additionally be drawn inside.
        '''
        pen = turtle.Turtle()
        pen.penup()
        pen.hideturtle()
        pen.setposition(CORNER + SQUARE * x, CORNER + SQUARE * y)
        pen.color(piece.color, piece.color)
        self.draw_circle(pen, HALF_SQUARE)
        if piece.king_status:
            pen.setposition(CORNER + SQUARE * x + HALF_SQUARE * KING_FACTOR,
                            CORNER + SQUARE * y + HALF_SQUARE * KING_FACTOR)
            pen.color("white", piece.color)
            self.draw_circle(pen, HALF_SQUARE * (1 - KING_FACTOR))
