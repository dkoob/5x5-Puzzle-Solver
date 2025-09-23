import random
from copy import deepcopy

# ---------- [BEGIN] CONSTANTS [BEGIN] ----------

GAME_PIECES = [
    {"id": 1, "symbols": ["A", "B", "C"], "length": 3, "placed": False, "position": None, "orientation": None, "color": "red"},
    {"id": 2, "symbols": ["A", "B", "D"], "length": 3, "placed": False, "position": None, "orientation": None, "color": "green"},
    {"id": 3, "symbols": ["D", "E", "B"], "length": 3, "placed": False, "position": None, "orientation": None, "color": "blue"},
    {"id": 4, "symbols": ["E", "D", "A"], "length": 3, "placed": False, "position": None, "orientation": None, "color": "yellow"},
    {"id": 6, "symbols": ["C", "E"], "length": 2, "placed": False, "position": None, "orientation": None, "color": "purple"},
    {"id": 5, "symbols": ["E", "B", "D"], "length": 3, "placed": False, "position": None, "orientation": None, "color": "magenta"},
    {"id": 7, "symbols": ["C", "A", "E"], "length": 3, "placed": False, "position": None, "orientation": None, "color": "cyan"},
    {"id": 8, "symbols": ["B", "C", "D"], "length": 3, "placed": False, "position": None, "orientation": None, "color": "bright_orange"},
    {"id": 9, "symbols": ["A", "C"], "length": 2, "placed": False, "position": None, "orientation": None, "color": "pink"},
]

PIECE_COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "purple": "\033[95m",
    "bright_orange": "\033[93m",
    "pink": "\033[96m",
    "reset": "\033[0m",
}

grid_height = 5
grid_width = 5
board = [[None for _ in range(grid_width)] for _ in range(grid_height)]
moves = 0

# ---------- [END] CONSTANTS [END] ----------

# ---------- [BEGIN] FUNCTIONS [BEGIN] ----------

def render_board():
    for row in board:
        for cell in row:
            if cell is None:
                print(" ", end="")
            else:
                piece_id, symbol_index = cell
                piece = next(piece for piece in GAME_PIECES if piece["id"] == piece_id)
                symbol = piece["symbols"][symbol_index]
                if symbol == "A":
                    symbol = " ◉ "
                elif symbol == "B":
                    symbol = " ⬟ "
                elif symbol == "C":
                    symbol = " ▲ "
                elif symbol == "D":
                    symbol = " 𖦹 "
                elif symbol == "E":
                    symbol = " ✡︎ "
                color_code = PIECE_COLORS[piece["color"]]
                print(color_code + symbol + PIECE_COLORS["reset"], end=" ")
        print()

def get_row_symbols(row, pieces_list):
    print(row)
    symbols = []
    for cell in board[row]:
        if cell is not None:
            piece_id, symbol = cell
            piece = next(piece for piece in pieces_list if piece["id"] == piece_id)
            symbols.append(piece["symbols"][symbol])
    return symbols

def get_col_symbols(column, pieces_list):
    symbols = []
    for r in range(grid_height):
        cell = board[r][column]
        if cell is not None:
            piece_id, symbol = cell
            piece = next(piece for piece in pieces_list if piece["id"] == piece_id)
            symbols.append(piece["symbols"][symbol])
    return symbols

