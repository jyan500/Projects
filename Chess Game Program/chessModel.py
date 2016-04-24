# chessModel.py
# Jansen Yan 12658454

##from collections import namedtuple
##Moves = namedtuple('Moves', 'columnIndex, rowIndex, boundaryMoves, validMoves')

BOARD_ROWS = 8
BOARD_COLUMNS = 8

NONE = 'XX'
PAWN = 'P'
KNIGHT = 'N'
BISHOP = 'B'
ROOK = 'R'
QUEEN = 'Q'
KING = 'K'

        
DIR = [(-1, -1), (0, -1), (1, -1),

       (0, -1),           (0,  1),

       (-1, 1),  (0,  1), (1,  1)]

class White(object):
    def __init__(self):
        self._WHITE_PIECES = []       
        for i in range(8):
            self._WHITE_PIECES.append('W'+ PAWN)
        for i in range(2):
            self._WHITE_PIECES.append('W' + KNIGHT)
            self._WHITE_PIECES.append('W' + BISHOP)
            self._WHITE_PIECES.append('W' + ROOK)
        self._WHITE_PIECES.append('W' + KING)
        self._WHITE_PIECES.append('W'+ QUEEN)
        
    def pieces(self):
        return self._WHITE_PIECES
    
    def pawns(self):
        Pawns = []
        for i in range(len(self._WHITE_PIECES)):
            if self._WHITE_PIECES[i] == 'WP':
                Pawns.append(self._WHITE_PIECES[i])
        return Pawns
       
        

class Black(object):
    def __init__(self):        
        self._BLACK_PIECES = []        
        for i in range(8):            
            self._BLACK_PIECES.append('B' + PAWN)            
        for i in range(2):            
            self._BLACK_PIECES.append('B' + KNIGHT)
            self._BLACK_PIECES.append('B' + BISHOP)
            self._BLACK_PIECES.append('B' + ROOK)            
        self._BLACK_PIECES.append('B'+ KING)
        self._BLACK_PIECES.append('B' + QUEEN)
        
    def pieces(self):
        return self._BLACK_PIECES
    
    def pawns(self):
        Pawns = []
        for i in range(len(self._BLACK_PIECES)):
            if self._BLACK_PIECES[i] == 'BP':
                Pawns.append(self._BLACK_PIECES[i])
        return Pawns
    

class Board(object):
    def __init__(self):
        
        self._board = []
        self._boardcopy = []
        self._BLACK_PIECES = Black()
        self._WHITE_PIECES = White()
        
        
    def create_board(self) -> None:
        ''' creates board '''
        for i in range(BOARD_COLUMNS):
            self._board.append([])
            for j in range(BOARD_ROWS):
                self._board[-1].append(NONE)

    def initBoard(self) -> [[str]]:
    
        ''' sets up the pieces in their appropriate spots '''
    
        whiteBack = ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']
        blackBack = ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR']
 
        for i in range(BOARD_COLUMNS):
            self._board[i][BOARD_ROWS - 2] = 'WP'
            self._board[i][1] = 'BP'
        for i in range(len(whiteBack)):
            self._board[i][BOARD_ROWS - 1] = whiteBack[i]
        for i in range(len(blackBack)):
            self._board[i][0] = blackBack[i]

                
    def copyBoard(self) -> None:
        ''' copies current gameboard for display '''  
        for i in range(BOARD_COLUMNS):
            self._boardcopy.append([])
            for j in range(BOARD_ROWS):
                self._boardcopy[-1].append(self._board[i][j])

    def displayBoard(self) -> None:
        ''' display board '''
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLUMNS):
                print(self._boardcopy[j][i], end = '  ')
            print()
            
    def getBoard(self) -> 'Board object':
        ''' returns current game board '''
        return self._board

    def update(self, pieceColumn: int, pieceRow: int, moveColumn: int, moveRow: int):
        # piece_indices is the piece that the person wants to move
        # move_indices represents where the person wants to move the piece to
        self._board[moveColumn][moveRow] = self._board[pieceColumn][pieceRow]
        self._board[pieceColumn][pieceRow] = NONE
        

