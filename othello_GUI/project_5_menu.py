import tkinter
import project_5_logic as logic
import project_5_GUI as GUI
from collections import namedtuple


class initMenu(object):
    def __init__(self):

        self.optionWin = tkinter.Toplevel()

        self.colLabel = tkinter.Label(master = self.optionWin, text = 'Please choose amount of columns')
        self.rowLabel = tkinter.Label(master = self.optionWin, text = 'Please choose amount of rows')
        self.turnLabel = tkinter.Label(master = self.optionWin, text = 'Please choose who moves first, 1 is BLACK, 2 is WHITE')
        self.pieceLabel = tkinter.Label(master = self.optionWin, text = 'Please choose color, 1 is BLACK, 2 is WHITE')
        self.winLabel = tkinter.Label(master = self.optionWin, text = 'Please choose winner option, < is less pieces wins, > is more pieces wins')
        
        
        self.specColumn = tkinter.Spinbox(master = self.optionWin, values = (4, 6, 8,
                                                                             10, 12, 14, 16), command = self.onClick1)
        self.specRow = tkinter.Spinbox(master = self.optionWin, values = (4, 6, 8,
                                                                             10, 12, 14, 16), command  = self.onClick2)

        self.specTurn = tkinter.Spinbox(master = self.optionWin, values = (logic.BLACK, logic.WHITE), command = self.onClick3)
        self.topLeft = tkinter.Spinbox(master = self.optionWin, values = (logic.BLACK, logic.WHITE), command = self.onClick4)
        self.winOption = tkinter.Spinbox(master = self.optionWin, values = ('>', '<'), command = self.onClick5)
        self.OK = tkinter.Button(master = self.optionWin, text = 'OK', command = self.onClick6)
          
        self.specColumn.grid(row = 2, column = 2)
        self.specRow.grid(row = 3, column = 2)
        self.specTurn.grid(row = 4, column = 2)
        self.topLeft.grid(row = 5, column = 2)
        self.winOption.grid(row = 6, column = 2)

        
        self.col = self.specColumn.get()
        self.row = self.specRow.get()       
        self.first = self.specTurn.get()    
        self.top = self.topLeft.get()
        self.win = self.winOption.get()

                
        self.colLabel.grid(row = 2, column = 1)
        self.rowLabel.grid(row = 3, column = 1)
        self.turnLabel.grid(row = 4, column = 1)
        self.pieceLabel.grid(row = 5, column = 1)
        self.winLabel.grid(row = 6, column = 1)
        self.OK.grid(row = 7, column = 2)

        
    def show(self):
        self.optionWin.grab_set()
        self.optionWin.wait_window()

    def onClick1(self):
        self.col = self.specColumn.get()

    def onClick2(self):
        self.row = self.specRow.get()

    def onClick3(self):
        self.first = self.specTurn.get()
          

    def onClick4(self):
        self.top = self.topLeft.get()

    def onClick5(self):
        self.win = self.winOption.get()

    def onClick6(self):
        gameInfo = namedtuple('Gameinfo', 'columns rows firstTurn topLeft winnerOption')
        self.gameInfo = gameInfo(self.col, self.row, self.first, self.top, self.win)
        self.optionWin.destroy()

    def get(self):
        return self.gameInfo
        

class Menu(object):
    def __init__(self, window: tkinter.Tk, game: logic.GameState):
        
        self.window = window
        self.game = game
        
        self.menu = tkinter.Menu(self.window)
        self.window.config(menu = self.menu)
        
        self.subMenu = tkinter.Menu(self.menu)
        self.menu.add_cascade(label = 'Options', menu = self.subMenu)
        self.subMenu.add_command(label = 'Exit', command = self.exitWindow)
        self.subMenu.add_command(label = 'New Game', command = self.newGame)
        
        self.string = logic.display_count(self.game)
        self.count = tkinter.Label(master = self.window, text = self.string)
        self.count.grid(row = 5, column = 0)

        self.string2 = ''
        self.win = tkinter.Label(master = self.window, text = self.string2)
        self.win.grid(row = 4, column = 0)

        self.string3 = logic.display_turn(self.game)
        self.turns = tkinter.Label(master = self.window, text = self.string3)
        self.turns.grid(row = 3, column = 0)

        self.rules = tkinter.Label(master = self.window, text = 'FULL')
        self.rules.grid(row = 1, column = 0)
   
    def displayScore(self, game):

        self.string = logic.display_count(self.game)    
        self.count.config(text = self.string)

    def winner(self, game):

        self.string2 = logic.display_winner(self.game, self.game.winOption)
        self.win.config(text = self.string2)

    def displayTurn(self, game):

        self.string3 = logic.display_turn(self.game)
        self.turns.config(text = self.string3)

    def destroyTurnsLabel(self):
        self.turns.destroy()

    def exitWindow(self):
        self.window.destroy()

    def newGame(self):

        self.window.destroy()
        app = GUI.OthelloBoard()
        app.start()
 
 
