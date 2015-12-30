#########################################################

# slight Modifications from the project 4 Logic:

# display functions no longer print, but return strings
# Game function no longer displays anything
# GameState class requires the winner option during initialization
# Added method get_winner_option to GameState class

#########################################################

# 12658454 Jansen Yan 11/28/15

from collections import namedtuple

Flipped = namedtuple('flipcheck', ['column_index', 'row_index', 'x_dir', 'y_dir', 'index1', 'index2', 'turn'])

NONE = 0

BLACK = 1

WHITE = 2

WINNER_CHOICE = ''

# WINNER_CHOICE is an empty string because the user defines it

#### CLASSES ######

class Board(object):

    def __init__(self, columns: int, rows: int):

        ''' initializes board '''
        
        self.board = []
        self.columns = columns
        self.rows = rows
        

    def create(self):

        ''' creates board '''
        
        for i in range(self.columns):
            self.board.append([])
            for j in range(self.rows):
                self.board[-1].append(NONE)
        return self.board

    def display(self):

        '''displays board '''
        
        for i in range(self.rows):
            for j in range(self.columns):
                
                if self.board[j][i] == NONE:
                    self.board[j][i] = '.'
                    
                if self.board[j][i] == BLACK:
                    self.board[j][i] = 'B'

                if self.board[j][i] == WHITE:
                    self.board[j][i] = 'W'

                print(self.board[j][i], end = ' ')
                
            print()


    def update(self, move: [int, int], turn: int):
        
        ''' updates the board, replaces NONE with BLACK/WHITE '''

        self.move = move
        self.turn = turn        
        self.board[self.move[0]][self.move[1]] = self.turn
        
        # above line takes the list position and sets it equal to BLACK (1)
        # or WHITE (2), showing that the space is occupied
        
        return self.board
    
    def first(self, top_left_piece):

        

        ''' initially, the board should look like this,
the amount of rows and columns don't matter'''

        ''' 0 0 0 0 0 0
            0 0 B W 0 0
            0 0 W B 0 0
            0 0 0 0 0 0 '''

        column_index1 = self.columns//2
        column_index2 = self.columns//2 - 1
        row_index1 = self.rows//2
        row_index2 = self.rows// 2 - 1

        if top_left_piece == BLACK:

            self.board[column_index2][row_index2] = BLACK
            self.board[column_index1][row_index1] = BLACK
            self.board[column_index1][row_index2] = WHITE
            self.board[column_index2][row_index1] = WHITE

        if top_left_piece == WHITE:

            self.board[column_index2][row_index2] = WHITE
            self.board[column_index1][row_index1] = WHITE
            self.board[column_index1][row_index2] = BLACK
            self.board[column_index2][row_index1] = BLACK

            
        
        return self.board

    def current(self):

        return self.board


class Turn(object):

    def __init__(self, first_turn):

        self.turn = first_turn

    def update(self, turn):

        ''' every time the turn is updated, the turn is switched '''

        if turn == BLACK:
            self.turn = WHITE

        if turn == WHITE:
            self.turn = BLACK

        else:
            pass

    def current(self):

        return self.turn

    def display(self):

        if self.turn == BLACK:
            return 'B'
        elif self.turn == WHITE:
            return 'W'
        

class GameState(object):

    def __init__(self, columns: int, rows: int, first_turn: int, top_left_piece: int, winner_option: str):
        
        self.board = Board(columns, rows)
        self.turn = Turn(first_turn)
        self.top = top_left_piece
        self.winOption = winner_option

    def new_game(self):

        self.board.create()
        self.board.first(self.top)
                
    def update(self, move: [int, int], turn: int):

        self.board.update(move, turn)
        self.turn.update(turn)

    def get_board(self):

        return self.board

    def get_turn(self):

        return self.turn

    def get_winner_option(self):

        return self.winOption

    

    
class InvalidMoveError(Exception):

    pass


#############################################################################

################## VALID MOVE CHECKS ########################

def empty_check(g: GameState, column_index: int, row_index: int) -> bool:

    ''' checks if the spot is empty '''

    try:

        if g.get_board().current()[column_index][row_index] == NONE:
            return True
        else:
            return False

    except IndexError:

        return False
    
