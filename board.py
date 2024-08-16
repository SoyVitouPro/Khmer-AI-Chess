import copy

class Gamestate():
    def __init__(self):
        self.reset()
        self.pieceScores = {'p': 1, 'N': 5, 'B': 5, 'R': 9, 'Q': 3, 'T': 3, 'K': 1000}

    def reset(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR"]]
        self.current_board = self.board.copy()
        self.moveFunctions = {
            "p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
            "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves, "T": self.getPawnPromotionMoves
        }
        
        # self.possibleMoveLog = []
        self.moveLog = []
        self.boardLog = [] # List to store current board move
        
        self.whiteToMove = True

        self.whiteKingLocation = (7, 3)
        self.blackKingLocation = (0, 4)

        self.whiteQueenLocation = (7, 4)
        self.blackQueenLocation = (0, 3)

        self.checkMate = False
        self.staleMate = False

        # King Castling
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
        # Queen Castling
        self.currentQueenCastlingRight = CastleQueenRights(True, True, True, True)
        self.QueencastleRightsLog = [CastleQueenRights(self.currentQueenCastlingRight.wks, self.currentQueenCastlingRight.bks,
                                                       self.currentQueenCastlingRight.wqs, self.currentQueenCastlingRight.bqs)]

        # Conditions for disallowing castling
        self.whiteKingInCheck = False
        self.blackKingInCheck = False
        self.whiteKingRookColumn = False
        self.blackKingRookColumn = False

        self.moveCout = 0
    
    def copy(self):
        new_gamestate = Gamestate()
        new_gamestate.board = copy.deepcopy(self.board)
        new_gamestate.current_board = copy.deepcopy(self.current_board)
        new_gamestate.moveLog = copy.deepcopy(self.moveLog)
        new_gamestate.boardLog = copy.deepcopy(self.boardLog)
        new_gamestate.whiteToMove = self.whiteToMove
        new_gamestate.whiteKingLocation = self.whiteKingLocation
        new_gamestate.blackKingLocation = self.blackKingLocation
        new_gamestate.whiteQueenLocation = self.whiteQueenLocation
        new_gamestate.blackQueenLocation = self.blackQueenLocation
        new_gamestate.checkMate = self.checkMate
        new_gamestate.staleMate = self.staleMate
        new_gamestate.currentCastlingRight = copy.deepcopy(self.currentCastlingRight)
        new_gamestate.castleRightsLog = copy.deepcopy(self.castleRightsLog)
        new_gamestate.currentQueenCastlingRight = copy.deepcopy(self.currentQueenCastlingRight)
        new_gamestate.QueencastleRightsLog = copy.deepcopy(self.QueencastleRightsLog)
        new_gamestate.whiteKingInCheck = self.whiteKingInCheck
        new_gamestate.blackKingInCheck = self.blackKingInCheck
        new_gamestate.whiteKingRookColumn = self.whiteKingRookColumn
        new_gamestate.blackKingRookColumn = self.blackKingRookColumn
        new_gamestate.moveCout = self.moveCout
        new_gamestate.pieceScores = self.pieceScores.copy()
        return new_gamestate
    
    def calculateReward(self, move):
        # for move in valide_move
        #   makeMove(move)
        #   score = evaluateBoard()
        #   undoMove()
        self.makeMove(move)
        score = self.evaluateBoard()
        self.undoMove()
        return score
    
    def validMoveToStr(self):
        self.validmove_str = []
        # for move in self.get:
        #     self.validmove_str.append(str(move))
        print(len(self.validmove_str))
        print(self.validmove_str)

    def evaluateBoard(self):
        whiteScore = 0
        blackScore = 0
        for row in self.board:
            for piece in row:
                if piece != "--":
                    pieceType = piece[1]
                    if piece[0] == 'w':
                        whiteScore += self.pieceScores[pieceType]
                    else:
                        blackScore += self.pieceScores[pieceType]
        return whiteScore - blackScore
    
    def step(self, move):
        """
        Make a move in the environment.
        :param move:
        :return:
        """
        if move not in self.getValidMoves():  # Call the method to get valid moves
            raise ValueError("Invalid move")
        else:
            self.makeMove(move)

        return None
    
    def is_capture(self, move):
        start_row, start_col = move.startRow, move.startCol
        end_row, end_col = move.endRow, move.endCol
        target_piece = self.board[end_row][end_col]
        return target_piece != "--"
    
    def result(self):
        if not self.whiteToMove and self.inCheck() and len(self.getValidMoves()) == 0:
            return '1-0'
        elif self.whiteToMove and self.inCheck() and len(self.getValidMoves()) == 0:
            return '0-1'
        else:
            return '0-0'
        
    def get_reward(self):
        if self.checkMate:
            if self.whiteToMove:
                return -1  # Black wins
            else:
                return 1   # White wins
        elif self.staleMate:
            return 0  # Draw
        else:
            return 0
    def is_checkmate(self):
        if self.inCheck() and len(self.getValidMoves()) == 0:
            return True
        else:
            return False
    
    
    def printBoard(self):
        for row in self.board:
            print(" ".join(row))

    def makeMove(self, move):
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.moveLog.append(move)  # log the move
        self.whiteToMove = not self.whiteToMove  # switch players
        # Update the king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        
        if move.pieceMoved == 'wQ':
            self.whiteQueenLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bQ':
            self.blackQueenLocation = (move.endRow, move.endCol)
        
        # Pawn Promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'T'

        # Update castling rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                                 self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
        
        self.updateQueenCastleRights(move)
        self.QueencastleRightsLog.append(CastleQueenRights(self.currentQueenCastlingRight.wks, self.currentQueenCastlingRight.bks, 
                                                           self.currentQueenCastlingRight.wqs, self.currentQueenCastlingRight.bqs))
        self.moveCout += 1
        

    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back

            # Update the king's position if needed
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            # Update the queen's position if needed
            if move.pieceMoved == "wQ":
                self.whiteQueenLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bQ":
                self.blackQueenLocation = (move.startRow, move.startCol)
            # Undo castling rights
            self.castleRightsLog.pop()  # get rid of the new castle rights from the move we're undoing 
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)  # set the current castle rights to the last one in the list
            
            self.QueencastleRightsLog.pop()
            newQueenRights = self.QueencastleRightsLog[-1]
            self.currentQueenCastlingRight = CastleQueenRights(newQueenRights.wks, newQueenRights.bks, newQueenRights.wqs, newQueenRights.bqs)
            # Undo castle move
            if move.castle:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol] = self.board[move.endRow][move.endCol]
                else:
                    self.board[move.endRow][move.endCol] = self.board[move.endRow][move.endCol]

            self.checkMate = False
            self.staleMate = False
            
            self.moveCout -= 1
            

    def updateCastleRights(self, move):
        '''
        Update the castle rights given the move
        '''
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        
    def updateQueenCastleRights(self, move):
        if move.pieceMoved == 'wQ':
            self.currentQueenCastlingRight.wks = False
            self.currentQueenCastlingRight.wqs = False
        elif move.pieceMoved == 'bQ':
            self.currentQueenCastlingRight.bks = False
            self.currentQueenCastlingRight.bqs = False

    def getValidMoves(self):
        '''
        All moves considering checks. Checks when Build network
        '''
        temCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                       self.currentCastlingRight.wqs, self.currentCastlingRight.bqs) #copy the current castling right
        #############################################################
        temQueenCastleRights = CastleQueenRights(self.currentQueenCastlingRight.wks, self.currentQueenCastlingRight.bks, 
                                       self.currentQueenCastlingRight.wqs, self.currentQueenCastlingRight.bqs) #copy the current castling right
        #1) generate all possible moves
        moves = self.getAllpossibleMoves()
        #2.) for each move, make the move
        for i in range(len(moves)-1, -1, -1): #when removing from a list go backward to that list
            self.makeMove(moves[i])
            #3.) generate all opponent's moves
            #4.) for each of your opponent's moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) #5.) if they do attack your king, not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0: #either checkmates or stalemates
            if self.inCheck():
                self.checkMate = True
            else: 
                self.staleMate = True

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        ########################
        if self.whiteToMove:
            self.getQueenCastleMoves(self.whiteQueenLocation[0], self.whiteQueenLocation[1], moves)
        else: 
            self.getQueenCastleMoves(self.blackQueenLocation[0], self.blackQueenLocation[1], moves)
        #########################
        self.currentCastlingRight = temCastleRights
        ########################
        self.currentQueenCastlingRight = temQueenCastleRights
        ########################
        # self.moveCout += 1
        return moves 
    
    
    
    def getAllpossibleMoves(self):
        ''' 
        All moves without considering checks
        '''     
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # calls the appropriate move function based on piece type 
        # print(len(moves))
        return moves
    
    def is_game_over(self):
        if self.inCheck() and len(self.getValidMoves()) == 0:
            return True
        elif not self.inCheck() and len(self.getValidMoves()) == 0:
            return True
        elif self.moveCout >= 200:
            return True  
               
    def inCheck(self):
        '''
        Determine if the current player is in check
        '''
        
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        '''
        Determine if the enemy can attack the square r, c
        ''' 
        self.whiteToMove = not self.whiteToMove  # switch to opponent's turn
        oppMoves = self.getAllpossibleMoves()
        self.whiteToMove = not self.whiteToMove  # switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # square is under attack
                return True
        return False
  
    def getPawnMoves(self, r, c, moves):
        '''
        Get all the pawn moves for the pawn located at row, col and add these moves to the list
        '''
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--": # 1 square move
                moves.append(Move((r, c), (r-1, c), self.board))
                # self.possibleMoveLog.append(str(Move((r, c), (r-1, c), self.board)))
    
            #captures
            if c - 1 >= 0: #captures to the left 
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board)) 
                    # self.possibleMoveLog.append(str(Move((r, c), (r-1, c-1), self.board)))

            if c + 1 <= 7: #captures to the right 
                if self.board[r-1][c+1][0] == 'b': #enemy piece to capture 
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                    # self.possibleMoveLog.append(str(Move((r, c), (r-1, c+1), self.board)))
            

        else: #black pawn moves
            if self.board[r+1][c] == "--": # 1 square pawn advance
                moves.append(Move((r, c), (r+1, c), self.board))
       
                # self.possibleMoveLog.append(str(Move((r, c), (r+1, c), self.board)))
            
            #captures
            if c - 1 >= 0: #captures to the left 
                if self.board[r+1][c-1][0] == 'w': #enemy piece to capture 
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                    # self.possibleMoveLog.append(str(Move((r, c), (r+1, c-1), self.board)))
                    
            if c + 1 <= 7: #captures to the right 
                if self.board[r+1][c+1][0] == 'w': #enemy piece to capture 
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                    # self.possibleMoveLog.append(str(Move((r, c), (r+1, c+1), self.board)))
                    
        # add pawn promotion 
    
    def getPawnPromotionMoves(self, r, c, moves):
        self.getQueenMoves(r, c, moves) 

    def getRookMoves(self, r, c, moves):
        '''
        Get all the rook moves for the rook located at row, col and add these moves to the list
        '''
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up, left, down, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board 
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        # self.possibleMoveLog.append(str(Move((r, c), (endRow, endCol), self.board)))
                    elif endPiece[0] == enemyColor: # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        # self.possibleMoveLog.append(str(Move((r, c), (endRow, endCol), self.board)))
                        break
                    else: # friendly piece invalid
                        break
                else: # off board
                    break

    def getKnightMoves(self, r, c, moves):
        '''
        Get all the knight moves for the rook located at row, col and add these moves to the list
        '''
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8  and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                    # self.possibleMoveLog.append(str(Move((r, c), (endRow, endCol), self.board)))
    
    def getBishopMoves(self, r, c, moves):
        '''
        Get all the bishop moves for the rook located at row, col and add these moves to the list
        '''
        if self.whiteToMove:
            bishopMoves = ((-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 1))
            allyColor = "w" if self.whiteToMove else "b"
            for d in bishopMoves:
                endRow = r + d[0]
                endCol = c + d[1]
                if 0 <= endRow < 8  and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: #enemy piece valid 
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        # self.possibleMoveLog.append(str(Move((r, c), (endRow, endCol), self.board)))
        else:
            bishopMoves = ((1, -1), (1, 0), (1, 1), (-1, -1), (-1, 1))
            allyColor = "w" if self.whiteToMove else "b"
            for d in bishopMoves:
                endRow = r + d[0]
                endCol = c + d[1]
                if 0 <= endRow <= 7  and 0 <= endCol <= 7:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: #enemy piece valid 
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        # self.possibleMoveLog.append(str(Move((r, c), (endRow, endCol), self.board)))
        
    def getQueenMoves(self, r, c, moves):
        '''
        Get all the queen moves for the rook located at row, col and add these moves to the list
        '''
        queenMoves = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in queenMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8  and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                    # self.possibleMoveLog.append(str(Move((r, c), (endRow, endCol), self.board)))

    def getKingMoves(self, r, c, moves):
        '''
        Get all the king moves for the rook located at row, col and add these moves to the list
        '''
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                    # self.possibleMoveLog.append(str(Move((r, c), (endRow, endCol), self.board)))
    
    def updateCastlingRights(self, r, c):
        if self.whiteToMove:
            if self.squareUnderAttack(r, c):
                self.whiteKingInCheck = True
            for i in range(len(self.board)):
                if self.board[i][self.whiteKingLocation[1]] == 'bR':
                    self.whiteKingRookColumn = True
        else:
            if self.squareUnderAttack(r, c):
                self.blackKingInCheck = True
            for i in range(len(self.board)):
                if self.board[i][self.blackKingLocation[1]] == 'wR':
                    self.blackKingRookColumn = True
               
    def getCastleMoves(self, r, c, moves):
        self.updateCastlingRights(r, c)

        if self.whiteToMove:
            if self.currentCastlingRight.wks and not self.whiteKingInCheck and not self.whiteKingRookColumn:
                self.getKingsideCastleMoves(r, c, moves)
            if self.currentCastlingRight.wqs and not self.whiteKingInCheck and not self.whiteKingRookColumn:
                self.getQueensideCastleMoves(r, c, moves)
        else:
            if self.currentCastlingRight.bks and not self.blackKingInCheck and not self.blackKingRookColumn:
                self.getKingsideCastleMoves(r, c, moves)
            if self.currentCastlingRight.bqs and not self.blackKingInCheck and not self.blackKingRookColumn:
                self.getQueensideCastleMoves(r, c, moves)
   
    def getQueenCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return  # can't castle while in check
        if (self.whiteToMove and self.currentQueenCastlingRight.wks) or (not self.whiteToMove and self.currentQueenCastlingRight.bks):
            self.getQueenSpecialMoves(r, c, moves)

    def getQueenSpecialMoves(self, r, c, moves):
        if self.whiteToMove:
            if (self.board[r-2][c] == '--'):
                if not self.inCheck():
                    moves.append(Move((r, c), (r-2, c), self.board, castle=True))
                    # self.possibleMoveLog.append(str(Move((r, c), (r-2, c), self.board, castle=True)))
        else:
            if (self.board[r+2][c] == '--'):
                if not self.inCheck():
                    moves.append(Move((r, c), (r+2, c), self.board, castle=True))
                    # self.possibleMoveLog.append(str(Move((r, c), (r+2, c), self.board, castle=True)))
                    
    def getKingsideCastleMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c-2] == '--':
                if not self.squareUnderAttack(r-1, c-2):
                    moves.append(Move((r, c), (r-1, c-2), self.board, castle=True))
                    # self.possibleMoveLog.append(str(Move((r, c), (r-1, c-2), self.board, castle=True)))
        else:
            if self.board[r+1][c+2] == '--':
                if not self.squareUnderAttack(r+1, c+2):
                    moves.append(Move((r, c), (r+1, c+2), self.board, castle=True))
                    # self.possibleMoveLog.append(str(Move((r, c), (r+1, c+2), self.board, castle=True)))

    def getQueensideCastleMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c+2] == '--':
                if not self.squareUnderAttack(r-1, c+2):
                    moves.append(Move((r, c), (r-1, c+2), self.board, castle=True))
                    # self.possibleMoveLog.append(str(Move((r, c), (r-1, c+2), self.board, castle=True)))
        else:
            if self.board[r+1][c-2] == '--':
                if not self.squareUnderAttack(r+1, c-2):
                    moves.append(Move((r, c), (r+1, c-2), self.board, castle=True))
                    # self.possibleMoveLog.append(str(Move((r, c), (r+1, c-2), self.board, castle=True)))
       
class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
        
class CastleQueenRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
        
class Move:
    # in chess, fields on the board are described by two symbols, one of them being number between 1-8 (which is corresponding to rows)
    # and the second one being a letter between a-f (corresponding to columns), in order to use this notation we need to map our [row][col] coordinates
    # to match the ones used in the original chess game
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, castle=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.castle = castle
        # pawn promotion
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wp' and self.endRow == 2) or (self.pieceMoved == 'bp' and self.endRow == 5):
            self.isPawnPromotion = True
        # castle move
        # self.isCastleMove = isCastleMove

        self.isCapture = self.pieceCaptured != '--'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def __hash__(self):
        return hash((self.startRow, self.startCol, self.endRow, self.endCol, self.pieceMoved, self.pieceCaptured, self.castle))

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]

    def __str__(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
