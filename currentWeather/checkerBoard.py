# CheckerBoard

class CheckerBoard:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = []
        for i in range(self.rows):
            self.board.append([])
            for j in range(self.columns):
                self.board[-1].append('*')
    def display(self):
        for i in 'abcdefgh':
            print(i, end = ' ')
        print()
        for i in range(self.rows):
            print(i, end = ' ')
            for j in range(self.columns):
                print(self.board[j][i], 
                
            
    def return_board(self):
        return self.board
c = CheckerBoard(8,8)
print(c.return_board())
                
