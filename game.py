import pygame
import sys
from board import Gamestate, Move

class Game:
    def __init__(self):
        self.gs = Gamestate()
        self.validMoves = self.gs.getValidMoves()
        self.sqSelected = ()
        self.playerClicks = []

        self.BOARD_HEIGHT = 790
        self.BOARD_WIDTH = 790
        self.MOVE_LOG_PANEL_WIDTH = 400
        self.MOVE_LOG_PANEL_HEIGHT = self.BOARD_HEIGHT
        self.DIMENSION = 8
        self.MAX_FPS = 15
        self.SQUARE_SIZE = self.BOARD_HEIGHT // self.DIMENSION
        

        self.gameOver = False
        self.moveMade = False
        self.animate = False
        self.loadImages()

    def loadImages(self):
        pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'wT', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ', 'bT']
        self.IMAGES = {}
        for piece in pieces:
            self.IMAGES[piece] = pygame.image.load("image_100x100/" + piece + ".png")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.gameOver:
                    location = pygame.mouse.get_pos()
                    col = location[0] // self.SQUARE_SIZE
                    row = location[1] // self.SQUARE_SIZE
                    if self.sqSelected == (row, col) or col >= self.DIMENSION:
                        self.sqSelected = ()
                        self.playerClicks = []
                    else:
                        self.sqSelected = (row, col)
                        self.playerClicks.append(self.sqSelected)
                    if len(self.playerClicks) == 2:
                        move = Move(self.playerClicks[0], self.playerClicks[1], self.gs.board)
                        print(move.getChessNotation())
                        for i in range(len(self.validMoves)):
                            if move == self.validMoves[i]:
                                self.gs.makeMove(self.validMoves[i])
                                self.moveMade = True
                                self.animate = True
                                self.sqSelected = ()
                                self.playerClicks = []
                        if not self.moveMade:
                            self.playerClicks = [self.sqSelected]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    self.gs.undoMove()
                    self.moveMade = True
                    self.animate = False
                elif event.key == pygame.K_r:
                    self.gs = Gamestate()
                    self.validMoves = self.gs.getValidMoves()
                    self.sqSelected = ()
                    self.playerClicks = []
                    self.moveMade = False
                    self.animate = False
                    self.gameOver = False

    def update(self, screen):
        if self.moveMade:
            if self.animate:
                self.animateMove(self.gs.moveLog[-1], screen)  # Pass screen as argument
            self.validMoves = self.gs.getValidMoves()
            self.moveMade = False
            self.animate = False
        if self.gs.checkMate or self.gs.staleMate:
            self.gameOver = True

    def draw(self, screen):
        self.drawGamestate(screen)
        if self.gameOver:
            self.drawEndGameText(screen)

    def drawGamestate(self, screen):
        self.drawBoard(screen)
        self.highlightSquare(screen)
        self.drawPieces(screen)
        self.drawMoveLog(screen)

    def drawBoard(self, screen):
        colors = pygame.Color(230, 210, 94)
        border_color = pygame.Color("Black")
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                pygame.draw.rect(screen, colors, pygame.Rect(column * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
                pygame.draw.rect(screen, border_color, pygame.Rect(column * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE), 1)

    def drawPieces(self, screen):
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                piece = self.gs.board[row][column]
                if piece != "--":
                    screen.blit(self.IMAGES[piece], pygame.Rect(column * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def drawMoveLog(self, screen):
        moveLogRect = pygame.Rect(self.BOARD_WIDTH, 0, self.MOVE_LOG_PANEL_WIDTH, self.MOVE_LOG_PANEL_HEIGHT)
        pygame.draw.rect(screen, pygame.Color("Black"), moveLogRect)
        moveLog = self.gs.moveLog
        moveTexts = []
        for i in range(0, len(moveLog), 2):
            moveString = str(i // 2 + 1) + ". " + str(moveLog[i]) + " "
            if i + 1 < len(moveLog):
                moveString += str(moveLog[i + 1]) + "  "
            moveTexts.append(moveString)
        movesPerRow = 3
        padding = 6
        textY = padding
        lineSpacing = 3
        for i in range(0, len(moveTexts), movesPerRow):
            text = ""
            for j in range(movesPerRow):
                if i + j < len(moveTexts):
                    text += moveTexts[i + j]
            textObject = pygame.font.SysFont("Helvetica", 15, False, False).render(text, True, pygame.Color('white'))
            textLocation = moveLogRect.move(padding, textY)
            screen.blit(textObject, textLocation)
            textY += textObject.get_height() + lineSpacing

    def animateMove(self, move, screen):  # Added screen as a parameter
        dR = move.endRow - move.startRow
        dC = move.endCol - move.startCol
        framesPerSquare = 6
        frameCount = (abs(dR) + abs(dC)) * framesPerSquare
        for frame in range(frameCount + 1):
            r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
            self.drawBoard(screen)
            self.drawPieces(screen)
            color = [pygame.Color(230, 210, 94), pygame.Color(168, 119, 62)][(move.endRow + move.endCol) % 2]
            endSquare = pygame.Rect(move.endCol * self.SQUARE_SIZE, move.endRow * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)
            pygame.draw.rect(screen, color, endSquare)
            if move.pieceCaptured != '--':
                screen.blit(self.IMAGES[move.pieceCaptured], endSquare)
            screen.blit(self.IMAGES[move.pieceMoved], pygame.Rect(c * self.SQUARE_SIZE, r * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def highlightSquare(self, screen):
        if self.sqSelected != ():
            r, c = self.sqSelected
            if self.gs.board[r][c][0] == ('w' if self.gs.whiteToMove else 'b'):
                s = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE))
                s.set_alpha(100)
                s.fill(pygame.Color('red'))
                screen.blit(s, (c * self.SQUARE_SIZE, r * self.SQUARE_SIZE))
                s.fill(pygame.Color('green'))
                for move in self.validMoves:
                    if move.startRow == r and move.startCol == c:
                        screen.blit(s, (move.endCol * self.SQUARE_SIZE, move.endRow * self.SQUARE_SIZE))

    def drawEndGameText(self, screen):
        font = pygame.font.SysFont("Helvetica", 32, True, False)
        if self.gs.staleMate:
            text = "Stalemate"
        else:
            text = "Black wins by checkmate" if self.gs.whiteToMove else "White wins by checkmate"
        textObject = font.render(text, 0, pygame.Color('Gray'))
        textLocation = pygame.Rect(0, 0, self.BOARD_WIDTH, self.BOARD_HEIGHT).move(self.BOARD_WIDTH // 2 - textObject.get_width() // 2, self.BOARD_HEIGHT // 2 - textObject.get_height() // 2)
        screen.blit(textObject, textLocation)
        textObject = font.render(text, 0, pygame.Color('Black'))
        screen.blit(textObject, textLocation.move(2, 2))
