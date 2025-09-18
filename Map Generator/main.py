import random

class Generator:
    def __init__(self):
        self.object_types = {
            "Empty": " ",
            "Path": ".",
            "Wall": "#",
            "Corridor": "+",
            "Player Spawn": "P",
            "Enemy Spawn": "E"
        }
            
    def generator(self, enemy_count: int = 5, row: int = 10, col: int = 10, padding: int = 0):
        def in_bounds(x, y):
            return min_x <= x <= max_x and min_y <= y <= max_y

        def generate_hall_area(x, y):
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if in_bounds(nx, ny) and layout[nx][ny] == []:
                    layout[nx][ny] = self.object_types["Wall"]

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # N, S, W, E
        layout = [[[] for _ in range(col)] for _ in range(row)]

        # Bounds after padding
        min_x, max_x = padding, row - 1 - padding
        min_y, max_y = padding, col - 1 - padding

        if max_x <= min_x or max_y <= min_y:
            raise ValueError("Invalid dimensions after padding")

        # 1. Place Player Spawn
        player_spawn = (random.randint(min_x, max_x), random.randint(min_y, max_y))
        layout[player_spawn[0]][player_spawn[1]] = self.object_types["Player Spawn"]
        generate_hall_area(player_spawn[0], player_spawn[1])
        current_pos = player_spawn

        # 2. Generate Hallways
        num_paths = 20
        for _ in range(num_paths):
            direction = random.choice(directions)
            steps = random.randint(3, 7)
            temp_pos = current_pos  # Save last known good position

            for _ in range(steps):
                nx = temp_pos[0] + direction[0]
                ny = temp_pos[1] + direction[1]

                if not in_bounds(nx, ny):
                    break

                if layout[nx][ny] in [self.object_types["Corridor"], self.object_types["Player Spawn"]]:
                    break  # Don't overwrite existing corridor or spawn

                layout[nx][ny] = self.object_types["Corridor"]
                generate_hall_area(nx, ny)
                temp_pos = (nx, ny)

            # Only update current_pos if we successfully moved at least once
            if temp_pos != current_pos:
                current_pos = temp_pos

        # 3. Place enemies on random corridor tiles
        corridor_tiles = [(x, y) for x in range(row) for y in range(col) if layout[x][y] == self.object_types["Corridor"]]
        enemy_count = min(enemy_count, len(corridor_tiles))
        for x, y in random.sample(corridor_tiles, enemy_count):
            layout[x][y] = self.object_types["Enemy Spawn"]

        # Display map
        self.display_map(layout)
        return layout

    def display_map(self, layout):
        row_line = "+" + "----" * len(layout[0]) + '-+'
        print(row_line)
        for row in layout:
            print(" ", end='')
            for col in row:
                square = col if not isinstance(col, list) else " "
                print(f"| {square} ", end='')
            print("|")
        print(row_line)

if __name__ == '__main__':
    Generator().generator()
