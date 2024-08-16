import random

pieceScore = {"K": 0, "Q": 4, "R": 12, "B": 6, "N": 6, "p": 1, "T": 6}

whiteKnightScores =    [[1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
                        [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
                        [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
                        [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
                        [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
                        [1.2, 1, 1.2, 1, 1, 1.2, 1, 1.2],
                        [1, 1, 1, 1.2, 1.2, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1]]

blackKnightScores =    [[1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1.2, 1.2, 1, 1, 1],
                        [1.2, 1, 1.2, 1, 1, 1.2, 1, 1.2],
                        [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
                        [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
                        [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
                        [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
                        [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2]]

whiteBishopScores =    [[1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1],
                        [1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1],
                        [1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1],
                        [1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1],
                        [1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1],
                        [1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1],
                        [1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1]]

blackBishopScores =    [[1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1],
                        [1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1],
                        [1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1],
                        [1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1],
                        [1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1],
                        [1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1],
                        [1, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1]]

whiteRookScores =  [[1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]]

blackRookScores =  [[1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]]

whiteQueenScores = [[1.2, 1, 1.2, 1.2, 1, 1.2, 1, 1.2],
                    [1.2, 1, 1.2, 1.2, 1, 1.2, 1, 1.2],
                    [1.2, 1, 1.2, 1.2, 1, 1.2, 1, 1.2],
                    [1.2, 1, 1.2, 1.2, 1, 1.2, 1, 1.2],
                    [1.2, 1, 1.2, 1.2, 1, 1.2, 1, 1.2],
                    [1.2, 1, 1.2, 1, 1.2, 1, 1.2, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]]

blackQueenScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1.2, 1, 1.2, 1, 1.2, 1, 1.2, 1],
                    [1.2, 1, 1.2, 1.2, 1, 1.2, 1, 1.2],
                    [1.2, 1, 1.2, 1.2, 1, 1.2, 1, 1.2],
                    [1.2, 1, 1.2, 1.2, 1, 1.2, 1, 1.2],
                    [1.2, 1, 1.2, 1.2, 1, 1.2, 1, 1.2],
                    [1.2, 1, 1.2, 1.2, 1, 1.2, 1, 1.2],]

whitePawnScores =  [[1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1.33, 1.33, 1.33, 1.33, 1.33, 1.33, 1.33, 1.33],
                    [1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3],
                    [1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]]

blackPawnScores =  [[1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
                    [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
                    [1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]]

whiteKingScores =  [[1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1.2, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]]

blackKingScores =  [[1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1.2, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]]

whitePawnpScore =  [[1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]]

blackPawnpScore =  [[1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1]]

piecePositionScores = {"wN": whiteKnightScores, "wB": whiteBishopScores, "wR": whiteRookScores, "wQ": whiteQueenScores, "wp": whitePawnScores, "wK": whiteKingScores, "wT": whitePawnpScore,
                      "bN": blackKnightScores, "bB": blackBishopScores, "bR": blackRookScores, "bQ": blackQueenScores, "bp": blackPawnScores, "bK": blackKingScores, "bT": blackPawnpScore
                    }

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3


# Level 0
def finRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentsMinMaxScore = CHECKMATE
    bestPlayerMove = None 
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.staleMate:
            opponentsMaxScore = STALEMATE
        elif gs.checkMate:
            opponentsMaxScore = -CHECKMATE
        else:
            opponentsMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentsMaxScore:
                    opponentsMaxScore = score
                gs.undoMove()
        if opponentsMaxScore < opponentsMinMaxScore:
            opponentsMinMaxScore = opponentsMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove

# Level 1
def findBestMoveMinMax(gs, validMoves):
    '''
    Helper method to make recursive call
    '''

    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

# Level 2
def findbestMoveNegaMax(gs, validMoves):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves  = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth -1 , -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

# Level 3
def findbestMoveNegaMaxAlphaBeta(gs, validMoves):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    # print(counter)
    return nextMove

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    #move ordering - implement later
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves  = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth -1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha: #prunning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

'''
A positive score is good for white, a negative score is good for black
''' 
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE # black wins
        else: 
            return CHECKMATE # white wins
    elif gs.staleMate:
        return STALEMATE
    
    score = 0 
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                #score it possitionaly
                piecePositionScore = 0
                piecePositionScore = piecePositionScores[square][row][col]

                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore * 0.1
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore * 0.1
   
    return score

def scoreMaterial(board):
    score = 0 
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score
