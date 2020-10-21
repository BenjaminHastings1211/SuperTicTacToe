# importing tkinter module to help create the game window
from tkinter import *

# defining constants
W,H = 600,675
color = {1 : ['#ff1a1a','X','#b30000','Red'], 2 : ['#1a1aff','O','#0000b3','Blue']}
FONT = ('Arial',48)

# all posible configurations for a win
CONFIGS = [
    '---      ',
    '   ---   ',
    '      ---',
    '-  -  -  ',
    ' -  -  - ',
    '  -  -  -',
    '-   -   -',
    '  - - -  '
]

# Square class represents each clickable tile in the tic-tac-toe boards
class Square():
    def __init__(self,root,pos,bigLocation,size):
        self.state = 0  # current state of tile
        self.pos = pos # position in parent tic-tac-toe board
        self.parentLocation = bigLocation #position of parent's tic-tac-toe board

        # creating the tile widget
        self.object = Frame(root,width=size-2,height=size-2,bg='white',highlightbackground='black',highlightthickness=1)
        self.object.grid(row=pos[0],column=pos[1],rowspan=1,columnspan=1)
        self.object.bind('<Button-1>',self._onClick)

    # _onClick handles when the tile is clicked by a player
    def _onClick(self,event):
        parentTile = game.board.children[self.parentLocation[0]][self.parentLocation[1]]
        if ((self.parentLocation == game.PlaceToPlay or game.PlaceToPlay == None) and self.state == 0 and parentTile.state == 0 and game.over == False):
            self.state = (game.turn % 2) + 1
            self.object.config(bg='white')
            self.text = Label(self.object,text=color[self.state][1],bg=self.object['bg'],font=FONT,fg=color[self.state][0])
            self.text.place(anchor='c',relx=0.5,rely=0.5)
            game.nextTurn(self.parentLocation,self.pos)

    # __str__ function makes str(Square) return the squares state as a string
    def __str__(self):
        return str(self.state)

# Board represents the tic-tac-toe boards
class Board():
    def __init__(self,root,pos,size,color,master=False):
        self.pos = pos # position of the tic-tac-toe board
        self.state = 0
        self.children = [] # a list containing all children (Square objects)

        # creating the tic-tac-toe board widget
        self.container = Frame(root,width=size,height=size,bg=color)
        if master == True:
            span = 9
        else:
            span = 3
        self.container.grid(row=self.pos[0]*3,column=self.pos[1]*3,padx=2,pady=2,rowspan=span,columnspan=span)

        # create the 3x3 grid of Square children
        for r in range(3):
            row = []
            for c in range(3):
                if master == True:
                    row.append(Board(self.container,[r,c],size/3,'white'))
                else:
                    row.append(Square(self.container,[r,c],pos,size/3))
            self.children.append(row)

    # reset will clear a tic-tac-toe tile data
    def reset(self):
        self.state = 0
        for row in self.children:
            for tile in row:
                tile.state = 0
                try:
                    tile.text.place_forget()
                except AttributeError:
                    pass

    # __str__ function makes str(Board) return the boards state as a string
    def __str__(self):
        return str(self.state)

# GameController handles all game logic and player inputs
class GameController():
    def __init__(self,root):
        self.board = Board(root,[0,0],W,'#000',True) # creates a Board object
        self.turn = 0 # number of total turns in the tic-tac-toe game
        self.PlaceToPlay = None # where next move must be (for that turn)
        self.over = False

        # defines wiget to show the winner at the end of the game
        self.winnerTag = Label(self.board.container,text='',width=W,font='Roboto 64 bold',bg='#000')

        # creates the (Blue or Red) bar at the bottom of the board to display whose turn it is
        self.turnContainer = Frame(root,width=W,height=(H-W),bg=color[self.turn+1][0])
        self.turnContainer.grid(row=10,column=0,columnspan=9,rowspan=2)
        self.turnContainer.pack_propagate(0)

        root.bind('<space>',self.newGame) # when space is pressed call GameController.newGame() function

    # nextTurn handles all logic for finishing a turn and moving forward
    def nextTurn(self,playedSection,tileId):
        board = self.board.children[playedSection[0]][playedSection[1]]
        turnId = (self.turn % 2) + 1 # who just played (playerId -> 1 or 2)

        if board.state == 0: # if the played location has a state of 0 (empty)
            self.highlightSection(playedSection,'white')
        if self.checkWin(board.children,turnId) == True: # if the local tic-tac-toe board is won
            board.state = turnId
            if self.checkWin(self.board.children,turnId) == True: # if the overall tic-tac-toe board is won
                self.winner(turnId)
            self.highlightSection(playedSection,color[board.state][2])
            self.PlaceToPlay = None
        else:
            if self.board.children[tileId[0]][tileId[1]].state == 0:
                self.PlaceToPlay = tileId
                self.highlightSection(tileId,'#d0d0d0')
            else:
                self.PlaceToPlay = None

        # change turn
        if self.over != True:
            self.turn += 1
            self.turnContainer.config(bg=color[(self.turn % 2) + 1][0])

    #highlightSection takes a given pos (y,x) and highlights that object a given color
    def highlightSection(self,pos,color):
        for row in self.board.children[pos[0]][pos[1]].children:
            for tile in row:
                tile.object.config(bg=color)
                try:
                    tile.text.config(bg=color)
                except AttributeError:
                    pass

    # checkWin determins if a wining state is present in a given set of gameData
    def checkWin(self,boardData,playerId):
        # parce board data
        parcedData = ''
        for row in boardData:
            r = ''
            for tile in row:
                if int(str(tile)) == playerId:
                    r += '-'
                else:
                    r += ' '
            parcedData += r
        #compare parcedData with CONFIGS
        for config in CONFIGS:
            same = 0
            for rows in zip(self.configToArray(config),self.configToArray(parcedData)):
                configRow, realRow = rows
                for tiles in zip(configRow,realRow):
                    if tiles.count('-') == 2:
                        same += 1
            if same == 3:
                return True
        return False

    # configToArray parces the gamedata into a readable state for GameController.checkWin() works with
    def configToArray(self,config):
        return [list(config[i:i+3]) for i in range(0,len(config)-1,3)]

    # newGame completly resets the tic-tac-toe board
    def newGame(self,event):
        self.turn = 0
        self.over = False
        self.turnContainer.config(bg=color[(self.turn % 2) + 1][0])
        self.winnerTag.place_forget()
        self.PlaceToPlay = None
        for row in self.board.children:
            for tile in row:
                self.highlightSection(tile.pos,'white')
                tile.reset()

    # winner runs when a overall winner is found
    def winner(self,playerId):
        self.over = True
        self.winnerTag.place(rely=0.5,relx=0.5,anchor='center')
        self.winnerTag.config(text="%s Won!"%color[playerId][3],fg=color[playerId][0])

# create the window
root = Tk()
root.resizable(0,0)
root.geometry('%sx%s'%(W,H))
root.title("Ultimate Tic Tac Toe")

#create the game controller
game = GameController(root)

root.mainloop()
