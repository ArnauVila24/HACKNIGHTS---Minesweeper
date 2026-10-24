from logic import Board, GameOver
import time
import pygame
import constants as c
from pathlib import Path
import numpy as np

# Action targets
REVEAL, FLAG, CHORD = 0, 1, 2

class ClickLogger:
    def __init__(self, radius: int = 2):
        self.radius = radius                
        self.windows: list[np.ndarray] = []
        self.actions: list[int] = []
        self.game_ids: list[int] = []
        self.game_id = 0

    def new_game(self) -> None:
        self.game_id += 1

    def log_click(self, shown_board, i: int, j: int, action: int) -> None:
        """Guarda la finestra 5x5 centrada a (i, j) i l'acció feta.
        Cal cridar-la ABANS d'aplicar l'acció, perquè la finestra mostri
        el que veia el jugador."""
        board = np.asarray(shown_board)
        radius = self.radius
        size = 2 * radius + 1
        rows, cols = board.shape[:2]
        win = np.full((size, size) + board.shape[2:], -2, dtype=board.dtype)

        # Overlap between the window and the board, in board coordinates
        r0, r1 = max(i - radius, 0), min(i + radius + 1, rows)
        c0, c1 = max(j - radius, 0), min(j + radius + 1, cols)

        # Same overlap, in window coordinates
        wr0, wc0 = r0 - (i - radius), c0 - (j - radius)

        win[wr0 : wr0 + (r1 - r0), wc0 : wc0 + (c1 - c0)] = board[r0:r1, c0:c1]
        
        self.windows.append(win)
        self.actions.append(action)
        self.game_ids.append(self.game_id)

        print("logged:\n", win)
        print("decision:", action)

    def save(self, path: str | Path) -> None:
        if not self.windows:
            return
        np.savez_compressed(
            path + f"_{len(self.actions)}.npz",
            X=np.stack(self.windows),                    # (N, 5, 5) int8
            y=np.array(self.actions, dtype=np.int8),     # (N,)
            game_id=np.array(self.game_ids, dtype=np.int32),
        )

    def clear(self) -> None:
        self.windows.clear(); self.actions.clear(); self.game_ids.clear()


def merge_datasets(folder: str | Path, out_path: str | Path) -> None:
    """Combina tots els .npz d'una carpeta en un sol dataset."""
    Xs, ys, gids, offset = [], [], [], 0
    for f in sorted(Path(folder).glob("*.npz")):
        d = np.load(f)
        Xs.append(d["X"]); ys.append(d["y"])
        gids.append(d["game_id"] + offset)               # keep game ids unique
        offset = gids[-1].max() + 1
    np.savez_compressed(out_path, X=np.concatenate(Xs), y=np.concatenate(ys),
                        game_id=np.concatenate(gids))

