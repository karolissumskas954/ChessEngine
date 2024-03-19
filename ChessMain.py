"""
Main driver file. 
Handles user input and displays the current GameState object.
"""

import pygame as p
from ChessEngine import GameState
from ChessEngine import Move

# p.init()
WIDTH = HEIGHT = 512 #400 another option
DIMENSION = 8 #Chess boards id 8x8
SQ_SIZE = HEIGHT // DIMENSION #Square size
MAX_FPS = 15 #For animations
IMAGES = {}

'''
Initialize a global dictionary of Images. Will be called once in main.
'''

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

"""
Main driver, handle user input and updating the graphics.
"""
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # Flag variable when move is made

    loadImages() #Do this once before While loop
    running = True
    sqSelected = () #No square is selected (tuple: (row, column))
    playerClicks = [] #Player clicks (two tuples: [(6,4), (4,4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col): # USER CLICKED THE SAME SQUARE TWICE
                    sqSelected = ()
                    playerClicks = []
                else :
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                if len(playerClicks) == 2: #after 2nd click
                    # if gs.board[playerClicks[0][0]][playerClicks[0][1]] == "--":
                    #     print("Move is canceled")
                    #     sqSelected = ()  # Reset the sqSelected value.
                    #     playerClicks = []  # Reset the playerClicks list.
                    # else:
                        move = Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True
                        sqSelected = () #reset user clicks
                        playerClicks = []
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True


        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Responsible for all the graphics with current game state.
'''
def drawGameState(screen, gs):
    drawBoard(screen) #Draw squares on board
    #Add piece highlighting
    drawPieces(screen, gs.board) #draw pieces on top of squares


def drawBoard(screen):
    colors = [(204,204,204), (127,127,127)]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
           color = colors[((row + column) % 2)]
           p.draw.rect(screen, color, p.Rect(column*SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--": #Not empty
                screen.blit(IMAGES[piece], p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