class Turn(object):
    def __init__(self):

        self._turn = 'WHITE'
        
    def update(self, color):
        
        if color == 'WHITE':
            self._turn = 'BLACK' 
        if color == 'BLACK':
            self._turn = 'WHITE'

    def getTurn(self):
        return self._turn
            

class GameState(object):
    
    def __init__(self):
        
        ''' initializes game'''
        
        self._board = Board()
        self._board.create_board()
        self._board.initBoard()
        self._turn = Turn()
        
    def update(self, pieceColumn: int, pieceRow: int, moveColumn: int, moveRow: int, color: str):
        
        ''' updates gameState '''
        
        self._board.update(pieceColumn, pieceRow, moveColumn, moveRow)
        self._turn.update(color)
        
    def getBoard(self):
        
        return self._board.getBoard()
    
    def getTurn(self):
        
        return self._turn.getTurn()

class InvalidMoveError(Exception):
    pass

class GameOverError(Exception):
    pass

class enPassantError(Exception):
    pass
        
### Defined solely so I wouldn't have to change each 'W' to 'B'
def giveColor(lst: (str), color: 'W or B'):
    newCopy = []
    for i in range(len(lst)):
        newCopy.append(color + lst[i])

    return newCopy
###########################
            
    
def isOnBoard(columnIndex: int, rowIndex: int) -> bool:

    ''' if column and row Index parameters are within board boundaries, return True '''
    
    if 0 <= columnIndex < BOARD_COLUMNS and 0 <= rowIndex < BOARD_ROWS:
        return True
    else:
        return False

def emptyCheck(columnIndex: int, rowIndex: int, board: [[str]]) -> bool:
    
    if board[columnIndex][rowIndex] == NONE:
        return True
    else:
        return False

def oppositeCheck(captureColumn: int, captureRow: int, game: GameState) -> bool:

    ''' checks if there is a piece of the opposite color in the square '''

    board = game.getBoard()
    turn = game.getTurn()

    if turn == 'WHITE':
        if 'B' == board[captureColumn][captureRow][0]:
            print('Yes, found a black piece to capture')
            return True
        else:
            return False
    if turn == 'BLACK':
        if 'W' == board[captureColumn][captureRow][0]:
            print('Yes, found a white piece to capture')
            return True
        else:
            return False

def isTurn(columnIndex, rowIndex, game: GameState) -> bool:

    board = game.getBoard()
    turn = game.getTurn()

    if turn == 'WHITE' and 'W' in board[columnIndex][rowIndex][0]:
        # if turn is white, and a 'W' is in the first character of the string
        # i.e WP or WK
        return True
    if turn == 'BLACK' and 'B' in board[columnIndex][rowIndex][0]:
        return True
    else:
        return False

### PAWN LOGIC ###

# a pawn can only move forwards, not backwards
# a pawn can only capture diagonally
    # in a sense, the pawn can move diagonally if...
    # there is a piece in that direction
# a pawn can perform an en passant (can be implemented later)
# a pawn can turn into a queen when getting to otherside of the board (can be implemented later)


# Implement continual checking of a direction
# if spot in front is empty:
    # its valid to move forward
# if spot in diagonal left/right direction is not empty:
    # continue
    # its valid to move
# if neither of these conditions met:
    # its not a valid move

# if pawn makes it to the other side of the board:
     # pawn becomes queen
     
def initPawnMove(columnIndex: int, rowIndex: int, moveColumn: int, moveRow: int, game: GameState) -> None:
    
    ''' On A Pawn's First move,  pawn either move one space forward or 
    two spaces forward, this function checks if its possible to do so '''
    
    board = game.getBoard()
    turn = game.getTurn()
    if turn == 'WHITE':
        if board[columnIndex][rowIndex] == 'WP':
            if 0 <= columnIndex < BOARD_COLUMNS and rowIndex == BOARD_ROWS - 2:    
                if emptyCheck(columnIndex, rowIndex - 1, board) == True and (moveColumn, moveRow) == (columnIndex, rowIndex - 1):
                    return True
                if emptyCheck(columnIndex, rowIndex - 2, board) == True and (moveColumn, moveRow) == (columnIndex, rowIndex - 2):
                    return True
                else:
                    return False       
            else:
                return False
    if turn == 'BLACK':
        if board[columnIndex][rowIndex] == 'BP':
            if 0 <= columnIndex < BOARD_COLUMNS and rowIndex == 1:
                if emptyCheck(columnIndex, rowIndex + 1, board) == True and (moveColumn, moveRow) == (columnIndex, rowIndex + 1):
                    return True
                if emptyCheck(columnIndex, rowIndex + 2, board) == True and (moveColumn, moveRow) == (columnIndex, rowIndex + 2):
                    return True
                else:
                    return False       
            else:
                return False
    else:
        return False
                
    
