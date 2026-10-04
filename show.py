from minesweep import Board
from PIL import Image, ImageDraw

def get_coords(i, j):
    return 32*i, 32*j

def main() -> None:
    fons = Image.open("images/background.png")
    bomba = Image.open("images/bomb_cell.png")

    for i in range(10):
        # for j in range(10):

        fons.paste(bomba, get_coords(i, i))

    return

if __name__ == "__main__":
    main()