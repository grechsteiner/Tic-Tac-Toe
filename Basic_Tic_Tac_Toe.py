#SE 101 Project
#Basic tic tac toe game


import random, pygame, time, os
from pygame.locals import *
from pygame import gfxdraw
import speech_recognition as sr

ICONONE = "X"   #The symbol for the first icon
ICONTWO = "O"   #The symbol for the second icon
BOARD_SIZE = 3  #Size of the board

# set up the window
WINDOWWIDTH = 480
WINDOWHEIGHT = 320

# set up the colors for drawing
BLACKCOLOUR = (0, 0, 0)
WHITECOLOUR = (255, 255, 255)
TANCOLOUR = (230, 220, 170)
GRAYCOLOUR = (169, 169, 169)


def get_speech():
    """Get speech and convert to text to text"""
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
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

def drawTextMiddle(text, font, surface, x, y, textcolour):
    """Draws the text on the surface at the location specified"""
    textobj = font.render(text, 1, textcolour)
    textrect = textobj.get_rect()
    textrect.midtop = (x, y)
    surface.blit(textobj, textrect)

def drawX(windowSurface, row, col, textcolour):
    """Draw a "X" in the designated spot"""

    x1 = 135 + col*80
    x2 = 185 + col*80

    y1= 80 + row*80
    y2 = 130 + row*80

    pygame.draw.line(windowSurface, textcolour, (x1, y1), (x2, y2))
    pygame.draw.line(windowSurface, textcolour, (x2, y1), (x1, y2))

def drawO(windowSurface, row, col, textcolour):
    """Draw a "O" in the designated spot"""

    x = 160 + col*80
    y = 105 + row*80

    gfxdraw.aacircle(windowSurface, x, y, 30, textcolour)    


###############################################
#Everything above here is pygame implementation
###############################################

def CreateGrid(size):
    """Accept a list, create a size by size blank 2-d list"""
    
    board = []
    for rows in range(size):
        row = []
        for cols in range(size):
            row.append(" ")
        board.append(row)

    return board


def CreateGridCopy(size):
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


def GameDone(board, current_icon):
    """Determine if the game has been won or not, return True or False"""
    
    #Check if previous move caused a win on horizontal line 
    for x in range(len(board)):
        win = True

        for y in range(len(board)):
            if board[x][y] != current_icon:
                win = False

        if win:
            return win

    #Check if previous move caused a win on vertical line 
    for x in range(len(board)):
        win = True

        for y in range(len(board)):
            if board[y][x] != current_icon:
                win = False
                
        if win:
            return win

    #Check if previous move was on the main diagonal and caused a win
    win = True
    for x in range(len(board)):
        if board[x][x] != current_icon:
            win = False

    if win:
        return win

    #Check if previous move was on the secondary diagonal and caused a win
    x = len(board) - 1
    win = True
    for y in range(len(board)):
        if board[x][y] != current_icon:
            win = False
        x = x - 1

    if win:
        return win

    #If we get to this point there hasn't been a winner and win is False 
    return win


def WhoGoesFirst():
    """Randomly determine if the computer or player goes first"""

    who_goes_first = random.randrange(2)
    if who_goes_first == 0:
        return "You"
    else:
        return "Jake Paul"


def MakeChange(copy, board, icon, chosen, size, available_numbers):
    """Update the board in the chosen icon with the current icon"""

    for x in range(size):
        for y in range(size):
            if copy[x][y] == chosen:
                board[x][y] = icon

    for x in range(len(available_numbers)):
        if str(available_numbers[x]) == chosen:
            available_numbers[x] = -1
                
def CreateAvailableNumbers(size):
    """Fill a list with available numbers given the size, used for available slots/spaces to pick"""

    available_numbers = []
    for x in range(1, size*size + 1):
        available_numbers.append(x)

    return available_numbers


def IsSpaceFree(chosen, available_numbers):
    """Determine if the chosen space is still available"""

    if chosen in available_numbers:
        return True
    
    else:
        return False


def MakeCopyBoard(board, size):
    """Make a copy of the board, used for AI"""

    newlist = []  
    for rows in range(size):
        row = []
        for cols in range(size):
            row.append(board[rows][cols])
        newlist.append(row)

    return newlist


def MakeCopyList(alist):
    """Make a copy of a list"""
    #newlist = the copied list 

    newlist = []
    for x in range(len(alist)):
        newlist.append(alist[x])

    return newlist


