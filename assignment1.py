# File name: assignment1.py
# Author: Samuel Fatone, Ckyever Gaviola
# Date created: 17/03/2018
# Date last modified: 19/03/2018
# Python Version: 3.6

#Initialises the game board as a list
gameboard = []

#Reads through each line of input, and adds the characters to a separate list,
#which is then added to the game board list
for i in range(8):
    oneline = []
    line = str(input())
    for j in range(0,15,2):
        oneline.append(line[j])
    gameboard.append(oneline)
    oneline.clear

#gameboard = [['X', '-', '-', '-', '-', '-', '-', 'X'], 
#             ['-', '-', '-', '-', '-', '-', '-', '-'], 
#             ['-', '-', '-', '-', '-', 'O', 'O', '-'], 
#             ['-', '-', '-', '-', '@', 'O', '-', '-'], 
#             ['-', '-', '-', '-', '-', '-', '-', '-'], 
#             ['-', '-', '-', '-', '-', 'O', '-', '-'], 
#             ['-', '-', '-', '-', '@', '-', '@', '@'], 
#             ['X', '-', '-', '-', '-', '-', '-', 'X']]

#Takes the user command, either 'Moves' or 'Massacre'
command = str(input())

if command == "Moves":
    
    #Sets the first icon to be counted as white, and the enemy as black
    player_icon = 'O'
    enemy_icon = '@'
    
    #Will run through loop twice; once for each colour
    while(1):
        tally = 0
        
        #Checks each square of the gameboard for the player icon
        for i in range(8):
            for j in range(8):
                if gameboard[i][j] == player_icon:
                    #Can the piece move up?
                    if (i!=0):
                        if (gameboard[i-1][j] == '-') :
                            tally += 1
                        #Can the piece move up by jumping?
                        if i!=1 and (gameboard[i-1][j] == 'O' or gameboard[i-1][j] == '@'):
                            if (gameboard[i-2][j] == '-'):
                                tally += 1
                    #Can the piece move down?
                    if (i!=7):
                        if (gameboard[i+1][j] == '-') :
                            tally += 1
                        #Can the piece move down by jumping?
                        if i!=6 and (gameboard[i+1][j] == 'O' or gameboard[i+1][j] == '@'):
                            if (gameboard[i+2][j] == '-'):
                                tally += 1
                    #Can the piece move left?
                    if (j!=0):
                        if (gameboard[i][j-1] == '-') :
                            tally += 1
                        #Can the piece move left by jumping?
                        if j!=1 and (gameboard[i][j-1] == 'O' or gameboard[i][j-1] == '@'):
                            if (gameboard[i][j-2] == '-'):
                                tally += 1
                    #Can the piece move right?
                    if (j!=7):
                        if (gameboard[i][j+1] == '-') :
                            tally += 1
                        #Can the piece move right by jumping?
                        if j!=6 and (gameboard[i][j+1] == 'O' or gameboard[i][j+1] == '@'):
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