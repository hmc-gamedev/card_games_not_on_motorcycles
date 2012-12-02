import random

class SpiderSingle:

    def __init__(self):
        self._deck = []
        for i in xrange(8):
            for j in xrange(1,14):
                self._deck.append( [j, 'S', False] )
        self.piles = []
        self.board = [[] for i in xrange(10)]
        self.reset()
        self.moves = 0
        self.complete_suits = 0

    def reset(self):
        self.moves = 0
        self.complete_suits = 0
        self._deck = [[i[0], i[1], False] for i in self._deck]
        random.shuffle(self._deck)
        
        self.piles = []
        self.board = [[] for i in xrange(10)]
        
        counter = 0
        pile = 0

        # set up board
        while counter < 54:
            self.board[pile].append(self._deck[counter])
            counter += 1
            pile += 1
            pile = pile % 10

        # set the tops of stacks to be visible
        for i in xrange(10):
            self.board[i][-1][2] = True
            
        # set up piles
        for x in xrange(5):
            newPile = []
            for y in xrange(10):
                newPile.append(self._deck[counter])
                counter += 1
            self.piles.append(newPile)

        # set anythign in piles to be visible for when it gets dealt
        for x in self.piles:
            for y in x:
                y[2] = True
            

    def validMove(self, destCol, col, card):
        # columns out of bounds
        if destCol < 0 or destCol > 9 or col < 0 or col > 9 or destCol == col:
            return False


        # destination can't take the specified card
        if len(self.board[destCol]) > 0:
            if self.board[destCol][-1][0] != card + 1:
                return False

        if self.board[col][-1][0] == card:
            return True
        
        for i in xrange(len(self.board[col])-2, -1, -1):
            if self.board[col][i][0] == card and self.board[col][i][2]:
                return True
            if self.board[col][i][0]-1 != self.board[col][i+1][0]:
                return False
        return False

    def move(self, dest, col, card):
        """assumes move is valid"""
        mL = []
        while self.board[col][-1][0] != card and len(self.board[col]) > 0:
            mL.append(self.board[col][-1])
            self.board[col] = self.board[col][:-1]

        mL.append(self.board[col][-1])
        self.board[col] = self.board[col][:-1]
        mL.reverse()
        self.board[dest] += mL
        self.checkComplete(dest)
        if len(self.board[col]) > 0:
            self.board[col][-1][2] = True
        self.moves += 1

    def checkComplete(self, col):
        if self.board[col][-1][0] == 1:
            for i in xrange(len(self.board[col])-2, -1, -1):
                if self.board[col][i][0]-1 != self.board[col][i+1][0]:
                    break
                if self.board[col][i][0] == 13 and i > 0:
                    self.board[col] = self.board[col][:i]
                    self.board[col][-1][2] = True
                    self.complete_suits += 1
                    break
                if self.board[col][i][0] == 13 and i == 0:
                    self.board[col] = []
                    self.complete_suits += 1
                    break
        
    def deal(self):
        if len(self.piles) > 0:
            for i in xrange(10):
                self.board[i].append(self.piles[0][i])
            self.piles = self.piles[1:]

    def won(self):
        w = [True for i in self.board if len(i) > 0]
        return not (True in w)
    
    def debug(self):
        D = {'10':'10', '11':' J', '12':' Q', '13':' K'}
        rs = ""
        rs += "There are " + str(len(self.piles)) + " piles to deal.\n"
        rs += "\n"
        for i in xrange(10):
            rs += " " + str(i) + "  "
        rs += "\n"

        # obviously cannot be more than 104 things in a single stack on board
        # actual limit is something like 6*13
        for i in xrange(104):
            rt = ""
            for j in xrange(10):
                if i < len(self.board[j]):
                    tt = str(self.board[j][i][0])
                    if len(tt) > 1:
                        rt += D[tt] + self.board[j][i][1] + " "
                    else:
                        rt += " " + tt + self.board[j][i][1] + " "
                else:
                    rt += "    "
            if 'S' in rt or '*' in rt:
                rs += rt + "\n"

        print rs
    
    def __repr__(self):
        D = {'10':'10', '11':' J', '12':' Q', '13':' K'}
        rs = ""
        rs += "There are " + str(len(self.piles)) + " piles to deal.\n"
        rs += "You have completed " + str(self.complete_suits) + " suits.\n"
        rs += "You have made " + str(self.moves) + " moves.\n"
        rs += "\n"
        for i in xrange(10):
            rs += " " + str(i) + "  "
        rs += "\n"

        # obviously cannot be more than 104 things in a single stack on board
        # actual limit is something like 6*13
        for i in xrange(104):
            rt = ""
            for j in xrange(10):
                if i < len(self.board[j]):
                    if not self.board[j][i][2]:
                        rt += " *  "
                    else:
                        tt = str(self.board[j][i][0])
                        if len(tt) > 1:
                            rt += D[tt] + self.board[j][i][1] + " "
                        else:
                            rt += " " + tt + self.board[j][i][1] + " "
                else:
                    rt += "    "
            if 'S' in rt or '*' in rt:
                rs += rt + "\n"

        return rs

def make_move(game):
    D = {'1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10,\
         'J':11, 'Q':12, 'K':13}
    col_from = int(raw_input("Move from which column? "))
    card_from = raw_input("Which card?")
    if card_from in D.keys():
        card_from = D[card_from]
    else:
        card_from = int(card_from)
    col_dest = int(raw_input("Move to which column? "))
    if game.validMove(col_dest, col_from, card_from):
        game.move(col_dest, col_from, card_from)
    else:
        print "not a valid move..."
        
def play():
    
    game = SpiderSingle()
    while not game.won():
        print game
        move = raw_input("m to move, d to deal")
        if move == "m":
            make_move(game)
        elif move == "d":
            game.deal()
    print "you won!", "it took", str(game.moves), "moves!"
        
        
