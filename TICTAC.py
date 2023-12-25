#Group Members: 
#Laurent Lorquet (Architect)
#Sebastian Rojas (Developer)
#Cedric Winter (Reporter)
#Professor: Dr. Oge Marques 
import random
import math
def print_tictac(tictac):
    for row in tictac:
        print(" | ".join(row))
        print("-" * 9)
def check_wwchickendinner(tictac, gamer):
    for row in tictac:
        if all(cell == gamer for cell in row):
            return True
    for uhoh in range(3):
        if all(tictac[row][uhoh] == gamer for row in range(3)):
            return True
    if all(tictac[i][i] == gamer for i in range(3)) or all(tictac[i][2 - i] == gamer for i in range(3)):
        return True
    return False
def is_tictac_full(tictac):
    return all(cell != " " for row in tictac for cell in row)
def get_no_cells(tictac):
    return [(row, uhoh) for row in range(3) for uhoh in range(3) if tictac[row][uhoh] == " "]
def user_move(tictac):
    while True:
        try:
            move = int(input("Enter your move (1-9): "))
            row = (move - 1) // 3
            uhoh = (move - 1) % 3
            if tictac[row][uhoh] == " ":
                return row, uhoh
            else:
                print("That cell is already occupied. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a number between 1 and 9.")
def minmax(tictac, depth, maximizing_gamer):
    if check_wwchickendinner(tictac, "O"):
        return 1
    if check_wwchickendinner(tictac, "X"):
        return -1
    if is_tictac_full(tictac):
        return 0
    if maximizing_gamer:
        max_eval = -math.inf
        for row, uhoh in get_no_cells(tictac):
            tictac[row][uhoh] = "O"
            eval = minmax(tictac, depth + 1, False)
            tictac[row][uhoh] = " "
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for row, uhoh in get_no_cells(tictac):
            tictac[row][uhoh] = "X"
            eval = minmax(tictac, depth + 1, True)
            tictac[row][uhoh] = " "
            min_eval = min(min_eval, eval)
        return min_eval
def computer_move(tictac):
    best_move = None
    best_eval = -math.inf
    for row, uhoh in get_no_cells(tictac):
        tictac[row][uhoh] = "O"
        eval = minmax(tictac, 0, False)
        tictac[row][uhoh] = " "

        if eval > best_eval:
            best_eval = eval
            best_move = (row, uhoh)
    return best_move
def play_game():
    print("You will be playing a Tic-Tac-Toe soon against the computer! ")
    print("Remember that each placement works like an old phone working from")
    print("1 | 2 | 3 /n")
    print("4 | 5 | 6 /n")
    print("7 | 8 | 9 /n")
    print(".............................................................. ")
    print("Welcome to Tic-Tac-Toe!")
    while True:
        tictac = [[" " for _ in range(3)] for _ in range(3)]
        user_symbol = "X"
        computer_symbol = "O"
        current_gamer = user_symbol
        print_tictac(tictac)
        while True:
            if current_gamer == user_symbol:
                row, uhoh = user_move(tictac)
            else:
                row, uhoh = computer_move(tictac)
            tictac[row][uhoh] = current_gamer
            print_tictac(tictac)
            if check_wwchickendinner(tictac, current_gamer):
                print(f"{current_gamer} wins!")
                break
            elif is_tictac_full(tictac):
                print("It's a tie!")
                break
            current_gamer = user_symbol if current_gamer == computer_symbol else computer_symbol
        play_again = input("Do you want to play again? (yes || no): ")
        if play_again.lower() != "yes":
            break
if __name__ == "__main__":
    play_game()
