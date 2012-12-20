import random

_suits = ["S", "H", "C", "D"]
_MOVE = "move"
_DEAL = "deal"
_CLEAR = "clear"

class SpiderGen:

    def __init__(self, suits):
        """ assumes suits is a number that is 1, 2, or 4 """
        self._deck = []
        self.undo = []
        self.suits = suits
        self.init_deck()
        
        self.piles = []
        self.board = [[] for i in xrange(10)]
        self.reset()
        self.moves = 0
        self.complete_suits = 0

    def init_deck(self):
        """ sets up the deck with 1, 2, or 4 suits """
        s = 8
        h = 0
        c = 0
        d = 0

        if self.suits == 2:
            s = 4
            h = 4
        elif self.suits == 4:
            s = 2
            h = 2
            c = 2
            d = 2

        for i in xrange(s):
            for j in xrange(1,14):
                self._deck.append( [j, 'S', False] )
        for i in xrange(h):
            for j in xrange(1,14):
                self._deck.append( [j, 'H', False] )
        for i in xrange(c):
            for j in xrange(1,14):
                self._deck.append( [j, 'C', False] )
        for i in xrange(d):
            for j in xrange(1,14):
                self._deck.append( [j, 'D', False] )
        
    def reset(self):
        """ reshuffles and sets up board """
        self.moves = 0
        self.complete_suits = 0
        self._deck = [[i[0], i[1], False] for i in self._deck]
        self.undo = []
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
        """ checks if something is a valid move, currently cannot figure out suits... """
        # columns out of bounds
        if destCol < 0 or destCol > 9 or col < 0 or col > 9 or destCol == col or len(self.board[col]) < 1:
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
            if self.board[col][i][1] != self.board[col][i+1][1]:
                return False
        return False

    def move(self, dest, col, card, undo=True):
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
        flipped = True
        if len(self.board[col]) > 0:
            flipped = self.board[col][-1][2]
            self.board[col][-1][2] = True
        self.moves += 1
        if undo:
            self.undo.append( (_MOVE, dest, col, card, flipped ) )

    def undo_last(self):
        if len(self.undo) > 0:
            self.moves += 1
            if self.undo[-1][0] == _MOVE:
                m = self.undo[-1]
                self.undo = self.undo[:-1]
                if not m[4]:
                    self.board[m[2]][-1][2] = False
                self.move(m[2], m[1], m[3], False)
                #self.undo = self.undo[:-1]
                    
            elif self.undo[-1][0] == _DEAL:
                m = self.undo[-1]
                newPiles = [ m[1] ]
                newPiles += self.piles
                self.piles = newPiles
                self.undo = self.undo[:-1]
                for i in xrange(10):
                    self.board[i] = self.board[i][:-1]
            elif self.undo[-1][0] == _CLEAR:
                m = self.undo[-1]
                newStack = self.board[m[1]]
                newStack += m[2]
                #self.board[m[1]].append(m[2])
                self.undo = self.undo[:-1]
                self.undo_last()
                
            
                
                    
        
    def checkComplete(self, col):
        """ checks if the column has a segment from 1 to 13 on top"""
        if len(self.board[col]) > 0:
            if self.board[col][-1][0] == 1:
                for i in xrange(len(self.board[col])-2, -1, -1):
                    if self.board[col][i][0]-1 != self.board[col][i+1][0]:
                        break
                    if self.board[col][i][0] == 13 and i > 0:
                        self.undo.append( (_CLEAR, col, self.board[col][i:]) )
                        self.board[col] = self.board[col][:i]
                        self.board[col][-1][2] = True
                        self.complete_suits += 1
                        break
                    if self.board[col][i][0] == 13 and i == 0:
                        self.undo.append( (_CLEAR, col, self.board[col][0:]) )
                        self.board[col] = []
                        self.complete_suits += 1
                        break
        
    def deal(self):
        """ puts cards onto the board """
        if len(self.piles) > 0:
            for i in xrange(10):
                self.board[i].append(self.piles[0][i])
            self.undo.append( (_DEAL, self.piles[0]) )
            self.piles = self.piles[1:]
            for i in xrange(10):
                self.checkComplete(i)

    def won(self):
        """ checks if there are no cards left on board """
        w = [True for i in self.board if len(i) > 0]
        return not (True in w)
    
    def debug(self):
        """ debug version of repr """
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
            check = [True for x in _suits if x in rt]
            if True in check or '*' in rt:
                rs += rt + "\n"

        return rs

def make_move(game):
    """ gets user input and tries to amke a move """
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
    """ lets you play a game of solitaire in python """
    game = SpiderGen(2)
    while not game.won():
        print game
        move = raw_input("m to move, d to deal")
        if move == "m":
            make_move(game)
        elif move == "d":
            game.deal()
    print "you won!", "it took", str(game.moves), "moves!"
        
        
