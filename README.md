# checkerbroad-game
Checkerbroad game is written in Python and run on the processing platform

## Instruction: How to start the game
Download the source code into your folder, then run it on IDE - preferably **VSCode**. 

# About the game
* Interactive visualization, easy-to-follow guidance on the screen
* Fun
* 2 play modes: Single player (against AI) or double players (great to compete against your friend)

# Demo after being ran on VSCode

> Single player demo

![Demo gif](demo/demo_gif.gif)

# Quick set of rules
* Pieces can only move diagonally.  
* Non-king pieces can only move forward.  
* Black always goes first.  
  
<img src="/demo/black_first.png" width=30%>

> When a piece is clicked, possible move(s) will be indicated. If you click on enemy's pieces, nothing will be shown.

* You can only capture the enemy's piece(s). You cannot jump over your own pieces.  
  
<img src="/demo/black_block.png" width=30%>

* When possible capture(s) available, that's the only move(s) can be made.  
  
<img src="demo/only_move1.png" width=30%> <img src="demo/only_move2.png" width=30%>

* Multiple captures enforced: after 1 capture, if there're more, you must finish them all.  
  
<img src="demo/multi_capture1.png" width=30%> <img src="demo/multi_capture2.png" width=30%>

> Notice how the direction changed to prompt user to continue.

* **King pieces**: When a piece get to the end of enemy's side, it becomes King - it now can move diagonally in 4 directions.  
  
<img src="demo/king_move1.png" width=30%> <img src="demo/king_move2.png" width=30%>

* Game over: Winner will be determined if all enemy's pieces are captured or enemy cannot make any moves. 
   
<img src="demo/game_over.png" width=30%>

### Please let me know if you find any bugs or encounter any issues. I will be very appreciative!