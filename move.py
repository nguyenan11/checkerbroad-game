'''
An Nguyen
CS 5001, Fall 2020 - Checker Broad Game

This file handles all necessary infomation of a move.
'''


class Move:
    '''
    Class -- Move
        Represents a move.
    Attributes:
        start -- A list storing coordinate X and Y of starting position
        end -- A list storing coordinate X and Y of ending position
        capturing_move -- A boolean value whether this move is capturing
        move
    '''

    def __init__(self, start, end, capturing_move=False):
        '''
        Constructor -- Creates a new instance of Move.
        Parameters:
            self -- The current Move object
            start -- A list storing coordinate X and Y of starting position
            end -- A list storing coordinate X and Y of ending position
            capturing_move -- A boolean value whether this move is capturing
            move. Automatically set to False if no input was taken.
        '''
        self.start = start
        self.end = end
        self.capturing_move = capturing_move

    def __eq__(self, other):
        '''
        Method -- __eq__
            Checks if two objects are equal
        Parameters:
            self -- The current Move object
            other -- An object to compare self to.
        Returns:
            True if the two objects are equal, False otherwise.
        '''
        if type(self) != type(other):
            return False
        return self.start == other.start and self.end == other.end