def pawnMove(columnIndex: int, rowIndex: int, moveColumn: int, moveRow: int, game: GameState) -> bool:
    
    ''' valid forward move for pawn '''
    # Explanation for PAWN in board[][]:
        # PAWN = 'P'
        # board[columnIndex][rowIndex] could be 'WP' or 'BP'
    board = game.getBoard()
    turn = game.getTurn()
    
    if turn == 'WHITE':
        if board[columnIndex][rowIndex] == 'WP':
            if 0 <= columnIndex < BOARD_COLUMNS and 0 <= rowIndex - 1 < BOARD_ROWS:    
                if emptyCheck(columnIndex, rowIndex - 1, board) == True and (moveColumn, moveRow) == (columnIndex, rowIndex - 1):
                    return True
                else:
                    return False
  
    if turn == 'BLACK':
        if board[columnIndex][rowIndex] == 'BP':
            if 0 <= columnIndex < BOARD_COLUMNS and 0 <= rowIndex + 1 < BOARD_ROWS:
                if emptyCheck(columnIndex, rowIndex + 1, board) == True and (moveColumn, moveRow) == (columnIndex, rowIndex + 1):
                    return True
                else:
                    return False
    else:
        return False


def pawnCapture(columnIndex: int, rowIndex: int, moveColumn: int, moveRow: int, game: GameState) -> bool:

    ''' valid forward-diagonal/backward-diagonal move for pawn '''

    whitePawnDir = [(-1, -1), (1, -1)]
    blackPawnDir = [(1, 1), (-1, 1)]

    index1 = columnIndex
    index2 = rowIndex
    
    board = game.getBoard()
    turn = game.getTurn()

    validBlackMoves = []
    validWhiteMoves = []
     
    if turn == 'WHITE':
        if board[columnIndex][rowIndex] == 'WP':
            for d in whitePawnDir:
                if 0 <= columnIndex + d[0] < BOARD_COLUMNS and 0 <= rowIndex + d[1] < BOARD_ROWS:    
                    if oppositeCheck(columnIndex + d[0], rowIndex + d[1], game) == True:
                        print('White Appended')
                        validWhiteMoves.append((columnIndex + d[0], rowIndex + d[1]))
                else:
                    continue
        if (moveColumn, moveRow) in validWhiteMoves:
            print('Yes, its true for white')
            return True
        
            
    if turn == 'BLACK':
        if board[columnIndex][rowIndex] == 'BP':
            for d in blackPawnDir:
                if 0 <= columnIndex + d[0] < BOARD_COLUMNS and 0 <= rowIndex + d[1] < BOARD_ROWS: 
                    if oppositeCheck(columnIndex + d[0], rowIndex + d[1], game) == True:
                        print('Black Appended')
                        validBlackMoves.append((columnIndex + d[0], rowIndex + d[1]))
                    else:
                        continue
        if (moveColumn, moveRow) in validBlackMoves:
            print('Yes its true for black')
            return True
                              
    else:
        return False,
    
        
def pawnPromotion(columnIndex: int, rowIndex: int, moveColumn: int, moveRow: int, game: GameState) -> None:

    ''' valid promotion for pawn '''
    
    board = game.getBoard()
    turn = game.getTurn()
   
    if turn == 'WHITE':
        if board[columnIndex][rowIndex] == 'WP':
            if moveRow == 0:
                # If the pawn is about to move into the last row, then it will
                # be turned into a queen
                board[columnIndex][rowIndex] = 'WQ'
                return True
    if turn == 'BLACK':
        if board[columnIndex][rowIndex] == 'BP':
            if moveRow == BOARD_ROWS - 1:
                # If the pawn is about to move into the last row, then it will
                # be turned into a queen
                board[columnIndex][rowIndex] = 'BQ'
                return True
                
    else:
        return None
    
