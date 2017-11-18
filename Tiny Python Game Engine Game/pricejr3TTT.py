"""
Jarred Price
CSE 102
13 May 2016

Tic-Tac-Toe created in the Tiny Python Game Engine!

This module defines a very simple interactive game of Tic-Tac-Toe.

There are 3 AI's implemented:
1.) Easy AI: AI which will pick a random move.
2.) Medium AI: AI which will pick a random move, unless they can block the player,
then they will block the player instead.
3.) Hard AI: AI that follows the minimax algorithm in order to pick optimal move.

There is a peer vs. peer mode. X vs. O and both share the screen.

HOW TO PLAY:

* There are 9 cells, which represent the TTT board.
* There are 4 different opttions which the user will choose
* You can click on a different mode and it will switch to the other mode
and start a new game while you are playing a game.

**************** If you have finished a game, you must click on the game mode that you want to play next
twice to start playing on the new game mode. Clicking it once after a game has finished, will just start
a new instance of the current difficulty that you are in. Double click it to choose the new difficulty!****************

* Click anywhere outside of the tic tac toe board and anywhere outside of the difficulty choices,
the game will restart if you are currently playing and it will do nothing if you have just finished a game.
If you have just finished a game, you must click a difficulty option to start again (but again, double click
to start a new gamemode and click once to start a new instance of your current game mode.



The data model used by this game is described as follows:

A Cell is either represented by three different strings: '-' denoting an empty space, 'x' denoting a space for player x, and 'o' denoting a space
for player o. A boardState represents the state of the entire Tic-Tac-Toe board and for example:
boardState[cell] such as boardState[1] will return the string that is found at that specific state. The game
follows the rules of tic tac toe and if boardState[0] and boardState[1] and boardState[2] all equal the same
'x' or 'o' string character, then we have a winner. If there is no such match of 3 in a row, then we have a 
tie game.

The board is laid out like:
    -----
    0|1|2
    -----
    3|4|5
    -----
    6|7|8
    -----
With 0 being cell 0, 1 being cell 1, and so on.

There are other cells that can be clicked, such as the difficulty mode selectors and
the non "button" spaces that can reset your game whilst playing a game (e.g, if you are playing
a game and click anywhere not contained in a box, then it will restart).

Cells 0-8 represent the tic-tac-toe board. 
Cells 9 = hard option, 10 = medium option, 11 = easy option, 12 = peer vs peer option.

We have point objects which are pairs of (x,y) ints that are found within the bounds of
the play area of 650 for width and 480 for height.

Piece repesents the type of string that is passed through. 'x', 'o' or '-' and these are used to determine
win conditions, tie conditions, etc.

There are lines that are used, which are line segments to draw the locations of the board and other boxes
and they are 4-tuples: (x1, y1, x2, y2).

Global xWON and global yWON are variables which determine if the user or AI/other player has won.
 
gameMode is a string value which determines what mode the user will play (AI/peer).

listOfChoices is a list which holds the list of choices in randomMove.

best_minimax_value is the greatest value that returns when applying minimax for o's turn
optimalMove is the move that is made when minimax algorithm determines the move for 'o'.

playerOneTurn and playerTwoTurn are boolean variables which determine the order in which the player
will go in peer vs peer games. Allows "x", aka player 1 to go first always.


"""

from tpge import *
import random

#WIDTH  = 640
#HEIGHT = 480


# Create a gamemode variable for gameMode
# Start it with the default game type of Peer vs. peer
global gameMode
gameMode = "peer"


global playerOneTurn
playerOneTurn = True

global playerTwoTurn
playerTwoTurn = False


global xWON
global yWON

xWON = False
yWON = False



def game_title():
    """
    game_title : String
    Returns the name of the game which is "Jarred Price ..... "
    """
 
    return "Jarred Price - Tic-Tac-Toe: 3 AI's and Peer Vs. Peer!"

def initial_state():
    """
    initial_state : State
    
    Returns the initial state of the game which is:
    boardState = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
    """
    boardState = ['-', '-', '-', '-', '-', '-', '-', '-', '-']

    global xWON
    global yWON
    
    xWON = False
    yWON = False
    
    global playerOneTurn
    playerOneTurn = True
    global playerTwoTurn
    playerTwoTurn = False
    
    return boardState

