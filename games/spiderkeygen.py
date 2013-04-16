from spidergen import SpiderGen
import curses


_CHOOSEPILE = "p"
_PICKMOVE = "m"
_UP = "u"
_DOWN = "d"
_RIGHT = "r"
_LEFT = "l"

class SpiderKeyGen(SpiderGen):

    def __init__(self, suit):
        SpiderGen.__init__(self, suit)
        self.mode  = _CHOOSEPILE
        self.stackpointer = 0
        self.cardpointer = 0
        self.stackpicker = 0
        curses.init_pair(1,curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3,curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4,curses.COLOR_RED, curses.COLOR_WHITE)
        curses.init_pair(5,curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(6,curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.init_pair(7,curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(8,curses.COLOR_GREEN, curses.COLOR_WHITE)
        self.colormap = {('S', 'n'):curses.color_pair(1),
                         ('S', 'h'):curses.color_pair(2),
                         ('H', 'n'):curses.color_pair(3),
                         ('H', 'h'):curses.color_pair(4),
                         ('C', 'n'):curses.color_pair(5),
                         ('C', 'h'):curses.color_pair(6),
                         ('D', 'n'):curses.color_pair(7),
                         ('D', 'h'):curses.color_pair(7)}
    
    def movestack(self, i):
        """ moves the stack picker or pointer depending on mode and feasibility """
        if i == _RIGHT and self.mode == _CHOOSEPILE and self.stackpointer < len(self.board) - 1:
            self.stackpointer += 1
            self.cardpointer = 0
        elif i == _LEFT and self.mode == _CHOOSEPILE and self.stackpointer > 0:
            self.stackpointer += -1
            self.cardpointer = 0
        elif i == _RIGHT and self.mode == _PICKMOVE and self.stackpicker < len(self.board) -1:
            self.stackpicker += 1
        elif i == _LEFT and self.mode == _PICKMOVE and self.stackpicker > 0:
            self.stackpicker += -1
                
    def movecard(self, i):
        """ moves the card pointer up if possible """
        if i == _UP and self.mode == _CHOOSEPILE and self.cardpointer < len(self.board[self.stackpointer])-1:
            card_index = len(self.board[self.stackpointer])-1-self.cardpointer
            if self.board[self.stackpointer][card_index-1][2]:
                if self.board[self.stackpointer][card_index][1] == self.board[self.stackpointer][card_index-1][1]:
                    if self.board[self.stackpointer][card_index][0] + 1 == self.board[self.stackpointer][card_index-1][0]:
                        self.cardpointer += 1
        elif i == _DOWN and self.mode == _CHOOSEPILE and self.cardpointer > 0:
            self.cardpointer += -1

    def switchmode(self):
        """ switches modes, automatically moves card piles if switching from
            pickmove and the move is valid """
        if self.mode == _CHOOSEPILE:
            self.stackpicker = self.stackpointer
            self.mode = _PICKMOVE
        elif self.mode == _PICKMOVE:
            # check for valid move and make if so
            if len(self.board[self.stackpointer]) > 0:
                cnum = self.board[self.stackpointer][len(self.board[self.stackpointer]) - self.cardpointer - 1][0]
                if self.validMove(self.stackpicker, self.stackpointer, cnum):
                    self.move(self.stackpicker, self.stackpointer, cnum)
            self.stackpointer = self.stackpicker
            self.mode = _CHOOSEPILE
            self.cardpointer = 0

    def keypress(self, c):
        """ deals with keypresses """
        if c == ord('d'):
            self.deal()
        elif c == 259:
            self.movecard(_UP)
        elif c == 258:
            self.movecard(_DOWN)
        elif c == 260:
            self.movestack(_LEFT)
        elif c == 261:
            self.movestack(_RIGHT)
        elif c == ord('\n'):
            self.switchmode()
        elif c == ord('r'):
            self.reset()
        elif c == ord('z'):
            self.undo_last()
        elif c == ord('q'):
            return None
        return self
            
    def print_to_screen(self, screen):
        """ prints itself to the curses screen """
        D = {'10':'10', '11':' J', '12':' Q', '13':' K', '1':' A'}
        h = "q - return to menu, d - deal, enter - switch from modes {select, move}, arrows - change selection, z - undo"
        screen.addstr(1,2,h)
        screen.addstr(2,2,"There are " + str(len(self.piles)) + " piles to deal.")
        screen.addstr(3,2,"You have completed " + str(self.complete_suits) + " suits.")
        screen.addstr(4,2,"You have made " + str(self.moves) + " moves.")
        screen.addstr(5,2," ")
        rs = ""
        for i in xrange(10):
            rs += " " + str(i) + "  "
        screen.addstr(6,2,rs)
        n = 7
        spacer = 4
        card_index = len(self.board[self.stackpointer])-1-self.cardpointer
        for i in xrange(104):
            rt = ""
            for j in xrange(10):
                if i < len(self.board[j]):
                    if not self.board[j][i][2]:
                        screen.addstr(n, 2+spacer*j," -  ")
                        rt += " -  "
                    else:
                        col_type = 'n'
                        if j == self.stackpointer and i >= card_index:
                            col_type = 'h'
                        color = self.colormap[self.board[j][i][1], col_type]
                        tt = str(self.board[j][i][0])
                        if tt in D.keys():
                            screen.addstr(n, 2+spacer*j, D[tt] + self.board[j][i][1] + " ", color)
                            rt += D[tt] + self.board[j][i][1] + " "
                        else:
                            screen.addstr(n, 2+spacer*j, " " + tt + self.board[j][i][1] + " ", color)
                            rt += " " + tt + self.board[j][i][1] + " "
                else:
                    rt += "    "
            n += 1
            if not ('S' in rt or '-' in rt or 'H' in rt): #we are done here
                break
        if self.mode == _PICKMOVE:
            screen.addstr(n, 2+spacer*self.stackpicker, " ^  ")
        if self.mode == _CHOOSEPILE:
            screen.addstr(n, 2+spacer*self.stackpointer, " ^  ")
        n += 1
        
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
                                                            
