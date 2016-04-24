# chess view 12/14/15

import tkinter
import chessModel as chess
import position as posit
from pathlib import Path

class Application(object):
    def __init__(self, game: chess.GameState):
        self._game = game
        self._board = game.getBoard()
        self._rootWindow = tkinter.Tk()
        self._blackTiles = dict()
        self._whiteTiles = dict()
        self.initTiles()
        self._pressed = False
        self._piece_column = None
        self._piece_row = None
        self._columns = 8
        self._rows = 8
        self._canvas = tkinter.Canvas(master = self._rootWindow, width = 480,
                                      height = 480, background = 'white')
        self._canvas.grid(row = 0, column = 0,
                          sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        self._rootWindow.rowconfigure(0, weight = 1)
        self._rootWindow.columnconfigure(0, weight = 1)
        self._canvas.bind('<Configure>', self._on_canvas_resized)
        self._canvas.bind('<Button-1>', self._click)
      

    def initTiles(self):

        ''' gets the pathnames and png's for each tile '''
        
        self._pathWhite = Path('C:/Users/Jansen/Desktop/ICS 32/Chess Game Program/chesspieces/white_pieces')
        self._pathBlack = Path('C:/Users/Jansen/Desktop/ICS 32/Chess Game Program/chesspieces/black_pieces')
        if self._pathWhite.exists():
            for p in self._pathWhite.iterdir():
                self._whiteTiles['W' + p.stem] = p
                # take the first letter of str p.stem and make it uppercase
            for p in self._pathBlack.iterdir():
                self._blackTiles['B' + p.stem] = p
        else:
            print('Path does not exist')
        

        
    def start(self):
        
        self._rootWindow.mainloop()
        
    def _on_canvas_resized(self, event: tkinter.Event):
        
        ##### Every time drawBoard is called, everything is deleted and redrawn
        
        self._canvas.delete(tkinter.ALL)
        
        cwidth = self._canvas.winfo_width()
        cheight = self._canvas.winfo_height()

        ##### Draw Lines on the Board #####

        for i in range(1, self._columns):
            self._canvas.create_line(cwidth/self._columns * i, 0,  cwidth/self._columns * i, cheight)

        for j in range(1, self._rows):
            self._canvas.create_line(0, cheight/self._rows * j, cwidth, cheight/self._rows * j)

        ##### Draw Pieces on Board #####
            
        self._draw_piece()
               
    def _draw_piece(self):

        #### Draws pieces based on their positioning within self._board ([[str]]) ####

        correspond = dict()
        
        cwidth = self._canvas.winfo_width()
        cheight = self._canvas.winfo_height()
        self._canvas.image = []
        
        for keys in self._whiteTiles.keys():
            image = tkinter.PhotoImage(master = self._rootWindow, file = self._whiteTiles[keys])
            self._canvas.image.append(image)
            if keys != 'Wknight':
                correspond[image] = 'W' + self._whiteTiles[keys].stem[0].upper()
            else:
                correspond[image] = 'WN'
            
        for keys in self._blackTiles.keys():
            image = tkinter.PhotoImage(master = self._rootWindow, file = self._blackTiles[keys])
            self._canvas.image.append(image)
            if keys != 'Bknight':
                correspond[image] = 'B' + self._blackTiles[keys].stem[0].upper()
            else:
                correspond[image] = 'BN'

        for item in self._canvas.image:
            for i in range(self._rows):
                for j in range(self._columns):
                    if self._board[j][i] == correspond[item]:
                        p1 = posit.Position(i, j)
                        pointTup = p1.convert(cwidth, cheight, self._columns, self._rows)
                        self._canvas.create_image(pointTup[0], pointTup[1], anchor = tkinter.NW, image = item)
                        
    def _click(self, event: tkinter.Event):
        
        ### User holds down on the left mouse button somewhere on the canvas
        ### that click point is converted to column and row indices ###
	
        cwidth = self._canvas.winfo_width()
        cheight = self._canvas.winfo_height()
        #print('click', event.x, event.y)
        p = posit.Point(event.x, event.y)
        
        self._piece_column = p.convert(cwidth, cheight, self._columns, self._rows)[0]
        self._piece_row = p.convert(cwidth, cheight, self._columns, self._rows)[1]
        self._canvas.bind('<Button-1>', self._release)
       
      
    def _release(self, event: tkinter.Event):

        cwidth = self._canvas.winfo_width()
        cheight = self._canvas.winfo_height()
        #print('release', event.x, event.y)
        p = posit.Point(event.x, event.y)

        self._move_column = p.convert(cwidth, cheight, self._columns, self._rows)[0]
        self._move_row = p.convert(cwidth, cheight, self._columns, self._rows)[1]

        print(self._piece_column, self._piece_row, self._move_column, self._move_row)

        chess.runGame(self._piece_column, self._piece_row, self._move_column, self._move_row, self._game)
        self._draw_piece()
        
        # during the second click, python needs another event to basically "override the original one"
        # that way, the _click -> _release is in a loop of some sort
        # by putting binding both click and release at once, both event handlers get run at the button click
        self._canvas.bind('<Button-1>', self._click)

        

if __name__ ==  '__main__':
    g = chess.GameState()
    app = Application(g)
    app.start()