def images(S):
    """
    images : boardState -> Image List
    
    If S is a boardState, then images(S) is the list of Images that need to be
    drawn to the screen in order to present the boardState S to the user. For
    this game the images that need to be drawn are the background and
    the contents of the cells.
    """
    return background() +  contents(S)


def successor_state(boardState, point):
    """
    successor_state: boardState * point -> boardState
    
    If the piece is a boardState and the second param is a point, then successor_state(piece, point) is 
    the resulting boardState from clicking the point
    """

    global gameMode
    global playerOneTurn
    global playerTwoTurn
    

    
    justWent = False;
    
    cell = check_cell_location(point)
	
        
    if won(boardState, 'x') or won(boardState, 'o') or game_over(boardState):
        
        

        
        if cell == 9 or cell == 10 or cell == 11 or cell == 12:
            boardState = initial_state()
        return boardState
		
		

    # For battling computer AI
    if gameMode != "peer":
        if (cell >= 0 and cell <= 8):
            if boardState[cell] == '-':
                boardState[cell] = 'x'     
                if (not won(boardState, 'x') and (not game_over(boardState))):            
                    boardState = isComputerTurn(boardState)            
            return boardState

    # For battling peers
    if gameMode == "peer" and playerOneTurn == True:
        

        if (cell >= 0 and cell <= 8):
                if boardState[cell] == '-':
                    boardState[cell] = 'x'     
                    if (not won(boardState, 'x') and (not game_over(boardState))):
                        

                        #Denote that it is player 2's turn with
                        playerOneTurn = False
                        playerTwoTurn = True
                         # Denote that we just went, so do not go on to next check
                        justWent = True
                return boardState
        
    # For battling peers
    if gameMode == "peer" and playerTwoTurn == True and justWent == False:
      

        if (cell >= 0 and cell <= 8):
                if boardState[cell] == '-':
                    boardState[cell] = 'o'     
                    if (not won(boardState, 'o') and (not game_over(boardState))):
                        

                        #Denote that it is player 2's turn with
                        playerOneTurn = True
                        playerTwoTurn = False

                       
                return boardState

        
		
		
    # If cell is 9, then we are AI_hard
    if cell == 9:
        boardState = initial_state()
        gameMode = "hard"
        return boardState
    

    # If cell is 10, then we are AI_medium
    if cell == 10:
        boardState = initial_state()
        gameMode = "medium"
        return boardState

    # If cell is 11, then we are AI_easy
    if cell == 11:
        boardState = initial_state()
        gameMode = "easy"
        return boardState

    # If cell is 12, then we are peer vs. peer
    if cell == 12:
        boardState = initial_state()
        gameMode = "peer"
        return boardState


    # If cell is 13, then we start over
    if cell == 13:
        boardState = initial_state()
        gameMode = gameMode
        return boardState
 
   
def game_over(boardState):
    """
    game_over: boardState -> bool
    
    If the boardState is valid, then game_over(boardState) is true when there is not a '-' in piece.
    """
    if '-' in boardState:
        return False
    if '-' not in boardState:
        return True
 



def game_over2(boardState):
    """
    game_over2: boardState -> bool (false)
    
    This takes in the boardState and always returns False. It always returns false
    because this is fed into the Tiny Python Game Engine in order for the game to continuously function.
    Without this, the games would shut down when player X or O won.
    """
    return False

	
