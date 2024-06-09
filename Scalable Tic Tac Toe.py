# Simple tic tac toe game that is played via the terminal
# Scalable game engine that supports arbitrary board sizes (e.g. 200x200)
# Simple AI opponent that functions for any size board
# Written as a side project in Grade 11 (2021) during one of the many Covid-19 lockdowns

import random

ICON_ONE = "X"   #The symbol for the first icon
ICON_TWO = "O"   #The symbol for the second icon


def create_grid(size):
    """Accept a list, create a size by size blank 2-d list"""

    board = []
    for rows in range(size):
        row = []
        for cols in range(size):
            row.append(" ")
        board.append(row)

    return board


def create_grid_copy(size):
    """Accept a list, create a size by size 2-d list with numbers like a number pad"""

    copy = []
    counter = size*size - (size-1)
    for rows in range(size):
        row = []
        for cols in range(size):
            row.append(str(counter))
            counter = counter + 1

        counter = counter - (size*2)
        copy.append(row)

    return copy


def display_board(board):
    """Accepts a 2-d list, displays it along with the other board components"""

    for y in range(len(board)):
        
        # Print the vertical lines above the icon
        vertical_lines = "   "
        for x in range(len(board) - 1):
            vertical_lines = vertical_lines + "|   "
        print(vertical_lines)

        # Print the row with the icon
        for x in range(len(board)):
            print(" " + board[y][x], end = " ")

            if x < len(board) - 1:
                print("|", end = "")

        # Print the vertical lines below the icon
        vertical_lines = "\n   "
        for x in range(len(board) - 1):
            vertical_lines = vertical_lines + "|   "
        print(vertical_lines)

        # Print the horizontal lines
        if y < (len(board) - 1):
            dash = ""
            for z in range(len(board)*4 - 1):
                dash = dash + "-"
            print(dash)


def choose_player_icon(icon_one, icon_two):
    """Accepts two icons, returns the players chosen icon"""

    icon = input("Do you want to be " + icon_one + " or " + icon_two + "? ")
    while icon.upper() != icon_one and icon.upper() != icon_two:
        icon = input("Please enter either " + icon_one + " or " + icon_two + ". ")

    return icon.upper()


def choose_computer_icon(icon_one, icon_two, player_icon):
    """Return the opposite icon to the accepted player icon"""

    if player_icon == icon_one:
        return icon_two
    else:
        return icon_one


def continue_playing():
    """Ask the user if they would like to play again, return Y or N"""

    answer = input("Do you want to play again? (yes/no) ")
    while answer.upper() != "YES" and answer.upper() != "NO":
        print("Please enter yes or no.")
        answer = input("Do you want to play again? (yes/no) ")

    return answer


def is_game_done(board, current_icon):
    """Determine if the game has been won or not, return True or False"""
    
    # Check if previous move caused a win on horizontal line 
    for x in range(len(board)):
        win = True
        for y in range(len(board)):
            if board[x][y] != current_icon:
                win = False
        if win:
            return win

    # Check if previous move caused a win on vertical line 
    for x in range(len(board)):
        win = True
        for y in range(len(board)):
            if board[y][x] != current_icon:
                win = False
        if win:
            return win

    # Check if previous move was on the main diagonal and caused a win
    win = True
    for x in range(len(board)):
        if board[x][x] != current_icon:
            win = False
    if win:
        return win

    # Check if previous move was on the secondary diagonal and caused a win
    x = len(board) - 1
    win = True
    for y in range(len(board)):
        if board[x][y] != current_icon:
            win = False
        x = x - 1
    if win:
        return win

    # If we get to this point there hasn't been a winner and win is False 
    return win


def who_goes_first():
    """Randomly determine if the computer or player goes first, returns 1 or 2"""

    who_goes_first = random.randrange(2)
    if who_goes_first == 0:
        return "player"
    else:
        return "computer"


def make_change(copy, board, icon, chosen, size, available_numbers):
    """Update the board in the chosen icon with the current icon"""

    for x in range(size):
        for y in range(size):
            if copy[x][y] == chosen:
                board[x][y] = icon

    for x in range(len(available_numbers)):
        if str(available_numbers[x]) == chosen:
            available_numbers[x] = -1
                

