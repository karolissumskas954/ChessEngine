import random

pieceScores = {"K" : 0, "Q" : 10, "R" : 5, "B" : 3, "N" : 3, "p" : 1}
CHEKMATE = 1000
STALEMATE = 0
DEPTH = 2

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)] # Inclusive for both parameters

'''
Greedy algorithm
'''
def findGreedyMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHEKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        opponentMaxScore = -CHEKMATE
        for opponentsMove in opponentsMoves:
            gs.makeMove(opponentsMove)
            if gs.checkMate:
                score = -turnMultiplier * CHEKMATE
            elif gs.staleMate:
                score = STALEMATE
            else:
                score = -turnMultiplier * scoreMaterial(gs.board)
            if score > opponentMaxScore:
                opponentMaxScore = score
            gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore :
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove

'''
Helper method to make first recursive call
'''
def findBestMove(gs, validMoves):
    global nextMove
    global counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHEKMATE, CHEKMATE, 1 if gs.whiteToMove else -1)
    # print(counter)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHEKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth -1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHEKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth -1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore
    
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHEKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore: # Possible solution -> score = max(score, maxScore), but it doesnt tell if there is new max
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore
    

'''

'''
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    global counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    # Move ordering TODO



    maxScore = -CHEKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore: # Possible solution -> score = max(score, maxScore), but it doesnt tell if there is new max
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha: # Pruning
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore
    
    
'''
Positive = White is winning, Negative = Black is winning
'''
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHEKMATE # Black wins
        else:
            return CHEKMATE # White wins
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScores[square[1]]
            elif square[0] == 'b':
                score -= pieceScores[square[1]]
    return score

'''
Score the board based on material.
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScores[square[1]]
            elif square[0] == 'b':
                score -= pieceScores[square[1]]
    return score