#File name: assignment1.py
#Author: Samuel Fatone, Ckyever Gaviola
#Date created: 17/03/2018
#Date last modified: 22/03/2018
#Python Version: 3.6

#Constants
BOARD_LENGTH = 8
BOARD_WIDTH = 8
TOP_BORDER = 0
BOTTOM_BORDER = 7
LEFT_BORDER = 0
RIGHT_BORDER = 7

#Returns coordinates [x1, y1, x2, y2] of the two closest white pieces to (i,j)
def closest_pieces(i, j, gameboard):
    closest_piece = []
    depth = 1
    while (len(closest_piece) < 4):
        for k in range(8):
            for m in range(8):
                if (abs(k-i) + abs(m-j) == depth):
                    if (gameboard[k][m] == 'O'):
                        closest_piece.append(k)
                        closest_piece.append(m)
                        if len(closest_piece) >=4:
                            return closest_piece
        depth += 1

#Initialises the game board as a list
gameboard = []

#Reads through each line of input, and adds the characters to a separate list,
#which is then added to the game board list
#for i in range(BOARD_LENGTH):
#    oneline = []
#    line = str(input())
#    for j in range(0,15,2):
#        oneline.append(line[j])
#    gameboard.append(oneline)
#    oneline.clear

gameboard = [['X', '-', '-', '-', '-', '-', '-', 'X'], 
             ['-', '-', '-', '-', '-', '-', '-', '-'], 
             ['-', '-', '-', '-', '-', 'O', 'O', '-'], 
             ['-', '-', '-', '-', '@', 'O', '-', '-'], 
             ['-', '-', '-', '-', '-', '-', '-', '-'], 
             ['-', '-', '-', '-', '-', 'O', '-', '-'], 
             ['-', '-', '-', '-', '@', '-', '@', '@'], 
             ['X', '-', '-', '-', '-', '-', '-', 'X']]

#Takes the user command, either 'Moves' or 'Massacre'
command = str(input())

#Sets the first icon to be counted as white, and the enemy as black
player_icon = 'O'
enemy_icon = '@'

if command == "Moves":
    
    #Will run through loop twice; once for each colour
    while(1):
        tally = 0
        
        #Checks each square of the gameboard for the player icon
        for i in range(BOARD_LENGTH):
            for j in range(BOARD_WIDTH):
                if gameboard[i][j] == player_icon:
                    #Can the piece move up?
                    if (i!=TOP_BORDER):
                        if (gameboard[i-1][j] == '-') :
                            tally += 1
                        #Can the piece move up by jumping?
                        if i!=TOP_BORDER+1 and (gameboard[i-1][j] == 'O' or gameboard[i-1][j] == '@'):
                            if (gameboard[i-2][j] == '-'):
                                tally += 1
                    #Can the piece move down?
                    if (i!=BOTTOM_BORDER):
                        if (gameboard[i+1][j] == '-') :
                            tally += 1
                        #Can the piece move down by jumping?
                        if i!=BOTTOM_BORDER-1 and (gameboard[i+1][j] == 'O' or gameboard[i+1][j] == '@'):
                            if (gameboard[i+2][j] == '-'):
                                tally += 1
                    #Can the piece move left?
                    if (j!=LEFT_BORDER):
                        if (gameboard[i][j-1] == '-') :
                            tally += 1
                        #Can the piece move left by jumping?
                        if j!=LEFT_BORDER+1 and (gameboard[i][j-1] == 'O' or gameboard[i][j-1] == '@'):
                            if (gameboard[i][j-2] == '-'):
                                tally += 1
                    #Can the piece move right?
                    if (j!=RIGHT_BORDER):
                        if (gameboard[i][j+1] == '-') :
                            tally += 1
                        #Can the piece move right by jumping?
                        if j!=RIGHT_BORDER-1 and (gameboard[i][j+1] == 'O' or gameboard[i][j+1] == '@'):
                            if (gameboard[i][j+2] == '-'):
                                tally += 1
                                
        #Prints the number of possible moves for the player
        print(tally)
        
        #Swaps to the second player after the first iteration, or breaks the loop otherwise
        if (player_icon == 'O'):
            player_icon = '@'
            enemy_icon = 'O'
        else:
            break
        
elif command == "Massacre":
    
    #Iterate through board finding all black pieces
    for i in range(BOARD_LENGTH):
        for j in range(BOARD_WIDTH):
            #Found a black piece
            if gameboard[i][j] == enemy_icon:
                white_pieces = closest_pieces(i,j,gameboard)
                print(white_pieces)