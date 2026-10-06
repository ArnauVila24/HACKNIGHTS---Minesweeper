import numpy as np
import random
import constants as c

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
    board:np.ndarray # Una casella de la board MAI SERÀ FLAG NI HIDDEN
    shown_board:np.ndarray #Una casella de la shown MAI SERÀ BOMBA 

    def __init__(self, w:int = c.DEFAULT_W, h:int = c.DEFAULT_H):
        self.w = w
        self.h = h
        self.size = (h, w) #n files i n columnes
        self.board = self.make_board(w, h)
        self.shown_board = np.array([[c.HIDDEN_CELL for _ in range(w)] for _ in range(h)])

    def get_size(self) -> tuple[int, int]:
        return self.size

    def get_board(self) -> np.ndarray:
        return self.shown_board
    def get_hidden_board(self) -> np.ndarray:
        return self.board

    def place_bomb(self, board:np.ndarray, i:int, j:int):
        h, w = board.shape

        board[i][j] = c.BOMB_CELL
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if 0 <= i+di < h and 0 <= j+dj < w:
                    board[i+di][j+dj] += 1 if board[i+di][j+dj] != c.BOMB_CELL  else 0
                
    def make_board(self, w:int, h:int, perc = 0.15) -> np.ndarray:
        nbombs = int(w*h*0.15)
        board = np.zeros(shape = [h, w])

        placed_bombs = 0
        while placed_bombs < nbombs:
            j, i = random.randint(0, w-1), random.randint(0, h-1)

            if board[i][j] == c.BOMB_CELL: #if bomb torna a buscar posició
                continue
            
            self.place_bomb(board, i, j)
            placed_bombs += 1

        return board

    def hide_cell(self, i:int, j:int):
        """Only for generating the NN dataset"""
        self.board[i][j] = c.HIDDEN_CELL
        return

    def reveal_board(self):
        """For when bomb booms"""
        # TODO
        return

    def reveal_cell(self, i:int, j:int) -> int:
        """La board és privada, està amagada
            Mostrem les caselles i farem show de la shown_board"""
        cella = self.board[i][j]       
        match cella:
            case c.BOMB_CELL:
                self.reveal_board()
                return -1
            case c.EMPTY_CELL:
                for di in range(-1, 2):
                    for dj in range(-1, 2):
                        self.reveal_cell(i+di, j+dj) #revel·la les caselles veïnes
            case a if a < 9:
                self.reveal_cell(i, j)
            case c.OUT_OF_BOUNDS_CELL:
                pass
            case c.HIDDEN_CELL | c.FLAGGED_CELL:
                raise ValueError("Vale això no hauria de passar perquè una casella de la board no pot ser hidden", cella)
            case _:
                raise ValueError("what te fuuuk")
        return 0

def main():
    a = Board()
    # print(a.get_board())
    # print(a.get_hidden_board())
    return

if __name__ == "__main__":
    main()