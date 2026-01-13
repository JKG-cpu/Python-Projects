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