def ComputerChooseSpot(order, copy, board, computer_icon, player_icon, size, available_numbers):
    """Determine which spot the computer will play, return the corresponding value"""

    #Determine if the computer can win with their next move, make that move to win
    computer_win = CheckComputerWin(copy, available_numbers, size, computer_icon, board)
    if int(computer_win) >= 0:
        return computer_win

    #Check if the player can win with their next move, make move to block
    player_win = CheckPlayerWin(copy, available_numbers, size, player_icon, board)
    if int(player_win) >= 0:
        return player_win

    #If the computer goes second, the computer chooses centre if possible
    if order == "You":
    
        #Check if the centre is available
        centre = CheckCentre(copy, available_numbers, size)
        if int(centre) >= 0:
            return centre

        #Check if there is a corner available 
        corner = CheckCorner(copy, available_numbers, size)
        if int(corner) >= 0:
            return corner

    #The computer went/is going first, chooses corners at random if available
    else:

        #Check if there is a corner available 
        corner = CheckCorner(copy, available_numbers, size)
        if int(corner) >= 0:
            return corner
        
        #Check if the centre is available
        centre = CheckCentre(copy, available_numbers, size)
        if int(centre) >= 0:
            return centre
        
    #Pick a random spot on the board
    chosen = random.randrange(1, size*size + 1)
    while not IsSpaceFree(chosen, available_numbers):
        chosen = random.randrange(1, size*size + 1)

    return str(chosen)


def CheckComputerWin(copy, available_numbers, size, computer_icon, board):
    """Check if the computer can win, if they can return the coresponding number"""

    for x in range(size):
        for y in range(size):

            duplicate = MakeCopyBoard(board, size)        
            duplicate_numbers = MakeCopyList(available_numbers)
            chosen = int(copy[x][y])
            
            if IsSpaceFree(chosen, available_numbers):
                
                MakeChange(copy, duplicate, computer_icon, str(chosen), size, duplicate_numbers)
                
                if GameDone(duplicate, computer_icon):
                    
                    return str(chosen)

    return -1
    

def CheckPlayerWin(copy, available_numbers, size, player_icon, board):
    """Check if the player can win, if they can return the number that would block it"""
    
    for x in range(size):
        for y in range(size):

            duplicate = MakeCopyBoard(board, size)        
            duplicate_numbers = MakeCopyList(available_numbers)
            chosen = int(copy[x][y])
            
            if IsSpaceFree(chosen, available_numbers):
                
                MakeChange(copy, duplicate, player_icon, str(chosen), size, duplicate_numbers)
                
                if GameDone(duplicate, player_icon):
                    
                    return str(chosen)
                
    return -1
    

def CheckCorner(copy, available_numbers, size):
    """Determine if there is a corner free, if there is, return the value of it, else return -1"""


    available_slots = [0, 1, 2, 3]
                
    for x in range(4):

        #Make sure that corner hasn't already been tried
        picked = random.randrange(4)
        while picked not in available_slots:
            picked = random.randrange(4)
            
        #Top left
        if picked == 0:
            if IsSpaceFree(int(copy[0][0]), available_numbers):
                return copy[0][0]

        #Bottom left
        elif picked == 1:
            if IsSpaceFree(int(copy[size-1][0]), available_numbers):
                return copy[size-1][0]

        #Top right
        elif picked == 2:
            if IsSpaceFree(int(copy[0][size-1]), available_numbers):
                return copy[0][size-1]

        #Bottom right
        elif picked == 3:
            if IsSpaceFree(int(copy[size-1][size-1]), available_numbers):
                return copy[size-1][size-1]

        available_slots[picked] = -1

    return -1


def CheckCentre(copy, available_numbers, size):
    """Determine if the centre is available, if it is return the correpsonding value of it"""

    #Size is an even number, no exact centre, choose one of the four middle squares at random
    if size % 2 == 0:

        slots_available = [0, 1, 2, 3]

        for x in range(4):
            
            #Make sure that middle spot hasn't already been tried
            pick = random.randrange(4)
            while pick not in slots_available:
                pick = random.randrange(4)

            #Top left of middle slots
            if pick == 0:
                if IsSpaceFree(int(copy[int(size/2 - 1)][int(size/2 - 1)]), available_numbers):
                    return copy[int(size/2 - 1)][int(size/2 - 1)]

            #Bottom left of middle slots
            elif pick == 1:
                if IsSpaceFree(int(copy[int(size/2)][int(size/2 - 1)]), available_numbers):
                    return copy[int(size/2)][int(size/2 - 1)]

            #Top right of middle slots
            elif pick == 2:
                if IsSpaceFree(int(copy[int(size/2 - 1)][int(size/2)]), available_numbers):
                    return copy[int(size/2 - 1)][int(size/2)]

            #Bottom right of middle slots
            elif pick == 3:
                if IsSpaceFree(int(copy[int(size/2)][int(size/2)]), available_numbers):
                    return copy[int(size/2)][int(size/2)]

            slots_available[pick] = -1

        return -1
            

    #Size is an odd number, there is an exact centre
    else:
        if IsSpaceFree(int(copy[int(size/2)][int(size/2)]), available_numbers):
            return copy[int(size/2)][int(size/2)]

        return -1



