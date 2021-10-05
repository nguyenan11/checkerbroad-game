from constants import RED, BLACK, EMPTY
from game_state import GameState
from move import Move


def test_constructor():
    game = GameState(True)
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
    assert(game.square == square)
    assert(game.turn == "Black's turn")
    assert(game.ai_in_process is False)
    assert(game.more_capture_avail is False)
    assert(game.test_mode is True)  # obvious, otherwise the test won't run


def test_piece_belong():
    # Will test on black's turn first, then change to red's
    game = GameState(True)
    assert(game.piece_belong(1, 0) is True)  # Black piece
    assert(game.piece_belong(0, 0) is False)  # Empty square
    assert(game.piece_belong(4, 5) is False)  # Red piece
    assert(game.piece_belong(2, 9) is False)  # y is out of bound
    game.change_turn()
    assert(game.piece_belong(4, 5) is True)  # Same Red piece as above
    assert(game.piece_belong(1, 0) is False)  # Same Black piece as above
    assert(game.piece_belong(-5, 1) is False)  # x is out of bound


def test_game_over():
    game = GameState(True)
    game.update_all_moves()
    assert(game.game_over() is None)
    game.square = [
        [EMPTY, BLACK, EMPTY, BLACK, EMPTY, BLACK, EMPTY, BLACK],  # this row
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
            ]
    game.update_all_moves()
    assert(game.game_over() == "Game over!\nBlack Won")
    game.square = [
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [RED, EMPTY, RED, EMPTY, RED, EMPTY, RED, EMPTY]  # this row
            ]
    game.update_all_moves()
    assert(game.game_over() == "Game over!\nRed Won")


def test_prioritize_capture():
    game = GameState(True)
    # Create list of move objects with random number then test
    move_1 = Move([1, 2], [3, 4], False)
    move_2 = Move([5, 6], [7, 8], True)
    move_3 = Move([4, 3], [2, 1], False)
    move_list = [move_1, move_2, move_3]
    assert(game.prioritize_capture(move_list) == [move_2])
    move_list.remove(move_2)
    assert(game.prioritize_capture(move_list) == [move_1, move_3])
    move_list.clear()
    assert(game.prioritize_capture(move_list) == [])


def test_check_king_status():
    game = GameState(True)
    assert(game.check_king_status("black", 7) is True)
    assert(game.check_king_status("red", 0) is True)
    assert(game.check_king_status("black", 0) is False)
    assert(game.check_king_status("red", 5) is False)


def test_convert():
    game = GameState(True)
    assert(game.convert(150) == 7)
    assert(game.convert(-198) == 0)
    assert(game.convert(-73) == 2)


def test_valid_next_move():
    game = GameState(True)
    game.update_all_moves()

    # Black piece with two possible non - capturing moves
    assert(game.valid_next_move(3, 2, 2, 3) is True)
    assert(game.valid_next_move(3, 2, 4, 3) is True)

    # Same piece but not a valid move
    assert(game.valid_next_move(3, 2, 5, 6) is False)

    # Set up a capturing move (black captures red) so it can be tested
    game.square = [
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, BLACK, EMPTY, EMPTY, EMPTY, EMPTY],  # this row
        [EMPTY, EMPTY, RED, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],  # and this row
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
            ]

    game.update_all_moves()
    assert(game.valid_next_move(3, 2, 1, 4) is True)
