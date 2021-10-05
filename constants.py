'''
An Nguyen
CS 5001, Fall 2020 - Checker Broad Game

This file contains constants used by both Drawing and GameState
'''
from piece import Piece


# The UI design's components and drawing's necessities
ORIGIN = 0
NUM_SQUARES = 8
SQUARE = 50
HALF_SQUARE = SQUARE // 2
BROAD_SIZE = NUM_SQUARES * SQUARE
HALF_BROAD = BROAD_SIZE // 2
CORNER = - HALF_BROAD
WINDOW_SIZE = BROAD_SIZE + SQUARE
NO_CIRCLE_ROW_1, NO_CIRCLE_ROW_2 = 3, 4
SQUARE_COLOR = "light gray"
CIRCLE_COLORS = ("black", "red")


# Factors of small circles
KING_FACTOR = 1/3
HINT_FACTOR = 3/4


# Game state's components
PROMPT = "Enter\n1 for single player\n2 for double players"
BLACK = Piece("black", False)
RED = Piece("red", False)
EMPTY = Piece("empty", False)
KING_BLACK_QUALIFIER = 7
KING_RED_QUALIFIER = 0
BOUNDS = range(0, NUM_SQUARES)
CAPTURE = 2
SINGLE_PLAY = 1
HALF_NUM_SQUARE = NUM_SQUARES // 2
