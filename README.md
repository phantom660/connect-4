# Connect 4

Python implementation of the classic game [Connect 4](https://en.wikipedia.org/wiki/Connect_Four)

## Game Details

This is a two person game. Player 1 is red and Player 2 is yellow. The turn will alternate automatically after a piece is successfully placed. Once the game is over, players can select to play again.

## Implementation Details
- numpy is used to represent the grid that pieces can be dropped into
- pygame is used for the main interface. Pieces are placed by simply clicking on the desired column. 
- Tkinter is used solely for the "play again?" messagebox prompt that appears when the game has reached the end (i.e. someone has four pieces in a row or the game board is full with no winner).

## Inspiration
I took some inspiration for this project from [this](https://www.youtube.com/playlist?list=PLFCB5Dp81iNV_inzM-R9AKkZZlePCZdtV) video series by Keith Galli
