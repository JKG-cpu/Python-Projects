from os import name, system

def display_board(board: list[int]):
    for i, num in enumerate(board, 1):
        if i % 3 == 0:
            if num == 1:
                print("X")
            
            elif num == -1:
                print("O")
            
            else:
                print(" ")
            
        else:
            if num == 1:
                print("X", end = " | ")
            
            elif num == -1:
                print("O", end = " | ")
            
            else:
                print(" ", end = " | ")

def get_board_input():
    while True:
        raw_input = input("Enter in a place to move (1 - 9) > ").strip()
        
        if raw_input in '123456789':
            return int(raw_input) - 1
    
        else:
            print("Not a valid option...")

def cc():
    system("cls" if name == "nt" else "clear")