def display_frame(windowSurface, board):
    """Update the screen of game"""

    #Draw tan background onto the surface
    windowSurface.fill(TANCOLOUR)

    #Set up font
    titleFont = pygame.font.SysFont("Times New Roman", 50, italic=True)

    #Draw title
    drawTextMiddle("Tic Tac Toe", titleFont, windowSurface, windowSurface.get_rect().centerx, 1, BLACKCOLOUR)
    
    #Draw lines of game
    #Vertical
    pygame.draw.line(windowSurface, BLACKCOLOUR, (199, 65), (199, 305))
    pygame.draw.line(windowSurface, BLACKCOLOUR, (281, 65), (281, 305))

    #Horizontal
    pygame.draw.line(windowSurface, BLACKCOLOUR, (120, 144), (360, 144))
    pygame.draw.line(windowSurface, BLACKCOLOUR, (120, 226), (360, 226))   

    #X's and O's
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            
            if board[row][col] == ICONONE:
                drawX(windowSurface, row, col, BLACKCOLOUR)

            elif board[row][col] == ICONTWO:
                drawO(windowSurface, row, col, BLACKCOLOUR)
    

    #Update screen
    pygame.display.update()



def display_end(windowSurface, board, string):
    """Update the screen of game"""

    #Draw tan background onto the surface
    windowSurface.fill(TANCOLOUR)

    #Set up font
    titleFont = pygame.font.SysFont("Times New Roman", 50, italic=True)
    endFont = pygame.font.SysFont("Times New Roman", 30, italic=False)

    #Draw title
    drawTextMiddle("Tic Tac Toe", titleFont, windowSurface, windowSurface.get_rect().centerx, 1, BLACKCOLOUR)
    
    drawTextMiddle(string, endFont, windowSurface, windowSurface.get_rect().centerx, 140, BLACKCOLOUR)

    #Update screen
    pygame.display.update()


def PlayerChooseSpot(size, available_numbers):
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

        if number != 0 and IsSpaceFree(number, available_numbers):
            return str(number)         


def main():
    """The mainline for the program"""

    pygame.init()

    #Set up windowsurface
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
    pygame.display.set_caption('Tic Tac Toe')

    #Create a 2D array representing the board, filled with blanks
    board = CreateGrid(BOARD_SIZE)

    #Create a copy of the board 2D array, but with the "slot" numbers instead of blanks
    copy = CreateGridCopy(BOARD_SIZE)

    #Create a list of available numbers to choose from (available slots (outlined above) )
    available_numbers = CreateAvailableNumbers(BOARD_SIZE)

    #Turns played
    turns = 0

    player_icon = ICONONE
    computer_icon = ICONTWO

    #Randomize who goes first
    turn = WhoGoesFirst()
    order = turn

    display_frame(windowSurface, board)

    #Run the game loop
    game_done = False
    while not game_done:

        display_frame(windowSurface, board)

        for event in pygame.event.get():
            continue

        #It's the players turn            
        if turn == "You":

            #Find out where the player wants to mark off
            chosen = PlayerChooseSpot(BOARD_SIZE, available_numbers)
            #Make the change in the 2D array (board)
            MakeChange(copy, board, player_icon, chosen, BOARD_SIZE, available_numbers)
            
            turns += 1

            display_frame(windowSurface, board)
            ##time.sleep(2)

            #Check if player has won and handle accordingly
            if GameDone(board, player_icon):
                display_frame(windowSurface, board)
                time.sleep(2)
                display_end(windowSurface, board, "You Beat The Legendary Jake Paul!")
                time.sleep(5)
                game_done = True
                
    
            #Check if the game is a tie and handle accordingly
            elif turns == 9:
                display_frame(windowSurface, board)
                time.sleep(2)
                display_end(windowSurface, board, "You're Lucky I Didn't KO You!")
                time.sleep(5)
                game_done = True

            #Switch the turn
            turn = "Jake Paul"


        #It's the computer's turn
        else:
            
            #Find out where the computer wants to play
            chosen = ComputerChooseSpot(order, copy, board, computer_icon, player_icon, BOARD_SIZE, available_numbers)
            #Make the change in the 2D array (board)
            MakeChange(copy, board, computer_icon, chosen, BOARD_SIZE, available_numbers)
            
            turns += 1

            time.sleep(3)
            display_frame(windowSurface, board)
            ##time.sleep(2)

            #Check if computer has won and handle accordingly
            if GameDone(board, computer_icon):
                display_frame(windowSurface, board)
                time.sleep(2)
                display_end(windowSurface, board, "Ha Ha! You Lose!")
                time.sleep(5)
                game_done = True
                

            #Check if the game is a tie and handle accordingly
            elif turns == 9:
                display_frame(windowSurface, board)
                time.sleep(2)
                display_end(windowSurface, board, "You're Lucky I Didn't KO You!")
                time.sleep(5)
                game_done = True
                
            #Switch the turn
            turn = "You"

    terminate()
        
main()

