'''
An Nguyen
CS 5001, Fall 2020 - Checker Broad Game

This file handles all necessary infomation of a piece.
'''


class Piece:
    '''
    Class -- Piece
        Represents a piece.
    Attributes:
        color -- The piece's color, a string
        king_status -- A boolean value whether a piece is King
        direction -- nested list of possible direction for piece to move
    Methods:
        assign_direction -- Assigns directions for piece.
    '''

    def __init__(self, color, king_status):
        '''
        Constructor -- Creates a new instance of Piece.
        Parameters:
            color -- The piece's color, a string
            king_status -- A boolean value whether a piece is King
        '''
        self.color = color
        self.king_status = king_status
        self.direction = []
        self.assign_direction()

    def assign_direction(self):
        '''
        Method -- assign_direction
            Assigns directions to piece
        Parameter:
            self -- the current Piece object
        '''
        if self.king_status:
            self.direction = [[1, -1], [1, 1], [-1, -1], [-1, 1]]
        else:
            if self.color == "black":
                self.direction = [[1, -1], [1, 1]]
            elif self.color == "red":
                self.direction = [[-1, -1], [-1, 1]]

    def __eq__(self, other):
        '''
        Method -- __eq__
            Checks if two objects are equal
        Parameters:
            self -- The current Piece object
            other -- An object to compare self to.
        Returns:
            True if the two objects are equal, False otherwise.
        '''
        return self.color == other.color
