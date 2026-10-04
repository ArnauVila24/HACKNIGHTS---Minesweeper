from minesweep import Board
import pygame

CELLSIZE = 32

def get_coords(i, j):
    return CELLSIZE*i, CELLSIZE*j

def show_board(tauler:Board) -> None:
    tauler_inicial = tauler.get_board()

    CELLS_W, CELLS_H = tauler.get_size()

    WINDOW_W = CELLSIZE * CELLS_W
    WINDOW_H = CELLSIZE * CELLS_H

    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Demo")

    fons = pygame.image.load("images/background.png")
    bomba = pygame.image.load("images/bomb_cell.png")
    empty = pygame.image.load("images/cleared_cell.png")
    number_cells = [pygame.image.load(f"images/{i}_cell.png") for i in range(1, 7)]

    #setup icones
    for i in range(CELLS_W):
        for j in range(CELLS_H):
            casella = int(tauler_inicial[i][j])
            match casella:
                case -1:
                    casella_img = bomba
                case 0:
                    casella_img = empty
                case n if n in [1, 2, 3, 4, 5, 6, 7, 8]:
                    casella_img = number_cells[casella -1]            

            screen.blit(casella_img, get_coords(i, j))

    pygame.display.flip() #sense això no es fa la pantalla

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Window closed, quitting game")
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                print(f"Clicked cell ({x // CELLSIZE}, {y // CELLSIZE})")       

    pygame.quit()
    return

def main():
    example_board = Board(10, 10)
    show_board(example_board)
    return

if __name__ == "__main__":
    main()