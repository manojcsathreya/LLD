from enum import Enum
from typing import List, Optional, Tuple
from collections import deque

class PieceType(Enum):
    X = 1
    O = 2

class PlayingPiece:
    def __init__(self, piece_type: PieceType) -> None:
        self.piece_type = piece_type
    
    def get_piece(self) -> PieceType:
        return self.piece_type

class PlayingPieceX(PlayingPiece):
    def __init__(self) -> None:
        super().__init__(PieceType.X)

class PlayingPieceO(PlayingPiece):
    def __init__(self) -> None:
        super().__init__(PieceType.O)

class Player:
    def __init__(self, name: str, playing_piece: PlayingPiece) -> None:
        self.name = name
        self.playing_piece = playing_piece
    
    def get_name(self) -> str:
        return self.name

    def get_playing_piece(self) -> PlayingPiece:
        return self.playing_piece

class Board:
    def __init__(self, size: int) -> None:
        self.size = size
        self.board: List[List[Optional[PlayingPiece]]] = [[None for _ in range(size)] for _ in range(size)]
    
    def add_piece(self, row: int, col: int, playing_piece: PlayingPiece) -> bool:
        if self.board[row][col] is not None:
            return False
        self.board[row][col] = playing_piece
        return True
    
    def get_free_cells(self) -> List[Tuple[int, int]]:
        free_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is None:
                    free_cells.append((i, j))
        return free_cells

    def print_board(self):
        for i in range(self.size):
            row_display = "| "
            for j in range(self.size):
                if self.board[i][j] is not None:
                    row_display += f"{self.board[i][j].get_piece().name} | "
                else:
                    row_display += "   | "
            print(row_display)
            print("-" * (self.size * 4))  # Divider line between rows

class Game:
    def __init__(self) -> None:
        self.q = deque()
        self.size = 3
        self.playing_board = None
    
    def initialize_game(self):
        player1 = Player("ABC", PlayingPieceX())
        player2 = Player("XYZ", PlayingPieceO())
        self.q.append(player2)
        self.q.append(player1)
        self.playing_board = Board(3)
    
    def start_game(self):
        self.initialize_game()
        while True:
            player = self.q.popleft()
            self.playing_board.print_board()
            free_cells = self.playing_board.get_free_cells()
            if not free_cells:
                print("It's a tie!")
                break
            r, c = map(int, input("Enter row and col: ").split())
            if not self.playing_board.add_piece(r, c, player.get_playing_piece()):
                print("Incorrect Position. Try again.")
                self.q.appendleft(player)
                continue
            self.q.append(player)
            if self.is_there_a_winner(r, c, player.get_playing_piece()):
                print(f"Player {player.get_name()} wins!")
                self.playing_board.print_board()
                return
        print("Game Over. No winner.")

    def is_there_a_winner(self, row: int, col: int, playing_piece: PlayingPiece) -> bool:
        piece_type = playing_piece.get_piece()
        
        # Check the row
        if all(self.playing_board.board[row][i] is not None and self.playing_board.board[row][i].get_piece() == piece_type for i in range(self.size)):
            return True

        # Check the column
        if all(self.playing_board.board[i][col] is not None and self.playing_board.board[i][col].get_piece() == piece_type for i in range(self.size)):
            return True

        # Check the main diagonal
        if row == col and all(self.playing_board.board[i][i] is not None and self.playing_board.board[i][i].get_piece() == piece_type for i in range(self.size)):
            return True

        # Check the anti-diagonal
        if row + col == self.size - 1 and all(self.playing_board.board[i][self.size - 1 - i] is not None and self.playing_board.board[i][self.size - 1 - i].get_piece() == piece_type for i in range(self.size)):
            return True

        return False

if __name__ == "__main__":
    game = Game()
    game.initialize_game()
    game.start_game()