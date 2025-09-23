# 5x5-Puzzle-Solver

### How this puzzle works
This puzzle consists of 9 pieces, 7 3x1 tiles and 2 2x1 tiles, each with 2 or 3 of 5 total unique symbols.
The goal is to arrange these pieces on a 5x5 board without having any duplicate symbols in the rows or columns.
This solver is able to find all valid solutions relatively quickly.

**The current max amount of unique solutions I've found is 7.**

### Code Explanation
The code may look a bit more complicated than it actually is, so here is a general explanation of how everything works.

### [ ---------- Constants ---------- ]
At the top of the script, I define some constants and create a dictionary (an object in Python that is 
able to store data keys and their values) for each unique shape. This dictionary holds all of the values that 
The solver will need, including: a unique ID for each shape, the symbols or, in this case, letters corresponding to each symbol 
because they look nicer in the command console, the length of each shape, and a True or False value for their placement status, 
a tuple (another simple data structure) with their position as a column/row form, their orientation, and a pretty color to display them in.
The next constants are the complex template strings for the colors (these are called ANSI codes and are used to format terminal/console text), and 
some basic constants to set up the game board. The line that says:
```python
board = [[None for _ in range(grid_width)] for _ in range(grid_height)]
```
creates the initial game board that looks something like this to the computer:
> None None None None None  
> None None None None None  
> None None None None None  
> None None None None None  

This allows me  to have a base object for the game board with initial values that I can check before trying to place a piece. If any of the cells that the piece would be placed on **ARE NOT** "None", then the placement would not be valid for that piece.

### [ ---------- Functions ---------- ]  
The next big section is where all of the functions live. I'll go in order of each function as they are called in the script and explain exactly how they work.  

- **solve_board(pieces_list)** << Line 196
  - This is the main logic handling command for the script, it is responsible for handling solved board cases (returning True when all cells on the board are filled, which tells the global game loop to pause and recognize a solution), keeping track of all unplaced pieces, grabbing all possible positions a piece can be placed, and sorting all
  available pieces by which one has the least amount of valid placements (MRV, or minimum remaining variables heuristic, which is a technique of sorting our variables to find the most constrained one and beginning with that to minimize the amount of backtracking we have to do to find a valid solution), and handling the backtracking system.
- **fetch_valid_placements(piece, pieces_list)** << Line 82
  - This function is by far the most complicated of the script; it is responsible for checking pieces in all 4 orientations to determine whether they can both be placed without entering an occupied or overhanging cell, and whether any of their symbols are duplicates in their respective row/columns.
  This function takes the piece and loops through each cell on the board, checking for the cases mentioned above, and if all of them pass, it saves the position and orientation as a valid placement for the piece in a list. It then does this 3 more times for each 90-degree rotation, horizontally and vertically. 
  - This function uses 2 smaller sub-functions called get_row_symbols and get_col_symbols, which just return all currently placed symbols on the current row and column of the piece being checked. Pretty straightforward, these functions take a row/column index and loop through it, saving each symbol in a list and returning it at the end.
- **place_piece(piece, placement)** << Line 151
  - Once a list of valid positions has been found for a piece, we then need to actually get it on the board. This function just takes the piece's length, the starting position of its placement, and the orientation it will go in, and updates the 'None None None' board structure with the piece's ID and symbol index instead. It then updates the 
  pieces placed, position, and orientation variables in the piece dictionary, increases the rolling count for total moves, and moves onto the next piece.
- **remove_piece(piece)** << Line 179
  - This function is VERY important for the backtracking method I used with this solver. The way it works is fairly straightforward, but it allows us to remove a piece and revert to the previous board when we can determine that a placement will lead to a failed solution. This is determined when checking the valid placements for the next piece, if there
  are no valid solutions, we remove the piece we just placed and try a different placement or piece.
- **store_solution(solution)** << Line 220
  - Once we have found a unique solution, we want to move on to the next one to find as many valid solutions as possible. This function takes the board, removes all of the spaces and formatting, and just saves each symbol as one big string (ex, if the board was A B C E D, new line E C A D B, the function turns it into ABCEDECADB and saves it). This way, whenever we find
  the next solution, we can check if its already been saved, and if so, ignore it and keep looking. 
- **render_board()** << Line 40
    - Finally is rendering the solutions. This function combines the ANSI color code constant with the symbols and solved board to make a nice-looking display in the console. It is also able to swap between displaying the symbols as letters from A to E and as accurate symbols as I could find in text, to the actual puzzle.

### [ ---------- Game Start ---------- ]  
At the bottom of the script are a couple of lines of code that are actually responsible for initiating and running the solver. This line has a "while True" loop, which was a fairly lazy choice on my part, but it essentially will just run the script forever until it is stopped. Inside of this loop, we create a copy of all of the game pieces, shuffle them to begin with a random one,
initiate a new blank board, reset all of the pieces to their default values, and then run the solve_board command and see how far we get.

That's basically it. Fairly simple and straightforward. I have not been able to come up with a confident estimate of the number of unique arrangements of pieces you can have for this puzzle, but my guess is somewhere over the 1 quadrillion mark. So a brute force strategy would probably not be as possible as I initially imagined. You basically have to have some degree
of backtracking and position checking optimization to have any realistic chance of solving this puzzle as a machine, as computers are missing the logical skills that humans have in identifying failed solutions early.

### Running this script without proper software
If you would like to run this script yourself without downloading anything or setting up any coding environments, you can copy all of the code from the [main.py file](main.py) and paste it into this website, [Programiz Online IDE](https://www.programiz.com/python-programming/online-compiler/), and click run!