##### KNIGHT LOGIC #####
            
# Knight Logic
    # if spot is empty:
        #continue
        # if spot in the L shape is empty (you'll need to find some sort of mathematical pattern):
            # its valid to move
        # if spot in the L shape is not empty:
            # its valid to move, take move

# knight moving pattern
# + or - 2 row, + or - 1 column
# + or - 1 row, + or - 2 column

def knightMove(columnIndex: int, rowIndex: int, game: GameState) -> 'bool or tuple':

    knightDir = [(-1, -2), (1, -2), (-1, 2), (1, 2), (2, -1), (2, 1), (-2, 1), (-2, -1)]

    ''' valid move for knight '''

    board = game.getBoard()
    validMoves = []
    boundaryPieces = []
    
    if KNIGHT in board[columnIndex][rowIndex]:
        print("It's a knight")
        for d in knightDir:
            print(columnIndex + d[0], rowIndex + d[1])
            if isOnBoard(columnIndex + d[0], rowIndex + d[1]) == True:
                if emptyCheck(columnIndex + d[0], rowIndex + d[1], board) == True:
                    validMoves.append((columnIndex + d[0], rowIndex + d[1]))
                else:
                    print('Boundary', columnIndex + d[0], rowIndex + d[1])
                    boundaryPieces.append((columnIndex + d[0], rowIndex + d[1]))
        return validMoves, boundaryPieces
    

                
            
#### BISHOP MOVE ####            

#Bishop Logic
    # if spot is empty:
        #continue
        # if any of the diagonals have pieces:
            # recognize those pieces
            # if one of the pieces is of the same color:
                # find piece of opposite color
                    # any spot before is a valid move, including the spot of the opposite color

def bishopMove(columnIndex: int, rowIndex: int, game: GameState) -> 'bool or tuple':

    ''' defines the boundaries of where the bishop can move given its current position '''

    diagonals = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    
    validMoves = []
    boundaryPieces = []

    index1 = columnIndex
    index2 = rowIndex
    board = game.getBoard()
    
    if BISHOP in board[columnIndex][rowIndex]:
        for d in diagonals:
            while True:
                if isOnBoard(index1 + d[0], index2 + d[1]) == True:
                    index1 += d[0]
                    index2 += d[1]
                    if emptyCheck(index1, index2, board) == True:
                        validMoves.append((index1, index2))
                    else:
                        boundaryPieces.append((index1, index2))
                        break
                else:
                    break
            index1 = columnIndex
            index2 = rowIndex
            
        return validMoves, boundaryPieces
    

#### ROOK LOGIC #####            
        
# Rook Logic
    # if spot is empty:
        # continue
        # if straight forward/backward and left/right has pieces:
            # find piece of same color:
                # find piece of opposite color
                    # any spot before is a valid move, including the spot of the opposite color
    
def rookMove(columnIndex: int, rowIndex: int, game: GameState) -> ' bool or tuple':

    ''' determines the boundaries of where the rook can move given its current position ''' 

    rookDir = [(0, -1), (0, -1), (-1, 0), (1,  0)]

    validMoves = []
    boundaryPieces = []
    
    index1 = columnIndex
    index2 = rowIndex
    board = game.getBoard()
    if ROOK in board[columnIndex][rowIndex]:
        for d in rookDir:
            while True:
                if isOnBoard(index1 + d[0], index2 + d[1]) == True:
                    index1 += d[0]
                    index2 += d[1]
                    if emptyCheck(index1, index2, board) == True:
                        validMoves.append((index1, index2))
                    else:
                        boundaryPieces.append((index1, index2))
                        break
                else:
                    break
            index1 = columnIndex
            index2 = rowIndex
            
        return validMoves, boundaryPieces
    else:
        return None
    

#### Queen Logic #####

    # if spot is empty:
        # continue
        # check in all 8 directions...
        # if there is a piece of the same color:
            # find piece of opposite color
                # any spot before is a valid move



