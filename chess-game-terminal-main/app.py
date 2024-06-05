class ChessGame:
    def __init__(self):
        self.board = [
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["r", "n", "b", "q", "k", "b", "n", "r"],
        ]
        self.current_player = "white"
        self.move_history = []
 
    def print_board(self):
        print("   a b c d e f g h")
        print("  -----------------")
        for i in range(8):
            print(f"{8 - i}| {' '.join(self.board[i])} |")
        print("  -----------------")
 
    def convert_move(self, move):
        col1, row1, col2, row2 = move
        if (
            col1 < "a"
            or col1 > "h"
            or col2 < "a"
            or col2 > "h"
            or row1 < 1
            or row1 > 8
            or row2 < 1
            or row2 > 8
        ):
            return None
        return 8 - row1, ord(col1) - ord("a"), 8 - row2, ord(col2) - ord("a")
 
    def make_move(self, move):
        i1, j1, i2, j2 = move
        piece = self.board[i1][j1]
        if piece == " ":
            print("Invalid move: No piece at the starting position.")
            return False
        elif (piece.islower() and self.current_player == "white") or (
            piece.isupper() and self.current_player == "black"
        ):
            print("Invalid move: It's not your turn.")
            return False
        elif not self.is_valid_move(i1, j1, i2, j2):
            print("Invalid move: Piece cannot move that way.")
            return False
        self.move_history.append(
            (self.board[i2][j2], i2, j2, piece, i1, j1, self.current_player)
        )
        self.board[i2][j2] = piece
        self.board[i1][j1] = " "
        self.current_player = "black" if self.current_player == "white" else "white"
        return True
 
    def undo_move(self):
        if not self.move_history:
            print("No move to undo.")
            return False
        last_move = self.move_history.pop()
        captured_piece, i2, j2, piece, i1, j1, prev_player = last_move
        self.board[i1][j1] = piece
        self.board[i2][j2] = captured_piece
        self.current_player = prev_player
        return True
 
    def is_valid_move(self, i1, j1, i2, j2):
        piece = self.board[i1][j1].lower()
        if piece == "p":
            if j1 == j2 and self.board[i2][j2] == " ":
                if abs(i2 - i1) == 1:
                    return True
                elif abs(i2 - i1) == 2 and (
                    (i1 == 6 and self.board[5][j1] == " ")
                    or (i1 == 1 and self.board[2][j1] == " ")
                ):
                    return True
            elif abs(j1 - j2) == 1 and self.board[i2][j2] != " ":
                if (
                    i2 - i1 == 1
                    and piece.islower()
                    or i2 - i1 == -1
                    and piece.isupper()
                ):
                    return True
        elif piece == "r":
            if i1 == i2:
                return self.is_clear_horizontal(i1, j1, j2)
            elif j1 == j2:
                return self.is_clear_vertical(j1, i1, i2)
        elif piece == "n":
            return (abs(i1 - i2) == 2 and abs(j1 - j2) == 1) or (
                abs(i1 - i2) == 1 and abs(j1 - j2) == 2
            )
        elif piece == "b":
            return self.is_clear_diagonal(i1, j1, i2, j2)
        elif piece == "q":
            return (
                (i1 == i2 and self.is_clear_horizontal(i1, j1, j2))
                or (j1 == j2 and self.is_clear_vertical(j1, i1, i2))
                or self.is_clear_diagonal(i1, j1, i2, j2)
            )
        elif piece == "k":
            return abs(i1 - i2) <= 1 and abs(j1 - j2) <= 1
        return False
 
    def is_clear_horizontal(self, i, j1, j2):
        step = 1 if j2 > j1 else -1
        for j in range(j1 + step, j2, step):
            if self.board[i][j] != " ":
                return False
        return True
 
    def is_clear_vertical(self, j, i1, i2):
        step = 1 if i2 > i1 else -1
        for i in range(i1 + step, i2, step):
            if self.board[i][j] != " ":
                return False
        return True
 
    def is_clear_diagonal(self, i1, j1, i2, j2):
        step_i = 1 if i2 > i1 else -1
        step_j = 1 if j2 > j1 else -1
        i, j = i1 + step_i, j1 + step_j
        while i != i2 and j != j2:
            if self.board[i][j] != " ":
                return False
            i += step_i
            j += step_j
        return True
 
    def start(self):
        print(
            "Enter moves in algebraic notation (e.g., e2e4). Enter 'undo' to undo the last move."
        )
        while True:
            self.print_board()
            move = input(f"Enter your move, {self.current_player.capitalize()}: ")
            if move == "undo":
                self.undo_move()
                continue
            if len(move) != 4:
                print("Invalid move: Enter two positions (e.g., e2e4).")
                continue
            move = move.lower()
            if not move[0].isalpha() or not move[2].isalpha():
                print("Invalid move: Enter valid column characters (a-h).")
                continue
            move = (move[0], int(move[1]), move[2], int(move[3]))
            move = self.convert_move(move)
            if move is None:
                print("Invalid move: Enter valid row numbers (1-8).")
                continue
            if not self.make_move(move):
                continue
 
 
if __name__ == "__main__":
    game = ChessGame()
    game.start()