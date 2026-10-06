from logic import Board, GameOver
import pygame
import constants as c

class MinesweeperGame:
    tauler:Board

    def __init__(self, tauler = None):
        if tauler is None:
            tauler = Board()
        self.tauler = tauler
        return

    def get_pixel_coords(self, i, j):
        return c.CELLSIZE_PIXELS*i, c.CELLSIZE_PIXELS*j

    def get_img(self, celltype) -> pygame.surface.Surface:
        number_cells = [pygame.image.load(f"images/{i}_cell.png") for i in range(1, 7)]
        match celltype:
            case c.BOMB_CELL:
                img = pygame.image.load("images/bomb_cell.png")
            case c.EMPTY_CELL:
                img = pygame.image.load("images/cleared_cell.png")
            case n if n in [1, 2, 3, 4, 5, 6, 7, 8]:
                print(celltype)
                img = number_cells[celltype -1] 
            case c.FLAGGED_CELL:
                img = pygame.image.load("images/flagged_cell.png")
            case c.HIDDEN_CELL:
                img = pygame.image.load("images/hidden_cell.png")
            case _:
                raise ValueError("wht the fuuu")
        return img

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

    def init_board(self) -> pygame.display:
        tauler_inicial = self.tauler.get_board()

        CELLS_H, CELLS_W = self.tauler.get_size()

        WINDOW_W = c.CELLSIZE_PIXELS * CELLS_W
        WINDOW_H = c.CELLSIZE_PIXELS * CELLS_H

        display = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("Demo")

        fons = pygame.image.load("images/background.png")
        
        #setup icones
        old_casella = c.HIDDEN_CELL
        casella_img = self.get_img(old_casella)

        for i in range(CELLS_H):
            for j in range(CELLS_W):
                casella = int(tauler_inicial[i][j])
                if casella != old_casella: #evitar carregar molts cops la img
                    casella_img = self.get_img(casella)           

                display.blit(casella_img, self.get_pixel_coords(j, i)) #vol primer x i després y -> girem j - i 

                pygame.display.flip() #sense això no es fa la pantalla
                old_casella = casella
        return display

    def play(self, display):
        running = True
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("Window closed, quitting game")
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        x, y = event.pos
                        i, j = y // c.CELLSIZE_PIXELS, x // c.CELLSIZE_PIXELS
                        print(f"Clicked cell (h= {y // c.CELLSIZE_PIXELS}, w= {x // c.CELLSIZE_PIXELS})")  
                        # print(f"")
                        updated_cells = self.tauler.reveal_cell(i, j)
                        for i, j in updated_cells:

                            img = self.get_img(self.tauler.get_cell(i, j))
                            print(f"displaying cell {i}, {j}")
                            display.blit(img, self.get_pixel_coords(j, i)) # again, fem swap i <-> j

                        pygame.display.flip()
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
    print(game.tauler.get_hidden_board())
    pantalla = game.init_board()
    game.play(pantalla)
    return

if __name__ == "__main__":
    main()