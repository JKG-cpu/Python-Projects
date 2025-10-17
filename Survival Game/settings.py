from VividText import VividText as vt

# Typewriters
maintp = vt(bold = True, sleep = .03)
quicktp = vt(bold = True, sleep = 0)
errortp = vt(color = "bright_red", bold = True, sleep = 0)

# Variables
board_sizes = {
    "Small": (7, 7),
    "Medium": (10, 10),
    "Big": (15, 15),
    "Giant": (20, 20)
}
board_size_ratios = {
    "Small": 2,
    "Medium": 4,
    "Big": 5,
    "Giant": 7
}
tiles = {
    "Forest": {
        "Empty": ".",
        "Tree": "^",
        "Cave": "C",
        "Water": "#",
        "Player": "P"
    }
}

