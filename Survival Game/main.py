import random

from settings import *

class Map:
    def __init__(self):
        self.directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        self.board, self.tile_key = self._get_forest_board(*board_sizes["Small"], "Small")

    # Board Methods
    def _generate_board(self, x, y) -> list[list[str]]:
        # Generate Board
        board = [
            ["" for _ in range(x)] for _ in range(y)
        ]

        return board

    def _get_forest_board(self, x, y, size) -> tuple[list, dict]:
        board = self._generate_board(x, y)
        max_x, max_y = x - 1, y - 1
        
        tiles_tu = tiles["Forest"]
        tile_key = {
            name: key for name, key in tiles_tu.items()
        }

        # Player Spawn
        center_board = (int(x / 2), int(y / 2))
        board[center_board[0]][center_board[1]] = tiles_tu["Player"]

        # Pick Forest Amounts
        #region
        forest_amount = random.randint(2, 2 * board_size_ratios[size])

        taken_spots = []
        for _ in range(forest_amount):
            run = True
            while run:
                random_point = (random.randint(0, max_x), random.randint(0, max_y))
                if random_point not in taken_spots and board[random_point[0]][random_point[1]] == "":
                    taken_spots.append(random_point)
                    run = False
                else:
                    continue
            
        for x, y in taken_spots:
            board[x][y] = tiles_tu["Tree"]
            for dx, dy in self.directions:
                if (max_x >= x + dx > 0 and max_y >= y + dy > 0):
                    board[x + dx][y + dy] = tiles_tu["Tree"] if board[x + dx][y + dy] == "" else board[x + dx][y + dy]
        #endregion

        # Pick Random Cave Point
        while True:
            point = (random.randint(0, max_x), random.randint(0, max_y))
            if board[point[0]][point[1]] != "P":
                board[point[0]][point[1]] = tiles_tu["Cave"]
                break

        # Generate A Water Source
        water_size = 3 * board_size_ratios[size]
        while True:
            point = (random.randint(0, max_x), random.randint(0, max_y))
            if board[point[0]][point[1]] == '':
                board[point[0]][point[1]] = tiles_tu["Water"]
                water_size -= 1
                break

        return (board, tile_key)

    def display_board(self, board):
        for row in board:
            print('|', end='')
            for col in row:
                square = col if col != "" else " "
                print(f" {square} |", end='')
            print()

if __name__ == '__main__':
    map = Map()
    map.display_board(map.board)