class MinesweeperGame:
    tauler:Board
    logger:ClickLogger
    def __init__(self, tauler = None):
        if tauler is None:
            tauler = Board()
        self.tauler = tauler
        self.logger = ClickLogger()
        return

    def init_board(self) -> pygame.display:
        tauler_inicial = self.tauler.get_board()

        CELLS_H, CELLS_W = self.tauler.get_size()

        WINDOW_W = c.CELLSIZE_PIXELS * CELLS_W
        WINDOW_H = c.CELLSIZE_PIXELS * CELLS_H

        display = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("Demo")

        fons = pygame.image.load("images/background.png")
        
        #setup icones

        casella_img = self.get_img(c.HIDDEN_CELL)           #evitar carregar molts cops la img, és tot hidden
        for i in range(CELLS_H):
            for j in range(CELLS_W):

                display.blit(casella_img, self.get_pixel_coords(j, i)) #vol primer x i després y -> girem j - i 

        pygame.display.flip() #sense això no es fa la pantalla
        return display

    def get_pixel_coords(self, i, j):
        return c.CELLSIZE_PIXELS*i, c.CELLSIZE_PIXELS*j

    def get_img(self, celltype) -> pygame.image:
        """Loads the image and returns it"""
        number_cells = [pygame.image.load(f"images/{i}_cell.png") for i in range(1, 7)]
        img_bomba = pygame.image.load("images/bomb_cell.png")
        img_empty = pygame.image.load("images/cleared_cell.png")
        img_flag = pygame.image.load("images/flagged_cell.png")
        img_hidden = pygame.image.load("images/hidden_cell.png")

        match celltype:
            case c.BOMB_CELL:
                img = img_bomba
            case c.EMPTY_CELL:
                img = img_empty
            case n if n in [1, 2, 3, 4, 5, 6, 7, 8]:
                img = number_cells[celltype -1] 
            case c.FLAGGED_CELL:
                img = img_flag
            case c.HIDDEN_CELL:
                img = img_hidden
            case _:
                raise ValueError("wht the fuuu")
        return img

    def paint_cells(self, updated_cells:set[tuple[int, int]], display:pygame.display) -> None:
        """Paints multiple cells at once, LOADS once"""

        number_cells = [pygame.image.load(f"images/{i}_cell.png") for i in range(1, 7)]
        img_bomba = pygame.image.load("images/bomb_cell.png")
        img_empty = pygame.image.load("images/cleared_cell.png")
        img_flag = pygame.image.load("images/flagged_cell.png")
        img_hidden = pygame.image.load("images/hidden_cell.png")

        for i, j in updated_cells:
            celltype = self.tauler.get_cell(i, j)     
            match celltype:
                case c.BOMB_CELL:
                    img = img_bomba
                case c.EMPTY_CELL:
                    img = img_empty
                case n if n in [1, 2, 3, 4, 5, 6, 7, 8]:
                    img = number_cells[celltype -1] 
                case c.FLAGGED_CELL:
                    img = img_flag
                case c.HIDDEN_CELL:
                    img = img_hidden
                case _:
                    raise ValueError("wht the fuuu")
            display.blit(img, self.get_pixel_coords(j, i)) # again, fem swap i <-> j
        pygame.display.flip()
        return 

    def flag_cell(self, i:int, j:int, display):        
        
        self.tauler.shown_board[i][j] = c.FLAGGED_CELL
        flag = self.get_img(c.FLAGGED_CELL)
        display.blit(flag, self.get_pixel_coords(j, i))
        pygame.display.flip()


    def bomb_exploded(self, display:pygame.display):
        board = self.tauler.get_board()
        hidden_board = self.tauler.get_hidden_board()
        CELLS_H, CELLS_W = self.tauler.get_size()
        celles = set()

        for i in range(CELLS_H):
            for j in range(CELLS_W):
                casella = int(board[i][j])         
                if board[i][j] == c.HIDDEN_CELL:
                    celles.add((i, j))
        self.paint_cells(celles, display)
        gat = pygame.image.load("images/gat.png")
        display.blit(gat, (0, 0))
        pygame.display.flip()
        a=True
        while a:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return

    def play(self, display):
        running = True
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("Window closed, quitting game")
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        #clic esq
                        x, y = event.pos
                        i, j = y // c.CELLSIZE_PIXELS, x // c.CELLSIZE_PIXELS

                        if 1 <= self.tauler.shown_board[i][j] <= 8:
                            self.logger.log_click(self.tauler.get_board(), i, j, CHORD)
                            updated_cells = self.tauler.chord(i, j)
                        else:
                            self.logger.log_click(self.tauler.get_board(), i, j, REVEAL)
                            updated_cells = self.tauler.reveal_cell(i, j)

                        self.paint_cells(updated_cells, display)

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:     
                        #clic dret             
                        x, y = event.pos
                        i, j = y // c.CELLSIZE_PIXELS, x // c.CELLSIZE_PIXELS
                        self.logger.log_click(self.tauler.get_board(), i, j, FLAG)

                        print(f"FLAGGED cell (h= {y // c.CELLSIZE_PIXELS}, w= {x // c.CELLSIZE_PIXELS})")  
                        self.flag_cell(i, j, display)

            except GameOver as e:
                self.logger.save(f"data/game_{int(time.time())}")
                self.logger.clear()
                if e.won:
                    print("Displaying Victory Screen...")
                else:
                    self.bomb_exploded(display)
                running = False   
        pygame.quit()
        return

def main():
    game = MinesweeperGame()
    for a in game.tauler.get_hidden_board():
        print(a)

    display = game.init_board()
    game.play(display)
    return

if __name__ == "__main__":
    main()