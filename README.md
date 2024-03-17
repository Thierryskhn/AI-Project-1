This game is made in Python (tested with Python 3.9.17) and needs the libraries 'time', 'itertools', 'enum', 'random' and 'abc' to run outside of the project files.

To start the game, the easier way is to go to src/dist/Game and run the Game executable.
If this does not work, run this command in a terminal opened in the main folder of the project (i.e. at the folder which contains src) :
PATH_TO_PYTHON "src/Game.py"
where PATH_TO_PYTHON is the path to your Python executable.

The coordinates to enter when you play are found in the Board.png image:
The third coordinate is found by subtracting the first two : if you want to move a piece to (-2, 3) in Board.png, enter "-2 3 -1" in the terminal (because -(-2)-3 = -1)

If the AI takes too long to play for your liking, you can either modify the constants AI_MIN_TURN_DURATION or CUTOFF in AIPlayer, compile and run. Reducing CUTOFF might have an impact on the AI's quality, but will significantly reduce the time to play.

The players' colors are random. If they are too similar (can happen depending on the terminal, machine & settings), try to close and rerun the game.