def fetch_valid_placements(piece, pieces_list):
    valid_placements = []
    piece_length = piece["length"]

    for i in range(grid_height):
        for j in range(grid_width):
            if j + piece_length <= grid_width:
                valid = True
                for k in range(piece_length):
                    row = i
                    column = j + k
                    if board[row][column] is not None:
                        valid = False
                        break
                    symbol = piece["symbols"][k]
                    if symbol in get_row_symbols(row, pieces_list) or symbol in get_col_symbols(column, pieces_list):
                        valid = False
                        break
                if valid:
                    valid_placements.append({"row": i, "column": j, "orientation": "horizontal"})

            if j + piece_length <= grid_width:
                valid = True
                for k in range(piece_length):
                    row = i
                    column = j + k
                    if board[row][column] is not None:
                        valid = False
                        break
                    symbol = piece["symbols"][piece_length - 1 - k]
                    if symbol in get_row_symbols(row, pieces_list) or symbol in get_col_symbols(column, pieces_list):
                        valid = False
                        break
                if valid:
                    valid_placements.append({"row": i, "column": j, "orientation": "reversed_horizontal"})

            if i + piece_length <= grid_height:
                valid = True
                for k in range(piece_length):
                    row = i + k
                    column = j
                    if board[row][column] is not None:
                        valid = False
                        break
                    symbol = piece["symbols"][k]
                    if symbol in get_row_symbols(row, pieces_list) or symbol in get_col_symbols(column, pieces_list):
                        valid = False
                        break
                if valid:
                    valid_placements.append({"row": i, "column": j, "orientation": "vertical"})

            if i + piece_length <= grid_height:
                valid = True
                for k in range(piece_length):
                    row = i + k
                    column = j
                    if board[row][column] is not None:
                        valid = False
                        break
                    symbol = piece["symbols"][piece_length - 1 - k]
                    if symbol in get_row_symbols(row, pieces_list) or symbol in get_col_symbols(column, pieces_list):
                        valid = False
                        break
                if valid:
                    valid_placements.append({"row": i, "column": j, "orientation": "reversed_vertical"})

    return valid_placements

def place_piece(piece, placement):
    global moves
    if not placement:
        piece["placed"] = False
        return
    row = placement["row"]
    column = placement["column"]
    piece_length = piece["length"]
    orientation = placement["orientation"]

    if orientation == "horizontal":
        for k in range(piece_length):
            board[row][column + k] = (piece["id"], k)
    elif orientation == "reversed_horizontal":
        for k in range(piece_length):
            board[row][column + k] = (piece["id"], piece_length - 1 - k)
    elif orientation == "vertical":
        for k in range(piece_length):
            board[row + k][column] = (piece["id"], k)
    elif orientation == "reversed_vertical":
        for k in range(piece_length):
            board[row + k][column] = (piece["id"], piece_length - 1 - k)

    piece["placed"] = True
    piece["position"] = (row, column)
    piece["orientation"] = orientation
    moves += 1

def remove_piece(piece):
    global moves
    if not piece["placed"]:
        return
    row, column = piece["position"]
    piece_length = piece["length"]
    orientation = piece["orientation"]
    if orientation == "horizontal" or orientation == "reversed_horizontal":
        for k in range(piece_length):
            board[row][column + k] = None
    else:
        for k in range(piece_length):
            board[row + k][column] = None
    piece["placed"] = False
    piece["position"] = None
    piece["orientation"] = None
    moves += 1

def solve_board(pieces_list):
    if all(piece["placed"] for piece in pieces_list):
        return True

    unplaced = [piece for piece in pieces_list if not piece["placed"]]

    piece_placements = [(piece, fetch_valid_placements(piece, pieces_list)) for piece in unplaced]
    piece_placements.sort(key=lambda x: len(x[1]))

    piece, placements = piece_placements[0]

    if not placements:
        return False

    for placement in placements:
        place_piece(piece, placement)
        if solve_board(pieces_list):
            return True
        remove_piece(piece)

    return False

unique_solutions = []
def store_solution(solution):
    global moves
    solution_string = ""
    for row in board:
        for cell in row:
            if cell is None:
                print(" ", end="")
            else:
                piece_id, symbol_index = cell
                piece = next(piece for piece in GAME_PIECES if piece["id"] == piece_id)
                symbol = piece["symbols"][symbol_index]
                solution_string += symbol
    if solution_string not in unique_solutions:
        unique_solutions.append(solution_string)
        render_board()
        print(f"{len(unique_solutions)} unique solutions have been found...")
        print(f"Found a valid solution in: {moves} moves")
        moves = 0

# ---------- [END] FUNCTIONS [END] ----------


# ---------- [BEGIN] GAME START [BEGIN] ----------

while True:
    pieces = deepcopy(GAME_PIECES)
    random.shuffle(pieces)

    board[:] = [[None for _ in range(grid_width)] for _ in range(grid_height)]
    for piece in pieces:
        piece["placed"] = False
        piece["position"] = None
        piece["orientation"] = None


    if solve_board(pieces):
        store_solution(board)
    else:
        print("No solution found")

# ---------- [END] GAME START [END] ----------