#File name: assignment1.py
#Author: Samuel Fatone, Ckyever Gaviola
#Date created: 17/03/2018
#Date last modified: 26/03/2018
#Python Version: 3.6

#Debug
#import pdb

import copy

#Constants
BOARD_LENGTH = 8
BOARD_WIDTH = 8
TOP_BORDER = 0
BOTTOM_BORDER = 7
LEFT_BORDER = 0
RIGHT_BORDER = 7
BLACK = '@'
WHITE = 'O'
EMPTY = '-'
CORNER = 'X'
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

class Piece:
    def __init__(self,icoord,jcoord,colour,eliminate=False):
        self.i = icoord             #Row number
        self.j = jcoord             #Column number
        self.colour = colour        #'@' or 'O'
        
class Gameboard:
    def __init__(self,gameboard):
        self.board = gameboard
        
    #Returns true if coordinates land inside the board
    def in_board(self,i,j):
        return (TOP_BORDER <= i <= BOTTOM_BORDER) and (LEFT_BORDER <= j <= RIGHT_BORDER)
            
    #Returns true if coordinates are empty and not a corner square
    def is_empty(self,i,j):
        return self.in_board(i,j) and (self.board[i][j] == EMPTY)
    
    #Returns true if coordinates contain a player piece
    def is_piece(self,i,j):
        return self.in_board(i,j) and (self.board[i][j] == BLACK or self.board[i][j] == WHITE)
    
    #Moves piece (i,j) to (k,m), checks for eliminations, then returns updated board
    def update_board(self,oldboard,i,j,k,m):

        newboard = Gameboard(copy.deepcopy(oldboard))
        temp = newboard.board[i][j]
        newboard.board[i][j] = EMPTY
        newboard.board[k][m] = temp
        
        #Check surroundings of where the new piece has moved for eliminations
        if newboard.is_elim(k-1,m):         #Square above
            newboard.board[k-1][m] = EMPTY
        if newboard.is_elim(k+1,m):         #Square below
            newboard.board[k+1][m] = EMPTY
        if newboard.is_elim(k,m-1):         #Square on left
            newboard.board[k][m-1] = EMPTY
        if newboard.is_elim(k,m+1):         #Square on right
            newboard.board[k][m+1] = EMPTY
        #Now check if current piece has been eliminated
        if newboard.is_elim(i,j):
            newboard.board[i][j] = EMPTY
        return newboard   
    
    #Returns true if piece (i,j) exists and is surrounded
    def is_elim(self,i,j):
        if not self.is_piece(i,j):
            return False
        #Identify the enemy colour
        piece = self.board[i][j]
        if (piece == BLACK):
            enemy = WHITE
        elif (piece == WHITE):
            enemy = BLACK
        #Check if surrounded vertically
        if ((i-1)>=TOP_BORDER and (i+1)<=BOTTOM_BORDER): #Prevents IndexError
            top_piece = self.board[i-1][j]
            bot_piece = self.board[i+1][j]
            if ((top_piece == enemy or top_piece == CORNER) and (bot_piece == enemy or bot_piece == CORNER)):
                return True
        #Check if surrounded horizontally
        if ((j-1)>=LEFT_BORDER and (j+1)<=RIGHT_BORDER):
            left_piece = self.board[i][j-1]
            right_piece = self.board[i][j+1]
            if ((left_piece == enemy or left_piece == CORNER) and (right_piece == enemy or right_piece == CORNER)):
                return True
        
        return False
    
    #Returns updated board if move is possible and None otherwise
    def move(self,gameboard,i,j,direction,jump):
        #Confirm coordinates give a piece
        if self.is_piece(i,j):
            if direction==UP:
                if jump and (self.is_piece(i-1,j) and self.is_empty(i-2,j)):
                    return self.update_board(gameboard,i,j,i-2,j)
                elif not jump and self.is_empty(i-1,j):
                    return self.update_board(gameboard,i,j,i-1,j)
            elif direction==DOWN:
                if jump and (self.is_piece(i+1,j) and self.is_empty(i+2,j)):
                    return self.update_board(gameboard,i,j,i+2,j)
                elif not jump and self.is_empty(i+1,j):
                    return self.update_board(gameboard,i,j,i+1,j)
            elif direction==LEFT:
                if jump and (self.is_piece(i,j-1) and self.is_empty(i,j-2)):
                    return self.update_board(gameboard,i,j,i,j-2)
                elif not jump and self.is_empty(i,j-1):
                    return self.update_board(gameboard,i,j,i,j-1)
            elif direction==RIGHT:
                if jump and (self.is_piece(i,j+1) and self.is_empty(i,j+2)):
                    return self.update_board(gameboard,i,j,i,j+2)
                elif not jump and self.is_empty(i,j+1):
                    return self.update_board(gameboard,i,j,i,j+1)
        
        return None
        