def player_choose_spot(size, available_numbers):
    """Let the player choose what spot they want to play"""

    valid = False
    while not valid:
        chosen = input("What is your next move? (1-" + str(size*size) + ") ")
        if chosen.isdigit():   
            if int(chosen) < 1 or int(chosen) > size*size:
                print("Please enter a number from 1 to", str(size*size) + ".")
            elif not is_space_free(int(chosen),available_numbers):
                print("That spot is already taken.")
            else:
                return chosen
        else:
            print("Please enter a number from 1 to", str(size*size) + ". ")


def create_available_numbers(size):
    """Fill a list with available numbers given the size"""

    available_numbers = []
    for x in range(1, size*size + 1):
        available_numbers.append(x)
    return available_numbers


def is_space_free(chosen, available_numbers):
    """Determine if the chosen space is still available"""

    if chosen in available_numbers:
        return True
    else:
        return False


def make_copy_board(board, size):
    """Make a copy of the board"""

    newlist = []
    for rows in range(size):
        row = []
        for cols in range(size):
            row.append(board[rows][cols])
        newlist.append(row)
    return newlist


def make_copy_list(alist):
    """Make a copy of a list"""

    newlist = []
    for x in range(len(alist)):
        newlist.append(alist[x])
    return newlist


def computer_choose_spot(order, copy, board, computer_icon, player_icon, size, available_numbers):
    """Determine which spot the computer will play, return the corresponding value"""
    
    # Determine if the computer can win
    computer_win = check_computer_win(copy, available_numbers, size, computer_icon, board)
    if int(computer_win) >= 0:
        return computer_win

    # Check if the player can win
    player_win = check_player_win(copy, available_numbers, size, player_icon, board)
    if int(player_win) >= 0:
        return player_win

    # If the computer goes second, the computer chooses centre over the corners
    if order == "player":
        # Check if the centre is available
        centre = check_centre(copy, available_numbers, size)
        if int(centre) >= 0:
            return centre

        # Check if there is a corner available 
        corner = check_corner(copy, available_numbers, size)
        if int(corner) >= 0:
            return corner

    else:
        # Check if there is a corner available 
        corner = check_corner(copy, available_numbers, size)
        if int(corner) >= 0:
            return corner
        
        # Check if the centre is available
        centre = check_centre(copy, available_numbers, size)
        if int(centre) >= 0:
            return centre
        
    # Pick a random spot on the board
    chosen = random.randrange(1, size*size + 1)
    while not is_space_free(chosen, available_numbers):
        chosen = random.randrange(1, size*size + 1)

    return str(chosen)


def check_computer_win(copy, available_numbers, size, computer_icon, board):
    """Check if the computer can win, if they can return the coresponding number"""

    for x in range(size):
        for y in range(size):
            duplicate = make_copy_board(board, size)        
            duplicate_numbers = make_copy_list(available_numbers)
            chosen = int(copy[x][y])
            if is_space_free(chosen, available_numbers):
                make_change(copy, duplicate, computer_icon, str(chosen), size, duplicate_numbers)
                if is_game_done(duplicate, computer_icon):
                    return str(chosen)
    return -1
    

def check_player_win(copy, available_numbers, size, player_icon, board):
    """Check if the player can win, if they can return the number that would block it"""
    
    for x in range(size):
        for y in range(size):
            duplicate = make_copy_board(board, size)        
            duplicate_numbers = make_copy_list(available_numbers)
            chosen = int(copy[x][y])
            if is_space_free(chosen, available_numbers):
                make_change(copy, duplicate, player_icon, str(chosen), size, duplicate_numbers)
                if is_game_done(duplicate, player_icon):
                    return str(chosen)  
    return -1
    

def check_corner(copy, available_numbers, size):
    """Determine if there is a corner free, if there is, return the value of it, else return -1"""
   
    available_slots = [0, 1, 2, 3]  
    for x in range(4):

        # Make sure that corner hasn't already been tried
        picked = random.randrange(4)
        while picked not in available_slots:
            picked = random.randrange(4)
            
        # Top left
        if picked == 0:
            if is_space_free(int(copy[0][0]), available_numbers):
                return copy[0][0]
        # Bottom left
        elif picked == 1:
            if is_space_free(int(copy[size-1][0]), available_numbers):
                return copy[size-1][0]
        # Top right
        elif picked == 2:
            if is_space_free(int(copy[0][size-1]), available_numbers):
                return copy[0][size-1]
        # Bottom right
        elif picked == 3:
            if is_space_free(int(copy[size-1][size-1]), available_numbers):
                return copy[size-1][size-1]

        available_slots[picked] = -1

    return -1


