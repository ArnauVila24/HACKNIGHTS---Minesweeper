import random
import time
import constants as c
from collections import deque

type BoardType = list[list[int]]


class GameOver(Exception):
    def __init__(self, message="Game Over!", won=False):
        super().__init__(message)
        self.won = won

class Board:
    """
    -2: Amagada
    -1: Bomba
    0: Descoberta
    1-8: numero
    """
    w:int
    h:int
    size:tuple[int, int]
    _board:BoardType # Una casella de la board MAI SERÀ FLAG NI HIDDEN
    shown_board:BoardType #Una casella de la shown MAI SERÀ BOMBA 

    def __init__(self, w:int = c.DEFAULT_W, h:int = c.DEFAULT_H):
        self.w = w
        self.h = h
        self.size = (h, w) #n files i n columnes
        self.board = self.make_board(w, h)
        self.shown_board = [[c.HIDDEN_CELL for _ in range(w)] for _ in range(h)]

    def get_size(self) -> tuple[int, int]:
        return self.size

    def get_cell(self, i, j) -> int:
        """Returns the HIDDEN cell in position i, j"""
        return int(self.board[i][j])

    def get_board(self) -> BoardType:
        return self.shown_board
    def get_hidden_board(self) -> BoardType:
        return self.board

    def place_bomb(self, board:BoardType, i:int, j:int):
        h, w = len(board), len(board[0])

        board[i][j] = c.BOMB_CELL
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if 0 <= i+di < h and 0 <= j+dj < w:
                    board[i+di][j+dj] += 1 if board[i+di][j+dj] != c.BOMB_CELL  else 0
                
    def make_board(self, w:int, h:int, perc = 0.15) -> BoardType:
        nbombs = int(w*h*0.15)
        board = [[0 for _ in range(w)] for _ in range(h)]                

        random.seed(1234)
        placed_bombs = 0
        while placed_bombs < nbombs:
            i, j = random.randint(0, h-1), random.randint(0, w-1)

            if board[i][j] == c.BOMB_CELL: #if bomb torna a buscar posició
                continue
            
            self.place_bomb(board, i, j)
            placed_bombs += 1

        return board

    def hide_cell(self, i:int, j:int):
        """Only for generating the NN dataset"""
        self.board[i][j] = c.HIDDEN_CELL
        return

    def reveal_cell(self, i:int, j:int, show_q:set[tuple[int, int]] | None = None) -> set[tuple[int, int]]:
        """Retorna conjunt de celles que s'han de mostrar al revelar la cella (i, j)        
            La board és privada, està amagada
            Mostrem les caselles i farem show de la shown_board"""
        if show_q is None:
            show_q = set()
        if (i, j) in show_q:
            return set()

        if not (0 <= i <= self.h-1 and 0 <= j <= self.w-1):
            return show_q

        if self.shown_board[i][j] == c.FLAGGED_CELL:
            return show_q

        
        show_q.add((i, j))
        cella = self.get_cell(i, j)
        match cella:
            case c.BOMB_CELL:
                raise GameOver
            case c.EMPTY_CELL:
                self.shown_board[i][j] = cella 
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        self.reveal_cell(i+di, j+dj, show_q) #revel·la les caselles veïnes

            case a if 1 <= a <= 8:
                self.shown_board[i][j] = cella
            case c.OUT_OF_BOUNDS_CELL:
                pass
            case c.HIDDEN_CELL | c.FLAGGED_CELL:
                raise ValueError("Vale això no hauria de passar perquè una casella de la board no pot ser hidden", cella)
            case _:
                raise ValueError("what te fuuuk")
        return show_q

    def chord(self, i: int, j: int) -> set[tuple[int, int]]:
        """Si la casella (i, j) és un número amb tantes banderes al voltant
        com indica, revela els veïns que continuen amagats."""
        if not (0 <= i <= self.h-1 and 0 <= j <= self.w-1):
            return set()

        value = self.shown_board[i][j]
        if not (1 <= value <= 8): # only works on revealed numbers
            return set()

        neighbors = [
            (i+di, j+dj)
            for di in range(-1, 2)
            for dj in range(-1, 2)
            if (di, dj) != (0, 0)
            and 0 <= i+di <= self.h-1
            and 0 <= j+dj <= self.w-1
        ]

        flags = sum(self.shown_board[ni][nj] == c.FLAGGED_CELL for ni, nj in neighbors)
        if flags != value:
            return set()

        show_q = set()
        for ni, nj in neighbors:
            if self.shown_board[ni][nj] == c.HIDDEN_CELL:
                self.reveal_cell(ni, nj, show_q)
        return show_q

def main():
    a = Board()
    # print(a.get_board())
    # print(a.get_hidden_board())
    return

if __name__ == "__main__":
    main()