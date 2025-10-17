import random

from .settings import *

class Map:
    def __init__(self):
        self.directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        self.method_keys = {
            "Forest": self._get_forest_board
        }

    # New Board
    def new_board(self, type, x, y, size) -> tuple[list, list]:
        board, tile_key = self.method_keys[type](x, y, size)

        return (board, tile_key)

    # Board Generate Methods
    def flood_fill(self, max_x, max_y, board, water, size, amount: int = 1):
        for _ in range(amount):
            # Generate a Water Source using Flood Fill
            water_size = 3 * board_size_ratios[size]

            # Find a valid starting point for water
            while True:
                start = (random.randint(0, max_x), random.randint(0, max_y))
                if board[start[0]][start[1]] == "":
                    break

            # Flood fill logic (iterative)
            stack = [start]
            filled = 0

            while stack and filled < water_size:
                x, y = stack.pop()

                if board[x][y] != "":
                    continue  # Skip non-empty tiles

                board[x][y] = water
                filled += 1

                # Check 4-directionally (or 8 if you want diagonals)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # ← ↑ ↓ →
                    nx, ny = x + dx, y + dy
                    if 0 <= nx <= max_x and 0 <= ny <= max_y:
                        if board[nx][ny] == "":
                            stack.append((nx, ny))

    def _generate_board(self, x, y) -> list[list[str]]:
        # Generate Board
        board = [
            ["" for _ in range(x)] for _ in range(y)
        ]

        return board

    # Generate Different Boards
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
        forest_amount = 2 * board_size_ratios[size]

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

        # Generate a Water Source using Flood Fill
        amount = 1
        if board_size_ratios[size] >= 5:
            amount = 4

        self.flood_fill(max_x, max_y, board, tiles_tu["Water"], size, amount)

        # Make ALL other tiles empty
        for i, row in enumerate(board):
            for j, col in enumerate(row):
                if col == "":
                    board[i][j] = tiles_tu["Empty"]

        return (board, tile_key)

    # Draw the board
    def display_board(self, board):
        for row in board:
            print('|', end='')
            for col in row:
                square = col if col != "" else " "
                print(f" {square} |", end='')
            print()