def check_cell_location(point):
    """
    check_cell_location : point -> cell
    
    If point is a valid point, then check_cell_location(point) is the cell of the point found and clicked upon.
    """

    x = point[0]
    y = point[1]

    if(100 <= x <= 200 and 300 <= y <= 400):
        cell = 0
       
    elif(200 <= x <= 300 and 300 <= y <= 400):
        cell = 1
       
    elif(300 <= x <= 400 and 300 <= y <= 400):
        cell = 2
     
    elif(100 <= x <= 200 and 200 <= y <= 300):
        cell = 3
       
    elif(200 <= x <= 300 and 200 <= y <= 300):
        cell = 4
      
    elif(300 <= x <= 400 and 200 <= y <= 300):
        cell = 5
       
    elif(100 <= x <= 200 and 100 <= y <= 200):
        cell = 6
      
    elif(200 <= x <= 300 and 100 <= y <= 200):
        cell = 7
  
    elif(300 <= x <= 400 and 100 <= y <= 200):
        cell = 8


      
    # Play HARD MODE tic-tac-toe
    elif(455 <= x <= 600 and 430 <= y <= 460):
        cell = 9
        print("HARD AI MODE SELECTED")

    # Play Moderate
    elif(455 <= x <= 600 and 330 <= y <= 360):
        cell = 10
        print("MEDIUM AI MODE SELECTED")

    # Play Easy
    elif(455 <= x <= 600 and 240 <= y <= 270):
        cell = 11
        print("EASY AI MODE SELECTED")

    # Play peer vs peer
    elif(455 <= x <= 600 and 130 <= y <= 160):
        cell = 12
        print("Peer vs Peer mode SELECTED")


    


    # Return boardState
    else:
        cell = 13


   
    return cell


def isComputerTurn(boardState):
    """
    isComputerTurn : boardState -> boardState
    
    If boardState is a valid state of the board, then it will return the new boardState after the computer has made their move. It follows the proper  
    decision on which computer AI move to make based on the Global gameMode string variable.
    """

    if gameMode == "hard":
        cell,score = minimax_max(boardState)
        boardState[cell] = 'o'
    if gameMode == "easy":
        cell = randomMove(boardState)
        boardState[cell] = 'o'
    if gameMode == "medium":
        cell = mediumMove(boardState)
        boardState[cell] = 'o'
    
    return boardState



def randomMove(boardState):
    """
    randomMove : boardState -> boardState
    
    If boardState is a valid state of the board, then it will 
    choose a random cell to populate and thus changing the boardState.
    """

    # List to hold all options
    listOfChoices = [];

    # Iterate through all choices
    for i in range(0,9):
        if boardState[i] == '-':
            listOfChoices.append(i);

            # If choice is valid and random
            cell = random.choice(listOfChoices)
            
    return cell

def mediumMove(boardState):
    """
    mediumMove : boardState -> boardState
    
    If boardState is a valid state of the board, then it will check to see if there is a position that the medium AI must block. If so, it will 
    choose that move and if there is not, it will choose a random cell to populate and thus changing the boardState.
    """

    # Acquire a randomMove
    cell = randomMove(boardState)
    
 # Now check to see if we need to change our move and block!
    
    # for 0, 1 and 2
    if(boardState[0] == 'x' and boardState[1] == 'x' and boardState[2] == '-'):
        cell = 2
    if(boardState[0] == 'x' and boardState[1] == '-' and boardState[2] == 'x'):
        cell = 1
    if(boardState[0] == '-' and boardState[1] == 'x' and boardState[2] == 'x'):
        cell = 0

    # for 3, 4 and 5
    if(boardState[3] == 'x' and boardState[4] == 'x' and boardState[5] == '-'):
        cell = 5
    if(boardState[3] == 'x' and boardState[4] == '-' and boardState[5] == 'x'):
        cell = 4
    if(boardState[3] == '-' and boardState[4] == 'x' and boardState[5] == 'x'):
        cell = 3

    # for 6, 7 and 8
    if(boardState[6] == 'x' and boardState[7] == 'x' and boardState[8] == '-'):
        cell = 8
    if(boardState[6] == 'x' and boardState[7] == '-' and boardState[8] == 'x'):
        cell = 7
    if(boardState[6] == '-' and boardState[7] == 'x' and boardState[8] == 'x'):
        cell = 6

    # for 0, 3 and 6
    if(boardState[0] == 'x' and boardState[3] == 'x' and boardState[6] == '-'):
        cell = 6
    if(boardState[0] == 'x' and boardState[3] == '-' and boardState[6] == 'x'):
        cell = 3
    if(boardState[0] == '-' and boardState[3] == 'x' and boardState[6] == 'x'):
        cell = 0


    # for 1, 4 and 7
    if(boardState[1] == 'x' and boardState[4] == 'x' and boardState[7] == '-'):
        cell = 7
    if(boardState[1] == 'x' and boardState[4] == '-' and boardState[7] == 'x'):
        cell = 4
    if(boardState[1] == '-' and boardState[4] == 'x' and boardState[7] == 'x'):
        cell = 1


    # for 2, 5 and 8
    if(boardState[2] == 'x' and boardState[5] == 'x' and boardState[8] == '-'):
        cell = 8
    if(boardState[2] == 'x' and boardState[5] == '-' and boardState[8] == 'x'):
        cell = 5
    if(boardState[2] == '-' and boardState[5] == 'x' and boardState[8] == 'x'):
        cell = 2

  # for 0, 4 and 8
    if(boardState[0] == 'x' and boardState[4] == 'x' and boardState[8] == '-'):
        cell = 8
    if(boardState[0] == 'x' and boardState[4] == '-' and boardState[8] == 'x'):
        cell = 4
    if(boardState[0] == '-' and boardState[4] == 'x' and boardState[8] == 'x'):
        cell = 0
        
  # for 2, 4, 6
    if(boardState[2] == 'x' and boardState[4] == 'x' and boardState[6] == '-'):
        cell = 6
    if(boardState[2] == 'x' and boardState[4] == '-' and boardState[6] == 'x'):
        cell = 4
    if(boardState[2] == '-' and boardState[4] == 'x' and boardState[6] == 'x'):
        cell = 2

    return cell

    
