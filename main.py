import random

# tried my best to get accurate symbols
GAME_PIECES_TEST = [
    {"id": 1, "symbols": ["◉", "⬟", "▲"], "length": 3, "placed": False, "position": None, "orientation": None, "color": "red"},
    {"id": 2, "symbols": ["◉", "⬟", "𖦹"], "length": 3, "placed": False, "position": None, "orientation": None, "color": "green"},
    {"id": 3, "symbols": ["𖦹", "✡︎", "⬟"], "length": 3, "placed": False, "position": None, "orientation": None, "color": "blue"},
    {"id": 4, "symbols": ["✡︎", "𖦹", "◉"], "length": 3, "placed": False, "position": None, "orientation": None, "color": "yellow"},
    {"id": 5, "symbols": ["✡︎", "⬟", "𖦹"], "length": 3, "placed": False, "position": None, "orientation": None, "color": "magenta"},
    {"id": 7, "symbols": ["▲", "◉", "✡︎"], "length": 3, "placed": False, "position": None, "orientation": None, "color": "cyan"},
    {"id": 8, "symbols": ["⬟", "▲", "𖦹"], "length": 3, "placed": False, "position": None, "orientation": None, "color": "bright_orange"},
    {"id": 9, "symbols": ["◉", "▲"], "length": 2, "placed": False, "position": None, "orientation": None, "color": "pink"},
    {"id": 6, "symbols": ["▲", "✡︎"], "length": 2, "placed": False, "position": None, "orientation": None, "color": "purple"},
]

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


# just defines the grid size and an empty data structure for the board
grid_height = 5
grid_width = 5
board = [[None for _ in range(grid_width)] for _ in range(grid_height)]

def render_board():
    for row in board:
        for cell in row:
            if cell is None:
                print("  ", end="")
            else:
                piece_id, symbol_index = cell
                piece = next(p for p in GAME_PIECES if p["id"] == piece_id)
                symbol = piece["symbols"][symbol_index]
                color_code = PIECE_COLORS[piece["color"]]
                print(color_code + symbol + PIECE_COLORS["reset"], end=" ")
        print()

def get_board_symbols(board_data):
    existing_symbols = []
    for cell in board_data:
        if cell is not None:
            piece_id, symbol_index = cell
            piece = next(p for p in GAME_PIECES if p["id"] == piece_id)
            existing_symbols.append(piece["symbols"][symbol_index])
    return existing_symbols


def fetch_valid_placements(piece):
    valid_placements = []

    for i in range(grid_height):
        for j in range(grid_width):

            if piece["length"] + j <= grid_width:
                forward_ok = True
                backward_ok = True

                row_symbols = get_board_symbols(board[i])
                col_symbols = get_board_symbols([board[r][j] for r in range(grid_height)])

                for k in range(piece["length"]):
                    f_symbol = piece["symbols"][k]
                    b_symbol = piece["symbols"][piece["length"] - 1 - k]

                    cell = board[i][j + k]
                    if cell is not None or f_symbol in row_symbols or f_symbol in col_symbols:
                        forward_ok = False
                    if cell is not None or b_symbol in row_symbols or b_symbol in col_symbols:
                        backward_ok = False
                if forward_ok:
                    valid_placements.append({"row": i, "col": j, "orientation": "horizontal"})
                if backward_ok:
                    valid_placements.append({"row": i, "col": j, "orientation": "reversed_horizontal"})

            if piece["length"] + i <= grid_height:
                forward_ok = True
                backward_ok = True

                row_symbols = get_board_symbols(board[i])
                col_symbols = get_board_symbols([board[r][j] for r in range(grid_height)])

                for k in range(piece["length"]):
                    f_symbol = piece["symbols"][k]
                    b_symbol = piece["symbols"][piece["length"] - 1 - k]

                    cell = board[i + k][j]
                    if cell is not None or f_symbol in row_symbols or f_symbol in col_symbols:
                        forward_ok = False
                    if cell is not None or b_symbol in row_symbols or b_symbol in col_symbols:
                        backward_ok = False
                if forward_ok:
                    valid_placements.append({"row": i, "col": j, "orientation": "vertical"})
                if backward_ok:
                    valid_placements.append({"row": i, "col": j, "orientation": "reversed_vertical"})

    return valid_placements

def place_piece(piece, valid_locations):
    if not valid_locations:
        piece["placed"] = "Invalid"
        return

    placement = random.choice(valid_locations)
    row = placement["row"]
    col = placement["col"]
    if placement["orientation"] == "horizontal":
        for k in range(piece["length"]):
            board[row][col + k] = (piece["id"], k)
    elif placement["orientation"] == "reversed_horizontal":
        for k in range(piece["length"]):
            board[row][col + k] = (piece["id"], piece["length"] - 1 - k)
    elif placement["orientation"] == "vertical":
        for k in range(piece["length"]):
            board[row + k][col] = (piece["id"], k)
    elif placement["orientation"] == "reversed_vertical":
        for k in range(piece["length"]):
            board[row + k][col] = (piece["id"], piece["length"] - 1 - k)

    piece["placed"] = True
    piece["position"] = (row, col)
    piece["orientation"] = placement["orientation"]

def solve_board(pieces, board):
    if all(piece["placed"] for piece in pieces):
        return True

    unplaced = [p for p in pieces if not p["placed"]]
    piece_placements = [(p, fetch_valid_placements(p)) for p in unplaced]
    piece_placements.sort(key=lambda x: len(x[1]))

    piece, placements = piece_placements[0]

    for placement in placements:
        # print(f"Trying piece {piece['id']} at {placement}")
        place_piece(piece, [placement])
        if solve_board(pieces, board):
            return True

        remove_piece(piece)

    return False

def remove_piece(piece):
    """Remove a piece from the board."""
    row, col = piece["position"]
    length = piece["length"]
    orientation = piece["orientation"]

    if orientation == "horizontal":
        for k in range(length):
            board[row][col + k] = None
    elif orientation == "reversed_horizontal":
        for k in range(length):
            board[row][col + k] = None
    elif orientation == "vertical":
        for k in range(length):
            board[row + k][col] = None
    elif orientation == "reversed_vertical":
        for k in range(length):
            board[row + k][col] = None

    piece["placed"] = False
    piece["position"] = None
    piece["orientation"] = None

# Usage
pieces = GAME_PIECES.copy()
random.shuffle(pieces)  # Optional

for piece in GAME_PIECES:
    piece["placed"] = False
    piece["position"] = None
    piece["orientation"] = None

while True:
    if solve_board(GAME_PIECES, board):
        render_board()
        exit()
    else:
        print("No solution found")

# def handle_game():
#     global board
#     success = False
#
#     while not success:
#
#         board = [[None for _ in range(grid_width)] for _ in range(grid_height)]
#         pieces = GAME_PIECES.copy()
#         random.shuffle(pieces)
#         invalid_placements = 0
#
#         for piece in pieces:
#             piece["placed"] = False
#             piece["position"] = None
#             piece["orientation"] = None
#
#         for piece in pieces:
#             while piece["placed"] is False:
#                 placements = fetch_valid_placements(piece)
#                 place_piece(piece, placements)
#                 if piece["placed"] == "Invalid":
#                     invalid_placements += 1
#                     break
#
#         if invalid_placements == 0:
#             success = True
#
#     render_board()

# handle_game()