def adjacent_check(g: GameState, index1: int, index2: int) -> tuple:

    directions = [(-1, -1), (1, 1), (1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]

    b = g.get_board()

    ''' Starting from one spot, goes all in all 8 directions, and calls a function to check if in any of the eight directions,
        there is a piece with the same color, and a piece of the opposite color right before it, return True and list of Flipped Namedtuples '''
    
    seq = []
    column_index = index1
    row_index = index2

    if empty_check(g, column_index, row_index) == True:
        
        try:
            for direction in directions:

                while True:
                    
                    if direction[0] != 0:
                        if 0 <= column_index + direction[0] < b.columns:
                            column_index = column_index + direction[0]
                        else:
                            break
                        
                    if direction[1] != 0:                        
                        if 0 <= row_index + direction[1] < b.rows:
                            row_index = row_index + direction[1]
                        else:
                            break

                    if b.current()[column_index][row_index] != NONE:

                        if g.get_turn().current() == WHITE:
                            if b.current()[column_index][row_index] == WHITE:                        
                                if b.current()[column_index - direction[0]][row_index - direction[1]] == BLACK:
                                    flip = Flipped(column_index, row_index, direction[0], direction[1], index1, index2, WHITE)
                                    seq.append(flip)
                                    break
                                else:
                                    break
                                
                                    
                        if g.get_turn().current() == BLACK:
                            if b.current()[column_index][row_index] == BLACK:
                                if b.current()[column_index - direction[0]][row_index - direction[1]] == WHITE:
                                    flip = Flipped(column_index, row_index, direction[0], direction[1], index1, index2, BLACK)
                                    seq.append(flip)
                                    break
                                else:
                                    break
                        
                    else:
                        break

                column_index = index1
                row_index = index2

        except IndexError:
            print('Error')    

    if empty_check(g, column_index, row_index) == False:
        raise InvalidMoveError

    if len(seq) != 0:
        return (True, seq)
        

    if len(seq) == 0:
        return (False, )
    

def is_valid_move(g: GameState, index1: 'column index', index2: 'row index') -> bool:

    ''' calls upon empty_check and adjacent_check to make sure that a spot is valid,
    if spot is valid, prints value and flips piece'''
    
    if empty_check(g, index1, index2) == True:
        # adjacent_check returns a tuple with two values, (True, [Flipped namedtuple])
        
        if adjacent_check(g, index1, index2)[0] == True:
            return True
        else:
            return False
    else:
        return False


#Flipped = namedtuple('flipcheck', ['column_index', 'row_index', 'x_dir', 'y_dir', 'index1', 'index2', 'turn'])
        
def flip_piece(game: GameState, flip_info: '[Namedtuple Flipped]') -> None:
    
    ''' flips the appropriate pieces based on the indices of a spot with one color, and the indices of another spot
    with the same color'''

    for info in flip_info:

        starting_row_index = info.index2
        starting_column_index = info.index1
        
    
        while True:

            if info.y_dir != 0:
                if info.y_dir < 0:
                    if starting_row_index + info.y_dir > info.row_index:
                        starting_row_index = starting_row_index + info.y_dir
                    else:
                        break
                if info.y_dir > 0:
                    if starting_row_index + info.y_dir < info.row_index:
                        starting_row_index = starting_row_index + info.y_dir 
                    else:
                        break
                
            if info.x_dir != 0:
                if info.x_dir < 0:
                    if starting_column_index + info.x_dir > info.column_index:
                        starting_column_index = starting_column_index + info.x_dir            
                    else:
                        break
                if info.x_dir > 0:
                    if starting_column_index + info.x_dir < info.column_index:
                        starting_column_index = starting_column_index + info.x_dir
                    else:
                        break

      
            game.get_board().update([starting_column_index, starting_row_index], info.turn)

         ############################
######## CHECKING FOR WINNER FUNCTIONS ##########
          ###########################
            
def check_winner(g: GameState) -> bool:

    ''' there are no more valid spots when all remaining passes empty_check test
but adjacent_check fails '''

    check_list1 = []
    

    for i in range(g.get_board().columns):
        for j in range(g.get_board().rows):
            if is_valid_move(g, i, j) == True:
                check_list1.append((i, j))
                #print('Coordinates: ', (i, j))
    if len(check_list1) == 0:
        return True
    else:
        return False
    

            

def display_winner(g: GameState, user_option: str) -> None:

    ''' Displays winner based on what the user wants to define as winner ''' 

    # type(score) == class <dict>

    score = count_pieces(g)
    
    if user_option == '>':
        
        if score['BLACK'] > score['WHITE']:
            return 'WINNER: BLACK'
        elif score['WHITE'] > score['BLACK']:
            return 'WINNER: WHITE'
        else:
            return 'WINNER: NONE'
            
    elif user_option == '<':
        
        if score['BLACK'] < score['WHITE']:
            return 'WINNER: BLACK'
        elif score['WHITE'] < score['BLACK']:
            return 'WINNER: WHITE'
        else:
            return 'WINNER: NONE'

    else:
        return 'ERROR'

###################################################

#### DISPLAY FUNCTIONS ######
    
def count_pieces(g: GameState) -> int:

    ''' counts up the score by checking for the amount of BLACK
and WHITE pieces '''
    
    current_board = g.get_board().current()    
    black_count = 0
    white_count = 0
    
    for items in current_board:
        for pieces in items:
            if pieces == BLACK:
                black_count += 1
            if pieces == WHITE:
                white_count += 1
    return {'BLACK': black_count, 'WHITE': white_count}

def display_count(game: GameState) -> None:

    ''' displays the score ''' 
    
    score_dict = count_pieces(game)
    format_string = "B: {} W: {}".format(score_dict['BLACK'], score_dict['WHITE'])
    return format_string
    
def display_turn(game: GameState) -> None:

    ''' displays the turn '''

    turn = "Turn: {}".format(game.get_turn().display())
    return turn

def display_board(game: GameState) -> None:

    ''' displays a copy of the current game board ''' 

    temporary_board = copy_game_board(game.get_board().current())
    rows = game.get_board().rows
    columns = game.get_board().columns 
    
    for i in range(rows):
        for j in range(columns):
            
            if temporary_board[j][i] == NONE:
                temporary_board[j][i] = '.'
                
            if temporary_board[j][i] == BLACK:
                temporary_board[j][i] = 'B'

            if temporary_board[j][i] == WHITE:
                temporary_board[j][i] = 'W'

            print(temporary_board[j][i], end = ' ')
            
        print()


def copy_game_board(board: [[int]]) -> [[int]]:

    ''' copies the game board '''

    # works similar to create_game_board, but instead appends
    # another board's content (board[i][j]) into the boardcopy instead
    # of NONE
    boardcopy = []

    columns = len(board)
    rows = len(board[0])

    for i in range(columns):
        boardcopy.append([])
        for j in range(rows):
            boardcopy[-1].append(board[i][j])
    return boardcopy

###### GAME FUNCTION #######
def Game(index1: 'column_index', index2: 'row_index', game: GameState ) -> None:

    
    ''' flips pieces if they are valid spots'''
    if check_winner(game) == False:
        
        if is_valid_move(game, index1, index2) == True:
            
            flip_piece(game, adjacent_check(game, index1, index2)[1])
            game.update([index1, index2], game.get_turn().current())

    if check_winner(game) == True:
        game.get_turn().update(game.get_turn().current())
        # This first check_winner(game) will make sure that if (A) player makes a move that causes the (B) player to have
        # no valid move, then it will update the turn so that (A) player can make a valid move
        if check_winner(game) == True:
            return True
            # This second check_winner(game) will make sure that if both (A) and (B) players no longer have valid moves,
            # then the game will officially end


            

        
        

        
##############################
#### TEST CASES ######
'''
if __name__ == '__main__':
    
    game = GameState(4, 6, BLACK, BLACK)

    game.new_game()
    
    Game(3, 2, game)
    Game(1, 0, game)
    Game(3, 3, game)
    Game(3, 4, game)
    Game(1, 1, game)
    Game(0, 2, game)
    Game(3, 1, game)
    Game(0, 0, game)
    Game(1, 0, game)
    Game(0, 4, game)
    Game(1, 4, game)
    Game(2, 0, game)
    Game(3, 5, game)
    Game(0, 5, game)
    Game(1, 5, game)
    Game(2, 5, game)
    Game(0, 1, game)
    Game(0, 3, game)
    # After this coordinate above, no more valid moves can be made
    
##    if check_winner(game) == True:
##        print('bla')
''' 
    
    
    
    
    




    

    