def minimax_max(boardState):
    """
    minimax_max : boardState -> optimalMove, best_minimax_value
    
    If the given cell is valid in the boardState, then minimax_max(boardState) will return the best_minimax value
    and the optimalMove in regards to player 'o' - the computer and it follows the minimax algorithm.
    """
    best_minimax_value = None
    optimalMove = None
    for states in range(0,9):
        if boardState[states] == '-':
            boardState[states] = 'o'
            if won(boardState,'x') or won(boardState,'o') or game_over(boardState):
                value = minMaxScore(boardState)
            else:
                cell,value = minimax_min(boardState)
            boardState[states] = '-'

            if best_minimax_value == None or value > best_minimax_value:
                best_minimax_value = value
                optimalMove = states
            
    return optimalMove, best_minimax_value

    
def minimax_min(boardState):
    """
    minimax_min : boardState -> optimalMove, best_minimax_value
    
    If the given cell is valid in the boardState, then minimax_min(boardState) will return the best_minimax value
    and the optimalMove in regards to player 'o' - the computer and it follows the minimax algorithm.
    """
    best_minimax_value = None
    optimalMove = None
    
    for states in range(0,9):
        if boardState[states] == '-':
            boardState[states] = 'x'
            if won(boardState,'x') or won(boardState,'o') or game_over(boardState):
                value = minMaxScore(boardState)
            else:
                cell,value = minimax_max(boardState)
            boardState[states] = '-'
        
            if best_minimax_value == None or value < best_minimax_value:
                best_minimax_value = value
                optimalMove = states
                
    return optimalMove, best_minimax_value

def minMaxScore(boardState):
    """
    minMaxScore : boardState -> best_minimax_value
    
    If the cell is a valid boardState, then minMaxScore(boardState) will return the value of the boardState
    in regards to player 'o' and it will follow the minimax algorithm.
    """
    if won(boardState,'x'):
        return 0
    elif game_over(boardState):
        return 5
    elif won(boardState,'o'):
        return 10

def won(boardState, piece):
    """
    won : boardState * piece -> bool
    
    Returns True if for the given boardState and piece if the boardState is found to be a winner for that
    given piece. If not, then it returns False
    """
    global xWON
    global yWON

    xWon = False
    yWon = False
    
    if ((boardState[0] == boardState[1] == boardState[2] == piece)
        or (boardState[3] == boardState[4] == boardState[5] == piece)
        or (boardState[6] == boardState[7] == boardState[8] == piece)
        or (boardState[0] == boardState[3] == boardState[6] == piece)
        or (boardState[1] == boardState[4] == boardState[7] == piece)
        or (boardState[2] == boardState[5] == boardState[8] == piece)
        or (boardState[0] == boardState[4] == boardState[8] == piece)
        or (boardState[2] == boardState[4] == boardState[6] == piece)):        

        if piece == 'x':
            xWON = True
        if piece == 'o':
            yWON = True
            
        return True
    return False

