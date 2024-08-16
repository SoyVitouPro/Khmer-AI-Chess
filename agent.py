
import pygame as py
import board
from search_algo import scoreBoard
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
import torch
from model import ChessModel
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 100
LR = 0.01

BOARD_WIDTH = BOARD_HEIGHT = 790
MOVE_LOG_PANEL_WIDTH = 400
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQUARE_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 300
IMAGES = {}

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'wT', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ', 'bT']
    for piece in pieces:
        IMAGES[piece] = py.image.load("image_100x100/" + piece + ".png")


def board_to_input(gamestate):
    # Initialize an empty board with the correct number of channels
    input_board = np.zeros((8, 8, 14), dtype=np.float32)
    
    piece_map = {
        'wp': 0, 'wR': 1, 'wN': 2, 'wB': 3, 'wQ': 4, 'wK': 5, 'wT': 6,
        'bp': 7, 'bR': 8, 'bN': 9, 'bB': 10, 'bQ': 11, 'bK': 12, 'bT': 13
    }
    
    # Fill the board with piece information
    for r in range(8):
        for c in range(8):
            piece = gamestate.board[r][c]
            if piece != "--":
                input_board[r, c, piece_map[piece]] = 1
    
    # Convert the board to a PyTorch tensor and add batch dimension
    input_tensor = torch.tensor(input_board, dtype=torch.float).unsqueeze(0)  # Add batch dimension
    
    # Permute the dimensions to match the expected input for Conv2d: (batch_size, channels, height, width)
    input_tensor = input_tensor.permute(0, 3, 1, 2)  # From (batch_size, height, width, channels) to (batch_size, channels, height, width)
    
    return input_tensor

class Agent:
    def __init__(self):
        self.n_games = 0
        self.memory = []  # Experience replay memory
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = ChessModel().to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=LR)
        self.gamma = 0.99  # Discount factor
        self.epsilon = 0.1  # Exploration rate
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    def get_state(self, gs):
        state = board_to_input(gs).to(self.device)
        return state
    
    def get_white_action(self, gs):
        legal_moves = list(gs.getValidMoves())
        best_move = None
        best_value = -np.inf

        if random.random() < self.epsilon:
            # Exploration: Random move
            best_move = random.choice(legal_moves)
        else:
            # Exploitation: Best move according to the model
            with torch.no_grad():
                for move in legal_moves:
                    gs.makeMove(move)
                    input_board = self.get_state(gs)
                    value = self.model(input_board).item()
                    gs.undoMove()
                    if value > best_value:
                        best_value = value
                        best_move = move
        
        return best_move
    
    def get_black_action(self, gs):
        valid_moves = list(gs.getValidMoves())
        if not valid_moves:  # Check if there are any valid moves
            return None  # Or handle it in a way that makes sense for your application
        random_index = random.randint(0, len(valid_moves) - 1)
        best_move = valid_moves[random_index]
        return best_move

    def train_step(self):
        if len(self.memory) < BATCH_SIZE:
            return
        
        batch = random.sample(self.memory, BATCH_SIZE)
        states, next_states, rewards, dones = zip(*batch)
        
        states = torch.cat(states).to(self.device)
        next_states = torch.cat(next_states).to(self.device)
        rewards = torch.tensor(rewards, dtype=torch.float32).to(self.device)
        dones = torch.tensor(dones, dtype=torch.float32).to(self.device)

        # Current Q values
        q_values = self.model(states).squeeze()

        # Next Q values
        with torch.no_grad():
            next_q_values = self.model(next_states).squeeze()

        # TD target: reward + gamma * max(next Q) (only if not done)
        td_target = rewards + self.gamma * next_q_values * (1 - dones)

        # Loss
        loss = nn.MSELoss()(q_values, td_target)
        
        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def store_transition(self, state, next_state, reward, done):
        if len(self.memory) > MAX_MEMORY:
            self.memory.pop(0)
        self.memory.append((state, next_state, reward, done))


