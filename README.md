# checkerbroad-game
Checkerbroad game is written in Python and run on the processing platform

# About the game
* Interactive visualization, easy-to-follow guidance on the screen
* Fun
* 2 play modes: Single player (against AI) or double players (great to compete against your friend)

# Demo after being ran on VSCode

## Single player

![Demo gif](demo/demo_gif.gif)

# Quick set of rules
* Pieces can only move diagonally.
* Non-king pieces can only move forward.
* Black always goes first.
![Black goes first](/demo/black_first.png)
> When a piece is clicked, possible move(s) will be indicated. If you click on enemy's pieces, nothing will be shown.

* You can only capture the enemy's piece(s). You cannot jump over your own pieces.
![Black blocked](/demo/black_block.png)

* When possible capture(s) available, that's the only move(s) can be made.
![Only move 1](demo/only_move1.png)
![Only move 2](demo/only_move2.png)

* Multiple captures enforced: after 1 capture, if there're more, you must finish them all.
![Multi captures 1](demo/multi_capture1.png)
![Multi captures 2](demo/multi_capture2.png)
> Notice how the direction changed to prompt user to continue.

* King pieces: When a piece get to the end of enemy's side, it becomes King - it now can move diagonally in 4 directions.
![King move 1](demo/king_move1.png)
![King move 2](demo/king_move2.png)

* Game over: Winner will be determined if all enemy's pieces are captured or enemy cannot make any moves.
![Game over](demo/game_over.png)

### Please let me know if you find any bugs or encounter any issues. I will be very appreciative!