#Node
class Node:
    def __init__(self,blackpiece,whitepiece1,whitepiece2,gameboard):
        self.bp = blackpiece
        self.wp1 = whitepiece1
        self.wp2 = whitepiece2
        self.board = gameboard
        self.children = []
        self.parent = None      #Allow us to traverse back up
        
    def add_child(self,node):
        self.children.append(node)
        node.parent = self
        
    #Compares position of white pieces between current node and parent, returns
    #the move as a list [start.i,start.j,end.i,end.j]
    def find_move(self):
        #No parent so this is the root
        if self.parent == None:
            return None
        #Whitepiece1 was moved
        elif (self.wp1.i != self.parent.wp1.i) or (self.wp1.j != self.parent.wp1.j):
            return [self.parent.wp1.i,self.parent.wp1.j,self.wp1.i,self.wp1.j]
        #Whitepiece2 was moved
        elif (self.wp2.i != self.parent.wp2.i) or (self.wp2.j != self.parent.wp2.j):
            return [self.parent.wp2.i,self.parent.wp2.j,self.wp2.i,self.wp2.j]
            
#Tree
class Tree:
    def __init__(self,root):
        self.root = root
    
    #Returns a list of leaf nodes by recurrsion
    def find_leaves(self,node):
        leaf_nodes = []
        #Node has no children
        if not node.children:
            leaf_nodes.append(node)
        else:
            for child in node.children:
                leaf_nodes.extend(self.find_leaves(child))
        return leaf_nodes
    
    #Expands the tree by depth 1
    def expand(self):        
        leaves = self.find_leaves(self.root)
        
        #For each leaf node, attempt to create children with possible moves
        #Node will not be added if move results in a whitepiece being eliminated
        for node in leaves:
            
            wp1 = copy.deepcopy(node.wp1)
            wp2 = copy.deepcopy(node.wp2)
            oldboard = copy.deepcopy(node.board.board)
            
            # Move whitepiece1 up?
            newboard = node.board.move(oldboard,wp1.i,wp1.j,UP,False)
            if newboard != None and newboard.board[node.wp1.i-1][node.wp1.j] != EMPTY:
                node.add_child(Node(node.bp,Piece(wp1.i-1,wp1.j,WHITE),node.wp2,newboard))
            # Jump whitepiece1 up?
            newboard = node.board.move(oldboard,wp1.i,wp1.j,UP,True)
            if newboard != None and newboard.board[node.wp1.i-2][node.wp1.j] != EMPTY:
                node.add_child(Node(node.bp,Piece(wp1.i-2,wp1.j,WHITE),node.wp2,newboard))
            # Move whitepiece1 down?
            newboard = node.board.move(oldboard,wp1.i,wp1.j,DOWN,False)
            if newboard != None and newboard.board[node.wp1.i+1][node.wp1.j] != EMPTY:
                node.add_child(Node(node.bp,Piece(wp1.i+1,wp1.j,WHITE),node.wp2,newboard))
            # Jump whitepiece1 down?
            newboard = node.board.move(oldboard,wp1.i,wp1.j,DOWN,True)
            if newboard != None and newboard.board[node.wp1.i+2][node.wp1.j] != EMPTY:
                node.add_child(Node(node.bp,Piece(wp1.i+2,wp1.j,WHITE),node.wp2,newboard))
            # Move whitepiece1 left?
            newboard = node.board.move(oldboard,wp1.i,wp1.j,LEFT,False)
            if newboard != None and newboard.board[node.wp1.i][node.wp1.j-1] != EMPTY:
                node.add_child(Node(node.bp,Piece(wp1.i,wp1.j-1,WHITE),node.wp2,newboard))
            # Jump whitepiece1 left?
            newboard = node.board.move(oldboard,wp1.i,wp1.j,LEFT,True)
            if newboard != None and newboard.board[node.wp1.i][node.wp1.j-2] != EMPTY:
                node.add_child(Node(node.bp,Piece(wp1.i,wp1.j-2,WHITE),node.wp2,newboard))
            # Move whitepiece1 right?
            newboard = node.board.move(oldboard,wp1.i,wp1.j,RIGHT,False)
            if newboard != None and newboard.board[node.wp1.i][node.wp1.j+1] != EMPTY:
                node.add_child(Node(node.bp,Piece(wp1.i,wp1.j+1,WHITE),node.wp2,newboard))
            # Jump whitepiece1 right?
            newboard = node.board.move(oldboard,wp1.i,wp1.j,RIGHT,True)
            if newboard != None and newboard.board[node.wp1.i][node.wp1.j+2] != EMPTY:
                node.add_child(Node(node.bp,Piece(wp1.i,wp1.j+2,WHITE),node.wp2,newboard))
            # Move whitepiece2 up?
            newboard = node.board.move(oldboard,wp2.i,wp2.j,UP,False)
            if newboard != None and newboard.board[node.wp2.i-1][node.wp2.j] != EMPTY:
                node.add_child(Node(node.bp,node.wp1,Piece(wp2.i-1,wp2.j,WHITE),newboard))
            # Jump whitepiece2 up?
            newboard = node.board.move(oldboard,wp2.i,wp2.j,UP,True)
            if newboard != None and newboard.board[node.wp2.i-2][node.wp2.j] != EMPTY:
                node.add_child(Node(node.bp,node.wp1,Piece(wp2.i-2,wp2.j,WHITE),newboard))
            # Move whitepiece2 down?
            newboard = node.board.move(oldboard,wp2.i,wp2.j,DOWN,False)
            if newboard != None and newboard.board[node.wp2.i+1][node.wp2.j] != EMPTY:
                node.add_child(Node(node.bp,node.wp1,Piece(wp2.i+1,wp2.j,WHITE),newboard))
            # Jump whitepiece2 down?
            newboard = node.board.move(oldboard,wp2.i,wp2.j,DOWN,True)
            if newboard != None and newboard.board[node.wp2.i+2][node.wp2.j] != EMPTY:
                node.add_child(Node(node.bp,node.wp1,Piece(wp2.i+2,wp2.j,WHITE),newboard))
            # Move whitepiece2 left?
            newboard = node.board.move(oldboard,wp2.i,wp2.j,LEFT,False)
            if newboard != None and newboard.board[node.wp2.i][node.wp2.j-1] != EMPTY:
                node.add_child(Node(node.bp,node.wp1,Piece(wp2.i,wp2.j-1,WHITE),newboard))
            # Jump whitepiece2 left?
            newboard = node.board.move(oldboard,wp2.i,wp2.j,LEFT,True)
            if newboard != None and newboard.board[node.wp2.i][node.wp2.j-2] != EMPTY:
                node.add_child(Node(node.bp,node.wp1,Piece(wp2.i,wp2.j-2,WHITE),newboard))
            # Move whitepiece2 right?
            newboard = node.board.move(oldboard,wp2.i,wp2.j,RIGHT,False)
            if newboard != None and newboard.board[node.wp2.i][node.wp2.j+1] != EMPTY:
                node.add_child(Node(node.bp,node.wp1,Piece(wp2.i,wp2.j+1,WHITE),newboard))
            # Jump whitepiece2 right?
            newboard = node.board.move(oldboard,wp2.i,wp2.j,RIGHT,True)
            if newboard != None and newboard.board[node.wp2.i][node.wp2.j+2] != EMPTY:
                node.add_child(Node(node.bp,node.wp1,Piece(wp2.i,wp2.j+2,WHITE),newboard))
    