def queenMove(columnIndex: int, rowIndex: int, game: GameState) -> None:
    
    queenDir = [(-1, -1), (0, -1), (1, -1),
                (0, -1),(0,  1), (-1, 1),
                (0,  1), (1,  1)]
    
    validMoves = []
    boundaryPieces = []
    board = game.getBoard()
    index1 = columnIndex
    index2 = rowIndex
    if QUEEN in board[columnIndex][rowIndex]:
        for d in queenDir:
            while True:
                if isOnBoard(index1 + d[0], index2 + d[1]) == True:
                    index1 += d[0]
                    index2 += d[1]
                    if emptyCheck(index1, index2, board) == True:
                        validMoves.append((index1, index2))
                    else:
                        boundaryPieces.append((index1, index2))
                        break
                else:
                    break
            index1 = columnIndex
            index2 = rowIndex
            
        return validMoves, boundaryPieces
    else:
        return None


####### King Logic ######

# King Logic
    # if spot is empty:
        # continue
        # check in all 8 adjacent directions (meaning only one space away):
        # if there is a piece of the same color:
            # not valid move
        # if there is a piece of the opposite color or empty:
            # valid move

def kingMove(columnIndex: int, rowIndex: int, game: GameState) -> bool:
    
    kingDir = [(-1, -1), (0, -1), (1, -1),
                (0, -1),(0,  1), (-1, 1),
                (0,  1), (1,  1)]
    
    validMoves = []
    boundaryPieces = []
    board = game.getBoard()

    if KING in board[columnIndex][rowIndex]:
        for d in kingDir:
            if isOnBoard(columnIndex + d[0], rowIndex + d[1]) == True:
                if emptyCheck(columnIndex + d[0], rowIndex + d[1], board) == True:
                    validMoves.append((columnIndex + d[0], rowIndex + d[1]))
                else:
                    boundaryPieces.append((columnIndex + d[0], rowIndex + d[1]))
                    break
            
        return validMoves, boundaryPieces
    else:
        return None


def isWhiteKing(columnIndex: int, rowIndex: int, board: [[str]]) -> bool:
    ''' returns true if position has white king ''' 
    if board[columnIndex][rowIndex] == 'WK':
        return True
    else:
        return False

def isBlackKing(columnIndex: int, rowIndex: int, board: [[str]]) -> bool:
    ''' returns true if position has black king ''' 
    if board[columnIndex][rowIndex] == 'BK':
        return True
    else:
        return False

def isKing(columnIndex: int, rowIndex: int, game: GameState) -> bool:
    ''' returns true if position is a king '''
    board = game.getBoard()
    turn = game.getTurn()
    if isBlackKing(columnIndex, rowIndex, game) or isWhiteKing(columnIndex, rowIndex, game) == True:
        return True
    else:
        return False
        
##### KING IN CHECK LOGIC ######
    # if king is in this [ insert this piece here ] and its appropriate direction:
        # king is in check and therefore...
        # no other piece has valid moves except..
        # the king in which...
        # the king must move out of check... (in other words)
        # the king is not in [insert this piece here and its appropriate direction check]'s range after the move
        # note that the king's valid move check still applies

def kingCheck(game: GameState) -> None:
    ''' a running check of all pieces on the board,
    makes sure that king is not in check '''
    
    board = game.getBoard()

    for i in range(len(board)):
        for j in range(len(board[i])):
            print(i, j)
            if kingInCheck(i, j, game) == True:
                print('King is not in Check')
            else:
                print('King is in check')
    

def kingInCheck(columnIndex: int, rowIndex: int, game: GameState) -> None:
    ''' if king is in certain piece's range, then it is in check '''
    checkingPieces = []
    logicDict = dict()
    pieces = [KNIGHT, BISHOP, ROOK, KING, QUEEN]
    functions = [knightMove, bishopMove, rookMove, kingMove, queenMove]
    board = game.getBoard()
    
    for p, f in zip(pieces, functions):
        logicDict[p] = f
    for key in logicDict.keys():
        if key in board[columnIndex][rowIndex]:
            movesTuple = logicDict[key](columnIndex, rowIndex, game)
            boundaryList = movesTuple[1]
            print('king check', boundaryList)
            for dirTuple in boundaryList:
                if isKing(dirTuple[0], dirTuple[1], game) == True:
                    print('one of the pieces is a king! kingInCheck functioning')
                    checkingPieces.append((board[columnIndex][rowIndex], columnIndex, rowIndex))
    if len(checkingPieces) != 0:
        return True
    else:
        return False

     
