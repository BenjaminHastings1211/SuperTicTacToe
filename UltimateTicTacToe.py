from tkinter import *
import time, random
W,H = 600,675
color = {1 : ['#ff1a1a','X','#b30000'], 2 : ['#1a1aff','O','#0000b3']}
FONT = ('Arial',48)

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
# state
# 0 = empty
# 1 = player 1
# 2 = player 2

class Square():
    def __init__(self,root,pos,bigLocation,size):
        self.state = 0
        self.pos = pos
        self.parentLocation = bigLocation
        self.object = Frame(root,width=size-2,height=size-2,bg='white',highlightbackground='black',highlightthickness=1)
        self.object.grid(row=pos[0],column=pos[1],rowspan=1,columnspan=1)

        self.object.bind('<Button-1>',self._onClick)

    def _onClick(self,event):
        parentTile = game.board.children[self.parentLocation[0]][self.parentLocation[1]]
        if ((self.parentLocation == game.PlaceToPlay or game.PlaceToPlay == None) and self.state == 0 and parentTile.state == 0 and game.over == False):
            self.state = (game.turn % 2) + 1
            self.object.config(bg='white')
            self.text = Label(self.object,text=color[self.state][1],bg=self.object['bg'],font=FONT,fg=color[self.state][0])
            self.text.place(anchor='c',relx=0.5,rely=0.5)
            game.nextTurn(self.parentLocation,self.pos)

        else:
            print('no can do')

    def __str__(self):
        return str(self.state)

class Board():
    def __init__(self,root,pos,size,color,master=False):
        self.pos = pos
        self.state = 0
        self.children = []

        self.container = Frame(root,width=size,height=size,bg=color)
        if master == True:
            span = 9
        else:
            span = 3
        self.container.grid(row=self.pos[0]*3,column=self.pos[1]*3,padx=2,pady=2,rowspan=span,columnspan=span)

        for r in range(3):
            row = []
            for c in range(3):
                if master == True:
                    row.append(Board(self.container,[r,c],size/3,'white'))
                else:
                    row.append(Square(self.container,[r,c],pos,size/3))
            self.children.append(row)

    def reset(self):
        self.state = 0
        for row in self.children:
            for tile in row:
                tile.state = 0
                try:
                    tile.text.place_forget()
                except AttributeError:
                    pass

    def __str__(self):
        return str(self.state)

class GameController():
    def __init__(self,root):
        self.board = Board(root,[0,0],W,'#000',True) #32CD32
        self.turn = 0
        self.PlaceToPlay = None
        self.over = False

        self.turnContainer = Frame(root,width=W,height=(H-W),bg=color[self.turn+1][0])
        self.turnContainer.grid(row=10,column=0,columnspan=9,rowspan=2)
        self.turnContainer.pack_propagate(0)

        root.bind('<space>',self.newGame)


    def nextTurn(self,playedSection,tileId):

        board = self.board.children[playedSection[0]][playedSection[1]]
        turnId = (self.turn % 2) + 1

        if board.state == 0:
            self.highlightSection(playedSection,'white')

        if self.checkWin(board.children,turnId) == True:
            board.state = turnId
            if self.checkWin(self.board.children,turnId) == True:
                self.winner(turnId)
            self.highlightSection(playedSection,color[board.state][2])
            self.PlaceToPlay = None
        else:
            if self.board.children[tileId[0]][tileId[1]].state == 0:
                self.PlaceToPlay = tileId
                self.highlightSection(tileId,'#d0d0d0')
            else:
                self.PlaceToPlay = None

        self.turn += 1
        self.turnContainer.config(bg=color[(self.turn % 2) + 1][0])

    def highlightSection(self,pos,color):
        for row in self.board.children[pos[0]][pos[1]].children:
            for tile in row:
                tile.object.config(bg=color)
                try:
                    tile.text.config(bg=color)
                except AttributeError:
                    pass

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

    def configToArray(self,config):
        return [list(config[i:i+3]) for i in range(0,len(config)-1,3)]

    def newGame(self,event):
        self.turn = 0
        self.over = False
        self.turnContainer.config(bg=color[(self.turn % 2) + 1][0])
        self.PlaceToPlay = None
        for row in self.board.children:
            for tile in row:
                self.highlightSection(tile.pos,'white')
                tile.reset()

    def winner(self,playerId):
        self.over = True
        print('congrats %s'%playerId)


root = Tk()
root.resizable(0,0)
root.geometry('%sx%s'%(W,H))
root.title("Ultimate Tic Tac Toe")

game = GameController(root)

root.mainloop()
# while 1:
#     root.update()
#     root.update_idletasks()
#     time.sleep(0.001)