#Recursive depth-limited search
def DLS(node, depth, gameboard):
    #Goal reached: black piece has been eliminated
    if (depth == 0 and gameboard.board[node.bp.i][node.bp.j] == EMPTY):
        return node
    if depth > 0:
        for child in node.children:
            result = DLS(child, depth-1,child.board)
            if (result != None):
                return result
    return None

#Iterative deepening search
def IDS(tree,gameboard):
    depth = 0
    while(True):
        result = DLS(tree.root, depth, gameboard)
        if result != None:
            return result
        depth += 1
        #Expand the tree by depth 1 to continue searching
        tree.expand()
        
#Returns coordinates [x1, y1, x2, y2] of the two white pieces closest to (i,j)
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
        
#Prints moves in the correct format
def print_moves(movelist):
    movelist.reverse()
    for move in movelist:
        print('({}, {}) -> ({}, {})'.format(move[1],move[0],move[3],move[2]))

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

#Figure 2 for Moves
#gameboard = [['X', '-', '-', '-', '-', '-', '-', 'X'], 
#             ['-', '-', '-', '-', '-', '-', '-', '-'], 
#             ['-', '-', '-', '-', '-', 'O', 'O', '-'], 
#             ['-', '-', '-', '-', '@', 'O', '-', '-'], 
#             ['-', '-', '-', '-', '-', '-', '-', '-'], 
#            ['-', '-', '-', '-', '-', 'O', '-', '-'], 
#             ['-', '-', '-', '-', '@', '-', '@', '@'], 
#             ['X', '-', '-', '-', '-', '-', '-', 'X']]

#Figure 3 for Massacre
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
    
    #To utilise Gameboard methods
    thegameboard = Gameboard(gameboard)
    
    #Iterate through board finding all black pieces
    for i in range(BOARD_LENGTH):
        for j in range(BOARD_WIDTH):
            #Found black piece
            if thegameboard.board[i][j] == BLACK:
                bp = Piece(i,j,BLACK)
                #Find the two closest white pieces
                closewhites = closest_pieces(i, j, thegameboard.board)
                wp1 = Piece(closewhites[0],closewhites[1],WHITE)
                wp2 = Piece(closewhites[2],closewhites[3],WHITE)
                #Initialise search tree for possible moves
                tree = Tree(Node(bp,wp1,wp2,thegameboard))
                #Find the final move node
                node = IDS(tree,thegameboard)
                #Update the gameboard
                thegameboard = node.board
                #Traverse back up from the goal node and record each move
                moves = []
                while(True):
                    #We've hit the root so stop
                    if node.parent == None:
                        break
                    #Add move to list and get the parent node
                    moves.append(node.find_move())
                    node = node.parent
                    
                #Print in reverse order since traversal started from last move
                print_moves(moves)