def background():
    """
    background : Image List
    
    Returns the Image List needed to display the background for the game.
    Draws the board, buttons, etc.
    """

    global xWON
    global yWON

    # Draws the tic tac toe squares
    VL1 = (200,400,200,100)
    VL2 = (300,400,300,100)
    VL3 = (100, 400, 100, 100)
    VL4 = (400, 400, 400, 100)
    HL1 = (100,200,400,200)
    HL2 = (100,300, 400, 300)
    HL3 = (100, 400, 400, 400)
    HL4 = (100, 100, 400, 100)
	
    # Draw buttons around boxes for game choice:
    pvp1 = (455,160, 600, 160)
    pvp2 = (455,130, 600, 130)
    pvp3 = (455,160, 455,130)
    pvp4 = (600,160,600,130)

    ez1 = (455, 270, 600, 270)
    ez2 = (455,240, 600,240)
    ez3 = (455,270, 455,240)
    ez4 = (600,270, 600, 240)

    mod1 = (455, 360, 600, 360)
    mod2 = (455, 330, 600, 330)
    mod3 = (455,360, 455,330)
    mod4 = (600, 360, 600, 330)

    hard1 = (455,460, 600, 460)
    hard2 = (455, 430, 600, 430)
    hard3 = (455,460, 455,430)
    hard4 = (600, 460, 600, 430)
   


    # Title, x pos, y pos, font size
    Peer = ("Peer Vs. Peer", 525, 145, 16)
    AI_hard = ("AI - Easy", 525, 255, 16)
    AI_medium = ("AI - Medium", 530, 345, 16)
    AI_easy = ("AI - Hard", 525, 445, 16)

    CURRENT_MODE = ("CURRENT MODE: " + gameMode, 500, 10, 15)
    WHO_WON = ("GAME IN PROGRESS!", 500, 50, 15)
   

    
    if xWON == True and gameMode != "hard":
        WHO_WON = ("X WON!", 500, 50, 15)
     
    if yWON == True and gameMode != "hard":
        WHO_WON = ("O WON!", 500, 50, 15)
      
    return [ WHO_WON, VL1,VL2,VL3,VL4, HL1,HL2, HL3, HL4, pvp1, pvp2, pvp3, pvp4, ez1, ez2, ez3, ez4,mod1, mod2 , mod3, mod4, hard1, hard2, hard3, hard4, Peer, AI_easy, AI_medium, AI_hard, CURRENT_MODE]



def contents(S):
    """
    contents : State -> displayer
    
    If S is a state, then contents(S) is the list of Images  of "X" and "O" needed to
    draw the contents of the cells in S.
    """
    displayer = []
    if S[0] == 'x':
        displayer.append(('X', 150,350,25))
        
    if S[0] == 'o':
        displayer.append(('O', 150,350,25))
        
    if  S[1] == 'x':
        displayer.append(('X', 250,350,25))
        
    if  S[1] == 'o':
        displayer.append(('O', 250,350,25))

    if  S[2] == 'x':
        displayer.append(('X', 350,350,25))
    if  S[2] == 'o':
        displayer.append(('O', 350,350,25))

    if  S[3] == 'x':
        displayer.append(('X', 150,250,25))
    if  S[3] == 'o':
        displayer.append(('O',150,250,25))

    if  S[4] == 'x':
        displayer.append(('X', 250,250,25))
        
    if S[4] == 'o':
        displayer.append(('O', 250,250,25))

    if  S[5] == 'x':
         displayer.append(('X',350,250,25))
      
    if  S[5] == 'o':
        displayer.append(('O', 350,250,25))

    if  S[6] == 'x':
        displayer.append(('X', 150,150,25))
    if S[6] == 'o':
        displayer.append(('O', 150,150,25))

    if  S[7] == 'x':
        displayer.append(('X', 250,150,25))
    if  S[7] == 'o':
        displayer.append(('O', 250,150,25))

    if  S[8] == 'x':
        displayer.append(('X', 350,150,25))
    if  S[8] == 'o':
        displayer.append(('O', 350,150,25))
    
    return displayer


if __name__ == "__main__":
    run_game(game_title, initial_state, successor_state, game_over2, images)
