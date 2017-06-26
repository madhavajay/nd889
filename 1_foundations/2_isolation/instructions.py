def show_instructions() -> str:
    print("\n")
    print("Instructions:")
    print("----------")
    print("\n  Board: The Isolation game board is a grid of rows and columns. \
           \n  Moves: Only L-Shaped moves are permitted (similar to knight in the game of Chess) and are depicted \
           \n    on the board as possible legal moves. \
           \n  Positions: Each positions on the board is represented as a tuple comprising its row and column in the grid. \
           \n  Exiting game: Press CTRL+C or enter q followed by Enter key. \
           \n  Players: The players are Player 1 (Green) and Player 2 (Red). \
           \n  Player Turns: Players take turns. On each turn of the Human player, they are prompted with a list of \
           \n    possible legal positions they may move to from their current position. The list option are represented \
           \n    as indexes. For example, given the following prompt (i.e. [0] (4, 3)	[1] (4, 5)) means there are \
           \n    two possible legal positions (that are on the board and have not been previously occupied) that the Human player \
           \n    may move to, which includes row 4 column 3 that may be chosen by entering index 0 and pressing Enter, or row 4 column 5 \
           \n    that may be chosen by entering index 1 and pressing Enter. \
           \n  Player current positions: \
           \n    |  1  (Green-coloured)   | - Represents current position of Player 1 (i.e. Human) \
           \n    |  2  (Red-coloured)     | - Represents current position of Player 2 (i.e. Computer AB_Custom) \
           \n  Player possible legal moves: \
           \n    | Box (Green-coloured)   | - Represents possible move(s) available to Player 1 on their turn \
           \n    | Box (Red-coloured)     | - Represents possible moves(s) available to Player 2 on their turn \
           \n    | Box (Blue-coloured)    | - Represents possible move(s) available to both Player 1 and Player 2 (but only one player may occupy any single grid element) \
           \n    |  -  (Dash)             | - Represents blocked positions no longer available (since previously occupied by either Player 1 or Player 2) \
           \n \
         ")