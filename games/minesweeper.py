import random

_NOMARK = 0
_MINEMARK = 1
_QUESTIONMARK = 2

_PLAYING = "playing"
_WON = "Won"
_LOST = "lost"

class Mine:
    def __init__(self, x, y):
        self.num = -1
        self.mine= False
        self.visible = False
        self.mark = _NOMARK
        self.x = x
        self.y = y

    def __str__(self):
        if not self.visible and self.mark == _NOMARK:
            return "-"
        if not self.visible and self.mark == _MINEMARK:
            return "!"
        if not self.visible and self.mark == _QUESTIONMARK:
            return "?"
        if self.mine:
            return "*"
        if self.num > 0:
            return str(self.num)
        return " "
            
        
class Board:
    def __init__(self, width, height, mines):
        self.board = [[Mine(i,j) for i in xrange(width)] for j in xrange(height)]
        self.width = width
        self.height = height
        self.mines = mines
        self.reset()
        self.status = _PLAYING

    def reset(self):
        # reset mines
        for i in self.board:
            for j in i:
                j.num = -1
                j.mine = False
                j.visible = False
                j.mark = _NOMARK
        # set mines
        numMines = self.mines
        while numMines > 0:
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            if not self.board[y][x].mine:
                self.board[y][x].mine = True
                numMines = numMines - 1
        # set numbers
        for i in xrange(self.width):
            for j in xrange(self.height):
                neighbors = self.getNeighbors(i, j)
                mineNeighbors = [True for x in neighbors if x.mine]
                self.board[j][i].num = len(mineNeighbors)

    def getNeighbors(self, w, h):
        nL = []
        for i in xrange(w-1, w+2):
            for j in xrange(h-1, h+2):
                if not (i == w and j == h) and i >= 0 and j >= 0 and j < len(self.board) and i < len(self.board[0]):
                    nL.append(self.board[j][i])
        return nL

    def checkWon(self):
        return False
    
    def reveal(self, x, y):
        """ reveals a cell on the board, returns false if it is a mine, returns
            true otherwise, also triggers status change if necessary
        """
        if self.status == _PLAYING:
            if self.board[y][x].mine:
                self.status == _LOST
                return False
            else:
                self.board[y][x].visible = True
                if self.board[y][x].num == 0:
                    nL = self.getNeighbors(x, y)
                    for n in nL:
                        if not n.visible:
                            self.reveal(n.x, n.y)
                self.checkWon()
                return True
        return None
            
    def switchMark(self, x, y):
        self.board[y][x].mark = (self.board[y][x].mark + 1)%3
        
    def __repr__(self):
        return "hello"
