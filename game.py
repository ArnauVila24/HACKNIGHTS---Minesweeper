from logic import Board, GameOver
import time
import pygame
import constants as c

class MinesweeperGame:
    tauler:Board

    def __init__(self, tauler = None):
        if tauler is None:
            tauler = Board()
        self.tauler = tauler
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

    def bomb_exploded(self):
        board = self.tauler.get_board()
        hidden_board = self.tauler.get_hidden_board()
        CELLS_H, CELLS_W = self.tauler.get_size()
        
        for i in range(CELLS_H):
            for j in range(CELLS_W):
                casella = int(board[i][j])         
                if board[i][j] == c.HIDDEN_CELL:
                    casella_img = self.get_img(int(hidden_board[i][j]))
                    display.blit(casella_img, self.get_pixel_coords(j, i)) #vol primer x i després y -> girem j - i 

                    pygame.display.flip() #sense això no es fa la pantalla


    def play(self, display):
        running = True
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("Window closed, quitting game")
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        t1 = time.time()
                        x, y = event.pos
                        i, j = y // c.CELLSIZE_PIXELS, x // c.CELLSIZE_PIXELS
                        print(f"Clicked cell (h= {y // c.CELLSIZE_PIXELS}, w= {x // c.CELLSIZE_PIXELS})")  
                        updated_cells = self.tauler.reveal_cell(i, j)
                        self.paint_cells(updated_cells, display)

                        print(f"Processed move in : {time.time() - t1:.05}s")

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:                        
                        x, y = event.pos
                        i, j = y // c.CELLSIZE_PIXELS, x // c.CELLSIZE_PIXELS

                        print(f"FLAGGED cell (h= {y // c.CELLSIZE_PIXELS}, w= {x // c.CELLSIZE_PIXELS})")  
                        self.flag_cell(updated_cells, display)
                        self.paint_cells(set((i, j)), display)

                        print(f"Processed move in : {time.time() - t1:.05}s")
            except GameOver as e:
                if e.won:
                    print("Displaying Victory Screen...")
                else:
                    self.bomb_exploded()
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