def check_centre(copy, available_numbers, size):
    """Determine if the centre is available, if it is return the correpsonding value of it"""

    # Size is an even number, no exact centre, choose one of the four middle squares at random
    if size % 2 == 0:
        slots_available = [0, 1, 2, 3]
        for x in range(4):
            
            #Make sure that middle spot hasn't already been tried
            pick = random.randrange(4)
            while pick not in slots_available:
                pick = random.randrange(4)

            # Top left of middle slots
            if pick == 0:
                if is_space_free(int(copy[int(size/2 - 1)][int(size/2 - 1)]), available_numbers):
                    return copy[int(size/2 - 1)][int(size/2 - 1)]

            # Bottom left of middle slots
            elif pick == 1:
                if is_space_free(int(copy[int(size/2)][int(size/2 - 1)]), available_numbers):
                    return copy[int(size/2)][int(size/2 - 1)]

            # Top right of middle slots
            elif pick == 2:
                if is_space_free(int(copy[int(size/2 - 1)][int(size/2)]), available_numbers):
                    return copy[int(size/2 - 1)][int(size/2)]

            # Bottom right of middle slots
            elif pick == 3:
                if is_space_free(int(copy[int(size/2)][int(size/2)]), available_numbers):
                    return copy[int(size/2)][int(size/2)]

            slots_available[pick] = -1
        return -1
            
    # Size is an odd number, there is an exact centre
    else:
        if is_space_free(int(copy[int(size/2)][int(size/2)]), available_numbers):
            return copy[int(size/2)][int(size/2)]
        return -1


def choose_board_size():
    """Lets the user choose what size of board they want to play on, greater than 1"""

    board_size = int(input("What size of board do you want to play on? "))
    while board_size <= 1:
        print("Please choose a size greater than 1.")
        board_size = int(input("What size of board do you want to play on? "))

    return board_size
        
    
def main():
    """The mainline for the program"""

    print("Welcome to Tic Tac Toe!")
    still_playing = "YES"
    while still_playing.upper() == "YES":    
        board_size = choose_board_size()                            # Let the user choose the board size
        board = create_grid(board_size)                              # Create a grid list of the board, filled with blanks
        copy = create_grid_copy(board_size)                           # Create a copy of the grid list, but with the numbers "slot" instead of blanks
        available_numbers = create_available_numbers(board_size)      # Create a list of available numbers to choose from
        turns = 0
        
        player_icon = choose_player_icon(ICON_ONE, ICON_TWO)
        computer_icon = choose_computer_icon(ICON_ONE, ICON_TWO, player_icon)
        
        turn = who_goes_first()
        print("The", turn, "will go first.")
        order = turn
        
        game_done = False
        while not game_done:
            if turn == "player":
                # It's the players turn
                display_board(board)
                chosen = player_choose_spot(board_size, available_numbers)
                make_change(copy, board, player_icon, chosen, board_size, available_numbers)
                turns = turns + 1
            
                if is_game_done(board, player_icon):
                    display_board(board)
                    print("Hooray! You have won the game!")
                    game_done = True
                elif turns == len(board)*len(board):
                    display_board(board)
                    print("The game is a tie!")
                    game_done = True
                turn = "computer"

            else:
                # It's the computer's turn
                chosen = computer_choose_spot(order, copy, board, computer_icon, player_icon, board_size, available_numbers)
                make_change(copy, board, computer_icon, chosen, board_size, available_numbers)
                turns = turns + 1
                
                if is_game_done(board, computer_icon):
                    display_board(board)
                    print("The computer has beaten you! You lose.")
                    game_done = True
                elif turns == len(board)*len(board):
                    display_board(board)
                    print("The game is a tie!")
                    game_done = True
                turn = "player"

        still_playing = continue_playing()
        
main()