def CheckMate() -> None:

    # if kingInCheck:
        # if king has no moves to avoid being in Check
        # king is checkmated
        # return True
    # else:
        # king still has a move to get out of check
        # return False
    pass
        


#### Capturing Move ######

def whichLogic(columnIndex: int, rowIndex: int, moveColumn: int, moveRow: int, game: GameState):
    
    ''' Runs the game logic for the other pieces besides the pawn '''
    
    logicDict = dict()
    pieces = [KNIGHT, ROOK, BISHOP, KING, QUEEN]
    functions = [knightMove, rookMove, bishopMove, kingMove, queenMove]
    board = game.getBoard()
    for p, f in zip(pieces, functions):
        logicDict[p] = f
    for key in logicDict.keys():
        if key in board[columnIndex][rowIndex][1]:
            movesTuple = logicDict[key](columnIndex, rowIndex, game)
            print(board[columnIndex][rowIndex], movesTuple)
            validList = movesTuple[0]
            boundaryList = movesTuple[1]
            if isTurn(columnIndex, rowIndex, game) == True:
                if canMove(moveColumn, moveRow, validList, game) or canCapture(moveColumn, moveRow, boundaryList, game):
                    game.update(columnIndex, rowIndex, moveColumn, moveRow, game.getTurn())
                else:
                    print('Invalid Move')
            else:
                print('Not your turn')
            
       

def canMove(moveColumn: int, moveRow: int, validList: 'validMoves', game: GameState) -> bool:

    ''' Checks if the piece can be moved '''
    

    if (moveColumn, moveRow) in validList:
        return True
    else:
        return False
    
   
    
def canCapture(captureColumn: int, captureRow: int, boundarylist: 'boundaryPieces', game: GameState) -> bool:
    ''' tests to see if a piece can be captured based on a list of boundary pieces '''
    listCapture = []
    for item in boundarylist:
        # type(item) == <tuple>
        if (captureColumn, captureRow) in boundarylist:
            if oppositeCheck(item[0], item[1], game) == True:
                print('Yes, opposite check worked')
                listCapture.append((item[0], item[1]))
                print(listCapture)
                return True

##### Game Function #########

def runGame(pieceColumn: int, pieceRow: int, moveColumn: int, moveRow: int, game: GameState):
    ''' runs logic for the pieces each turn '''
    #kingCheck(pieceColumn, pieceRow, game)   
    pawnLogic(pieceColumn, pieceRow, moveColumn, moveRow, game)
    whichLogic(pieceColumn, pieceRow, moveColumn, moveRow, game)
    print(game.getTurn())



            
    

def pawnLogic(pieceColumn: int, pieceRow: int, moveColumn: int, moveRow: int, game: GameState):
    
    ''' mostly pawn logic for now... '''
    
    if initPawnMove(pieceColumn, pieceRow, moveColumn, moveRow, game) == True:
        game.update(pieceColumn, pieceRow, moveColumn, moveRow, game.getTurn())
        print(game.getTurn())
        
    elif pawnPromotion(pieceColumn, pieceRow, moveColumn, moveRow, game) == True:
        print('Yup, another pawn promoted...')
        game.update(pieceColumn, pieceRow, moveColumn, moveRow, game.getTurn())
        print(game.getTurn())
        
    elif pawnMove(pieceColumn, pieceRow, moveColumn, moveRow, game) == True:
        game.update(pieceColumn, pieceRow, moveColumn, moveRow, game.getTurn())
        print(game.getTurn())
            
    elif pawnCapture(pieceColumn, pieceRow, moveColumn, moveRow, game) == True:
        game.update(pieceColumn, pieceRow, moveColumn, moveRow, game.getTurn())
        print(game.getTurn())
    else:
        pass
        



if __name__ == '__main__':
    g = GameState()
    
            
    


        
        




            