def train():
    agent = Agent()
    
    # Initialize game
    py.init()
    screen = py.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = py.time.Clock()
    
    screen.fill(py.Color("white"))
    gs = board.Gamestate()
    validMoves = gs.getValidMoves()
    moveLogFont = py.font.SysFont("Helvetica", 15, False, False)
    save_path = "chess_model_checkpoint.pth"
    loadImages()
    
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    step = 0

    scores = []
    mean_scores = []
    total_score = 0
    
    while running:
        for e in py.event.get():
            if e.type == py.QUIT:
                running = False

        if not gameOver:
            state = agent.get_state(gs)
            
            if gs.whiteToMove:
                move = agent.get_white_action(gs)
                gs.makeMove(move)
                reward = scoreBoard(gs)
                next_state = agent.get_state(gs)
                done = gs.checkMate or gs.staleMate
                if gs.checkMate:
                    reward = 1 if gs.whiteToMove else -1  # Win for white, lose for black
                elif gs.staleMate:
                    reward = 0  # Draw
                
                agent.store_transition(state, next_state, reward, done)
                
                total_score += reward
                scores.append(reward)
                mean_score = total_score / (step + 1)
                mean_scores.append(mean_score)
                
                plot(scores, mean_scores)  # Update the plot with scores
                
                print(step, ". white walking score:", reward)
                step += 1
                agent.train_step()
                
            else:
                move = agent.get_black_action(gs)
                gs.makeMove(move)
                print("black walking score:", scoreBoard(gs))
            
            moveMade = True
            sqSelected = ()
            playerClicks = []
            
            if gs.checkMate or gs.staleMate:
                gameOver = True
                text = 'Stalemate' if gs.staleMate else 'Black wins by checkmate' if gs.whiteToMove else 'White wins by checkmate'
                drawEndGameText(screen, text)

        if moveMade:
            drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        clock.tick(MAX_FPS)
        py.display.flip()
        
        # Reset the game if over
        if gameOver or step > 150:
            
            if agent.n_games % 10 == 0:
                # Save the model state every 10 games
                torch.save(agent.model.state_dict(), save_path)
                print(f"Model saved after {agent.n_games} games.")
            print("New Game")
            py.time.wait(1000)  # Wait for 1 second before resetting
            gs.reset()  # Use reset() method to initialize a new game
            validMoves = gs.getValidMoves()
            step = 0
            total_score = 0
            sqSelected = ()
            playerClicks = []
            moveMade = False
            gameOver = False
            agent.n_games += 1


    

def renderGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    """
    Renders the entire game state.
    
    :param screen: Pygame screen
    :param gs: GameState object
    :param validMoves: List of valid moves
    :param sqSelected: Tuple of selected square
    :param moveLogFont: Font for the move log
    """
    drawBoard(screen)
    highlightSquare(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)
    py.display.flip()

def highlightSquare(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # sqSelected is a piece that can be moved
            # Highlight selected square
            s = py.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)  # Transparency value -> 0 transparent; 255 opaque
            s.fill(py.Color('red'))
            screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))
            # Highlight moves from that square
            s.fill(py.Color('green'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQUARE_SIZE, move.endRow * SQUARE_SIZE))

def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)  # Draw squares on the board
    highlightSquare(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)  # Draw pieces on top of those squares
    drawMoveLog(screen, gs, moveLogFont)

def drawBoard(screen):
    global colors
    colors = py.Color(230, 210, 94)
    border_color = py.Color("Black")
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            py.draw.rect(screen, colors, py.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            py.draw.rect(screen, border_color, py.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

def drawPieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], py.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawMoveLog(screen, gs, font):
    moveLogRect = py.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    py.draw.rect(screen, py.Color("Black"), moveLogRect)
    moveLog = gs.moveLog
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
        textObject = font.render(text, True, py.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10  # Frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # Erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = py.Rect(move.endCol * SQUARE_SIZE, move.endRow * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        py.draw.rect(screen, color, endSquare)
        # Draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # Draw moving piece
        screen.blit(IMAGES[move.pieceMoved], py.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        py.display.flip()
        clock.tick(60)

def drawEndGameText(screen, text):
    font = py.font.SysFont("Helvetica", 40, True, False)
    textObject = font.render(text, 0, py.Color('grey'))
    textLocation = py.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2, BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, py.Color("black"))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    train()