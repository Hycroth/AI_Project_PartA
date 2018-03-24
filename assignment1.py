#File name: assignment1.py
#Author: Samuel Fatone, Ckyever Gaviola
#Date created: 17/03/2018
#Date last modified: 23/03/2018
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
        for k in range(BOARD_LENGTH):
            for m in range(BOARD_WIDTH):
                if (abs(k-i) + abs(m-j) == depth):
                    if (gameboard[k][m] == 'O'):
                        closest_piece.append(k)
                        closest_piece.append(m)
                        if len(closest_piece) >=4:
                            return closest_piece
        depth += 1
        
#Moves the white piece (i,j) to (k,m) and returns the new gameboard
def update_gameboard(i, j, k, m, gameboard):
    temp = gameboard
    temp[i][j] = '-'
    temp[k][m] = 'O'
    return temp
    
#Returns true if moving piece a piece to (i,j) is legal
def is_legalsquare(i, j, gameboard):
    #Check square is empty, not a corner square and within boundaries of board
    if (TOP_BORDER <= i <= BOTTOM_BORDER and LEFT_BORDER <= j <= RIGHT_BORDER and gameboard[i][j] == '-'):
        return True
    else:
        return False
    
#Returns true if the current piece (i,j) is surrounded
def is_eliminated(piece,gameboard):
    piece = gameboard[Piece.icoord][Piece.jcoord]
    
    if (piece == 'O'):
        #Check elimination vertically
        if ((i-1)>=TOP_BORDER and (i+1)<=BOTTOM_BORDER): #Prevents IndexError
            top_piece = gameboard[i-1][j]
            bot_piece = gameboard[i+1][j]
            if ((top_piece == '@' or top_piece == 'X') and (bot_piece == '@' or bot_piece == 'X')):
                return True
        #Check elimination horizontally
        elif ((j-1)>=LEFT_BORDER and (j+1)<=RIGHT_BORDER):
            left_piece = gameboard[i][j-1]
            right_piece = gameboard[i][j+1]
            if ((left_piece == '@' or left_piece == 'X') and (right_piece == '@' or right_piece == 'X')):
                return True
    #Repeat for black piece
    elif (piece == '@'):
        if ((i-1)>=TOP_BORDER and (i+1)<=BOTTOM_BORDER):
            top_piece = gameboard[i-1][j]
            bot_piece = gameboard[i+1][j]
            if ((top_piece == 'O' or top_piece == 'X') and (bot_piece == 'O' or bot_piece == 'X')):
                return True
        elif ((j-1)>=LEFT_BORDER and (j+1)<=RIGHT_BORDER):
            left_piece = gameboard[i][j-1]
            right_piece = gameboard[i][j+1]
            if ((left_piece == 'O' or left_piece == 'X') and (right_piece == 'O' or right_piece == 'X')):
                return True
    else:
        return False
    
#Recursive depth-limited search
def DLS(node, depth, gameboard):
    if (depth == 0 and is_eliminated(node.blackpiece,gameboard)):
        return node
    if depth > 0:
        for child in node.children:
            result = DLS(child, depth-1)
            if (result != None):
                return result
    return None

#Iterative deepening search
def IDS(tree):
    depth = 0
    while(True):
        result = DLS(tree.root, depth, gameboard)
        if result != None:
            return result
        depth += 1
        # Expand next layer of tree
        tree.expand_tree

class Piece:
    def __init__(self, icoord, jcoord, colour):
        self.icoord = icoord    #Row number
        self.jcoord = jcoord    #Column number
        self.colour = colour
    
#Node holding location of black piece and the two closest white pieces
class Node:
    def __init__(self, blackpiece, whitepiece1, whitepiece2):
        self.blackpiece = blackpiece
        self.whitepiece1 = whitepiece1
        self.whitepiece2 = whitepiece2
        self.children = []
        
    def add_child(self, node):
        self.children.append(node)
        
#Tree containing the possible sequence of moves to eliminate a black piece
#using two white pieces
class Tree:
    def __init__(self, root=None):
        self.root = root
        self.expand_tree        

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

#Figure 2
#gameboard = [['X', '-', '-', '-', '-', '-', '-', 'X'], 
#             ['-', '-', '-', '-', '-', '-', '-', '-'], 
#             ['-', '-', '-', '-', '-', 'O', 'O', '-'], 
#             ['-', '-', '-', '-', '@', 'O', '-', '-'], 
#             ['-', '-', '-', '-', '-', '-', '-', '-'], 
#             ['-', '-', '-', '-', '-', 'O', '-', '-'], 
#             ['-', '-', '-', '-', '@', '-', '@', '@'], 
#             ['X', '-', '-', '-', '-', '-', '-', 'X']]

#Figure 3
gameboard = [['X', '-', '-', '-', '-', '-', '-', 'X'], 
             ['-', '-', '-', '-', '-', '-', '-', '-'], 
             ['-', '-', '-', '-', '-', 'O', '-', '-'], 
             ['-', '-', '-', '-', '@', 'O', '-', '-'], 
             ['-', '-', '-', '-', '-', '-', 'O', '-'], 
             ['-', '-', '-', '-', '-', 'O', '@', '-'], 
             ['-', '-', '-', '-', '-', '-', '-', '@'], 
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
                black_piece = Piece(i,j,enemy_icon)
                white_pieces = closest_pieces(i,j,gameboard)
                white1 = Piece(white_pieces[0], white_pieces[1], player_icon)
                white2 = Piece(white_pieces[2], white_pieces[3], player_icon)                
                #Create search tree of possible moves for two closest white pieces
                #Each move must bring it closer or remain the same distance to black piece