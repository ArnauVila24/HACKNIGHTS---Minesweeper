import numpy as np
import random
from constants import *
# import torch
# import torch.nn as nn

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
    board:np.ndarray

    def __init__(self, w:int, h:int):
        self.w = w
        self.h = h
        self.size = (w, h)
        self.board = self.make_board(w, h)

    def get_size(self) -> tuple[int, int]:
        return self.size

    def get_board(self) -> np.ndarray:
        return self.board

    def place_bomb(self, board:np.ndarray, i:int, j:int):
        w, h = board.shape

        board[i][j] = BOMB_CELL
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if 0 <= i+di < w and 0 <= j+dj < h:
                    board[i+di][j+dj] += 1 if board[i+di][j+dj] != BOMB_CELL  else 0
                
    def make_board(self, w:int, h:int, perc = 0.15) -> np.ndarray:
        nbombs = int(w*h*0.15)
        board = np.zeros(shape = [w, h])

        placed_bombs = 0
        while placed_bombs < nbombs:
            i, j = random.randint(0, w-1), random.randint(0, h-1)

            if board[i][j] == BOMB_CELL: #if bomb torna a buscar posició
                continue
            
            self.place_bomb(board, i, j)
            placed_bombs += 1

        return board

    def hide_cell(self, i:int, j:int):
        self.board[i][j] = HIDDEN_CELL
        return

def main():
    a = Board(10, 10)
    print(a.get_board())
    return

if __name__ == "__main__":
    main()