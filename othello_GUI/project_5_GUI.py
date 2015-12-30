# Project_5_GUI
# 12658454 Jansen Yan
import project_5_logic as logic
import project_5_position as posit
import tkinter
import project_5_menu as Menu

# self.gameInfo = namedtuple('Gameinfo', 'columns rows firstTurn topLeft winnerOption')

class OthelloBoard(object):
    def __init__(self):

        #### Makes Top Level Object that has widgets so
        #### Users can specify the game information
        
        self.init = Menu.initMenu()
        self.init.show()
        self.gameInfo = self.init.get()

        #### Initializes the Game

        game = logic.GameState(int(self.gameInfo.columns), int(self.gameInfo.rows),
                                    int(self.gameInfo.firstTurn), int(self.gameInfo.topLeft), self.gameInfo.winnerOption)        
        self.game = game
        game.new_game()

        ##### Game Information
        
        self.board = game.get_board()
        self.rows = game.get_board().rows
        self.columns = game.get_board().columns
        self.topLeft = game.top
        

        ##### Initializes the first four ovals
        
        if self.topLeft == logic.BLACK:
            self.firstColor = 'Black'
            self.secondColor = 'White'
        if self.topLeft == logic.WHITE:
            self.firstColor = 'White'
            self.secondColor = 'Black'

        ##### Initializes the Window and Canvas, and allows it to resize
        self.window = tkinter.Tk()
        
        self.canvas = tkinter.Canvas(master = self.window, width = 500, height = 500)
        self.canvas.grid(row = 0, column = 0,
                                 sticky = tkinter.S + tkinter.E + tkinter.N + tkinter.W)

        self.menu = Menu.Menu(self.window, self.game)

        self.canvas.bind('<Configure>', self.drawBoard)
        self.canvas.bind('<Button-1>', self.handleClick)
        
        self.window.rowconfigure(0, weight = 1)
        self.window.columnconfigure(0, weight = 1)     

    def drawBoard(self, event: tkinter.Event):

        ##### Every time drawBoard is called, everything is deleted and redrawn
        
        self.canvas.delete(tkinter.ALL)
        
        cwidth = self.canvas.winfo_width()
        cheight = self.canvas.winfo_height()

        ##### Draw Lines on the Board #####

        for i in range(1, self.columns):
            self.canvas.create_line(cwidth/self.columns * i, 0,  cwidth/self.columns * i, cheight)

        for j in range(1, self.rows):
            self.canvas.create_line(0, cheight/self.rows * j, cwidth, cheight/self.rows * j)

        ##### Draw the Ovals #####

        temporary_board = logic.copy_game_board(self.game.get_board().current())

        for i in range(self.rows):
            for j in range(self.columns):
                
                if temporary_board[j][i] == logic.NONE:
                    pass
                    
                if temporary_board[j][i] == logic.BLACK:
                    p1 = posit.Position(i, j)
                    pointTup = p1.convert(cwidth, cheight, self.columns, self.rows)
                    self.canvas.create_oval(pointTup[0], pointTup[1], pointTup[2], pointTup[3], fill = 'Black')

                if temporary_board[j][i] == logic.WHITE:
                    p1 = posit.Position(i, j)
                    pointTup = p1.convert(cwidth, cheight, self.columns, self.rows)
                    self.canvas.create_oval(pointTup[0], pointTup[1], pointTup[2], pointTup[3], fill = 'White')


    def start(self) -> None:

        #### Starts the Game
        
        self.window.mainloop()

    def handleClick(self, event: tkinter.Event):

        #### Handles Click when user clicks somewhere on the Canvas

        cwidth = self.canvas.winfo_width()
        cheight = self.canvas.winfo_height()
        
        p = posit.Point(event.x, event.y)
        column_index = p.convert(cwidth, cheight, self.columns, self.rows)[0]
        row_index = p.convert(cwidth, cheight, self.columns, self.rows)[1]
        logic.Game(column_index, row_index, self.game)
        self.drawBoard(event)

        if logic.Game(column_index, row_index, self.game) == True:
            self.menu.displayScore(self.game)
            self.menu.destroyTurnsLabel()
            self.menu.winner(self.game)

        else:
            self.menu.displayScore(self.game)
            self.menu.displayTurn(self.game)
   

    
        
if __name__ == '__main__':
    app = OthelloBoard()
    app.start()
