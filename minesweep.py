import numpy as np
import random
# import torch
# import torch.nn as nn

class Board:
    w:int
    h:int
    board:np.ndarray

    def __init__(self, w:int, h:int):
        self.board = self.make_board(w, h)

    def place_bomb(self, board:np.ndarray, i:int, j:int):
        w, h = board.shape

        board[i][j] = -1
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if 0 <= i+di < w and 0 <= j+dj < h:
                    board[i+di][j+dj] += 1 if board[i+di][j+dj] != -1  else 0
                
    def make_board(self, w:int, h:int, perc = 0.15) -> np.ndarray:
        nbombs = int(w*h*0.15)
        board = np.zeros(shape = [w, h])
        nbombs = 5

        placed_bombs = 0
        while placed_bombs < nbombs:
            i, j = random.randint(0, w-1), random.randint(0, h-1)

            if board[i][j] == -1: #if bomb torna a buscar posició
                continue
            
            self.place_bomb(board, i, j)
            placed_bombs += 1

        print(board)
        return np.zeros(10)

def main():
    a = Board(10, 10)

if __name__ == "__main__":
    main()