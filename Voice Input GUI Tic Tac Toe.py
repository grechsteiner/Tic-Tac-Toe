# Simple tic tac toe game with graphical interface
# Simple AI opponent
# Voice input for entering moves (see player_choose_spot function for supported instructions)
# Voice input and graphical interface added to original "Scalable Tic Tac Toe.py" program during Freshman year at uwaterloo (2022)


import random, pygame, time, os
from pygame.locals import *
from pygame import gfxdraw
import speech_recognition as sr


ICON_ONE = "X"   # The symbol for the first icon
ICON_TWO = "O"   # The symbol for the second icon
BOARD_SIZE = 3   # Size of the board

# Set up the window dimensions
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 320

# Set up the colors for drawing
BLACK_COLOUR = (0, 0, 0)
WHITE_COLOUR = (255, 255, 255)
TAN_COLOUR = (230, 220, 170)
GRAY_COLOUR = (169, 169, 169)


def get_speech():
    """Get speech and convert to text to text"""
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    text = ""
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        pass
 
    return text


def terminate():
    """This function is called when the user closes the window or presses ESC"""

    pygame.quit()
    os._exit(1)


def draw_text_middle(text, font, surface, x, y, textcolour):
    """Draws the text on the surface at the location specified"""

    textobj = font.render(text, 1, textcolour)
    textrect = textobj.get_rect()
    textrect.midtop = (x, y)
    surface.blit(textobj, textrect)


def draw_x(windowSurface, row, col, textcolour):
    """Draw a "X" in the designated spot"""

    x1 = 135 + col*80
    x2 = 185 + col*80
    y1 = 80  + row*80
    y2 = 130 + row*80
    pygame.draw.line(windowSurface, textcolour, (x1, y1), (x2, y2))
    pygame.draw.line(windowSurface, textcolour, (x2, y1), (x1, y2))


def draw_o(windowSurface, row, col, textcolour):
    """Draw a "O" in the designated spot"""

    x = 160 + col*80
    y = 105 + row*80
    gfxdraw.aacircle(windowSurface, x, y, 30, textcolour)    


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
        return "Player"
    else:
        return "Computer"


def make_change(copy, board, icon, chosen, size, available_numbers):
    """Update the board in the chosen icon with the current icon"""

    for x in range(size):
        for y in range(size):
            if copy[x][y] == chosen:
                board[x][y] = icon

    for x in range(len(available_numbers)):
        if str(available_numbers[x]) == chosen:
            available_numbers[x] = -1
                

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
    if order == "Player":
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

def display_frame(windowSurface, board):
    """Update the screen of game"""

    # Draw tan background onto the surface
    windowSurface.fill(TAN_COLOUR)

    # Set up font
    titleFont = pygame.font.SysFont("Times New Roman", 50, italic=True)

    # Draw title
    draw_text_middle("Tic Tac Toe", titleFont, windowSurface, windowSurface.get_rect().centerx, 1, BLACK_COLOUR)
    
    # Draw lines of game
    # Vertical
    pygame.draw.line(windowSurface, BLACK_COLOUR, (199, 65), (199, 305))
    pygame.draw.line(windowSurface, BLACK_COLOUR, (281, 65), (281, 305))

    # Horizontal
    pygame.draw.line(windowSurface, BLACK_COLOUR, (120, 144), (360, 144))
    pygame.draw.line(windowSurface, BLACK_COLOUR, (120, 226), (360, 226))   

    # X's and O's
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == ICON_ONE:
                draw_x(windowSurface, row, col, BLACK_COLOUR)
            elif board[row][col] == ICON_TWO:
                draw_o(windowSurface, row, col, BLACK_COLOUR)

    # Update screen
    pygame.display.update()



def display_end(windowSurface, board, string):
    """Update the screen of game"""

    # Draw tan background onto the surface
    windowSurface.fill(TAN_COLOUR)

    # Set up font
    titleFont = pygame.font.SysFont("Times New Roman", 50, italic=True)
    endFont = pygame.font.SysFont("Times New Roman", 30, italic=False)

    # Draw title
    draw_text_middle("Tic Tac Toe", titleFont, windowSurface, windowSurface.get_rect().centerx, 1, BLACK_COLOUR)
    draw_text_middle(string, endFont, windowSurface, windowSurface.get_rect().centerx, 140, BLACK_COLOUR)

    # Update screen
    pygame.display.update()


def player_choose_spot(size, available_numbers):
    """Let the player choose what spot they want to play"""

    valid = False
    while not valid:
        chosen = get_speech()

        if chosen == "bottom left":
            number = 1
        elif chosen == "bottom middle":
            number = 2
        elif chosen == "bottom right":
            number = 3
        elif chosen == "middle left":
            number = 4
        elif chosen == "middle middle":
            number = 5
        elif chosen == "middle right":
            number = 6
        elif chosen == "top left":
            number = 7
        elif chosen == "top middle":
            number = 8
        elif chosen == "top right":
            number = 9
        else:
            number = 0

        if number != 0 and is_space_free(number, available_numbers):
            return str(number)         


def main():
    """The mainline for the program"""

    pygame.init()

    # Set up windowsurface
    windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    pygame.display.set_caption('Tic Tac Toe')

    board = create_grid(BOARD_SIZE)                             # Create a 2D array representing the board, filled with blanks
    copy = create_grid_copy(BOARD_SIZE)                         # Create a copy of the board 2D array, but with the "slot" numbers instead of blanks
    available_numbers = create_available_numbers(BOARD_SIZE)    # Create a list of available numbers to choose from (available slots (outlined above) )

    turns = 0
    player_icon = ICON_ONE
    computer_icon = ICON_TWO

    # Randomize who goes first
    turn = who_goes_first()
    order = turn

    display_frame(windowSurface, board)

    # Run the game loop
    game_done = False
    while not game_done:
        display_frame(windowSurface, board)
        for event in pygame.event.get():
            continue

        # It's the players turn            
        if turn == "Player":

            # Find out where the player wants to mark off
            chosen = player_choose_spot(BOARD_SIZE, available_numbers)
            make_change(copy, board, player_icon, chosen, BOARD_SIZE, available_numbers)
            turns += 1
            display_frame(windowSurface, board)

            # Check if player has won and handle accordingly
            if is_game_done(board, player_icon):
                display_frame(windowSurface, board)
                time.sleep(2)
                display_end(windowSurface, board, "You Won!")
                time.sleep(5)
                game_done = True
                
            # Check if the game is a tie and handle accordingly
            elif turns == 9:
                display_frame(windowSurface, board)
                time.sleep(2)
                display_end(windowSurface, board, "Tie Game")
                time.sleep(5)
                game_done = True

            # Switch the turn
            turn = "Computer"

        # It's the computer's turn
        else:
            
            # Find out where the computer wants to play
            chosen = computer_choose_spot(order, copy, board, computer_icon, player_icon, BOARD_SIZE, available_numbers)
            make_change(copy, board, computer_icon, chosen, BOARD_SIZE, available_numbers)
            turns += 1
            time.sleep(3)
            display_frame(windowSurface, board)

            # Check if computer has won and handle accordingly
            if is_game_done(board, computer_icon):
                display_frame(windowSurface, board)
                time.sleep(2)
                display_end(windowSurface, board, "You Lost!")
                time.sleep(5)
                game_done = True
                

            # Check if the game is a tie and handle accordingly
            elif turns == 9:
                display_frame(windowSurface, board)
                time.sleep(2)
                display_end(windowSurface, board, "Tie Game")
                time.sleep(5)
                game_done = True
                
            # Switch the turn
            turn = "Player"

    terminate()
        
main()

