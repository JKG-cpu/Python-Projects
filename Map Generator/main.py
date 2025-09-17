import random

class Generator:
    def __init__(self):
        self.object_types = {
            "Empty": " ",
            "Path": ".",
            "Wall": "#",
            "Player Spawn": "P",
            "Enemy Spawn": "E"
        }

    def generator(self, enemy_count: int = 5, row: int = 10, col: int = 10, padding: int = 0):
        object_count = {
            "Player": 1,
            "Enemy": enemy_count
        }
        layout = [
            [[] for _ in range(col)] for _ in range(row)
        ]

        # Base Variabels
        min_x, max_x = 0 + padding, row - 1 - padding
        min_y, max_y = 0 + padding, col - 1 - padding

        if (max_x <= min_x) or (max_y <= min_y):
            raise ValueError(f"Invalid padding, row, or column.")

        # Generate Random Hallways
        # for i, row in enumerate(layout):
        #     for j, col in enumerate(row):
        #         if (i > min_x and i < max_x) and (j > min_y and j < max_y):
        #             layout[i][j] = "#"
        # Pick a point
        player_spawn = (random.randint(min_x, max_x), random.randint(min_y, max_y))

        # Start by filling player point and making hallways (x + (directions), y + (directions))

        # Display and return generated layout
        self.display_map(layout)
        return layout

    def display_map(self, layout):
        row_line = "+" + "----" * len(layout[0]) + '-+'
    
        print(row_line)

        # Map
        for row in layout:
            print(" ", end='')
            for col in row:
                square = col if not isinstance(col, list) else " "
                print(f"| {square} ", end='')
            print("|")
        
        print(row_line)

if __name__ == '__main__':
    Generator().generator()