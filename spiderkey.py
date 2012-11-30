from spider import SpiderSingle
import curses


_CHOOSEPILE = "p"
_PICKMOVE = "m"
_UP = "u"
_DOWN = "d"
_RIGHT = "r"
_LEFT = "l"

class SpiderKey(SpiderSingle):

    def __init__(self):
        SpiderSingle.__init__(self)
        self.mode  = _CHOOSEPILE
        self.stackpointer = 0
        self.cardpointer = 0
        self.stackpicker = 0

    def movestack(self, i):
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
        # TODO: stop it from going up farther than visible
        if i == _UP and self.mode == _CHOOSEPILE and self.cardpointer < len(self.board[self.stackpointer])-1:
            card_index = len(self.board[self.stackpointer])-1-self.cardpointer
            if self.board[self.stackpointer][card_index-1][2]:
                self.cardpointer += 1
        elif i == _DOWN and self.mode == _CHOOSEPILE and self.cardpointer > 0:
            self.cardpointer += -1

    def switchmode(self):
        if self.mode == _CHOOSEPILE:
            self.stackpicker = self.stackpointer
            self.mode = _PICKMOVE
        elif self.mode == _PICKMOVE:
            # check for valid move and make if so
            cnum = self.board[self.stackpointer][len(self.board[self.stackpointer]) - self.cardpointer - 1][0]
            if self.validMove(self.stackpicker, self.stackpointer, cnum):
                self.move(self.stackpicker, self.stackpointer, cnum)
            self.stackpointer = self.stackpicker
            self.mode = _CHOOSEPILE
            self.cardpointer = 0


    def print_to_screen(self, screen, h, n):
        D = {'10':'10', '11':' J', '12':' Q', '13':' K', '1':' A'}
        screen.addstr(2,2,"There are " + str(len(self.piles)) + " piles to deal.", n)
        screen.addstr(3,2,"You have completed " + str(self.complete_suits) + " suits.", n)
        screen.addstr(4,2,"You have made " + str(self.moves) + " moves.", n)
        screen.addstr(5,2," ", n)
        rs = ""
        for i in xrange(10):
            rs += " " + str(i) + "  "
        screen.addstr(6,2,rs, n)
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
                        tt = str(self.board[j][i][0])
                        if tt in D.keys():
                            if j == self.stackpointer and i >= card_index:
                                screen.addstr(n, 2+spacer*j, D[tt] + self.board[j][i][1] + " ", h)
                            else:
                                screen.addstr(n, 2+spacer*j, D[tt] + self.board[j][i][1] + " ")
                            rt += D[tt] + self.board[j][i][1] + " "
                        else:
                            if j == self.stackpointer and i >= card_index:
                                screen.addstr(n, 2+spacer*j, " " + tt + self.board[j][i][1] + " ", h)
                            else:
                                screen.addstr(n, 2+spacer*j, " " + tt + self.board[j][i][1] + " ")
                            rt += " " + tt + self.board[j][i][1] + " "
                else:
                    rt += "    "
            n += 1
            if not ('S' in rt or '-' in rt): #we are done here
                break
        if self.mode == _PICKMOVE:
            screen.addstr(n, 2+spacer*self.stackpicker, " ^  ")
        n += 1

        screen.addstr(n, 2, "stackpointer: " + str(s.stackpointer))
        screen.addstr(n+1, 2, "cardpointer: " + str(s.cardpointer))
        screen.addstr(n+2, 2, "stackpicker: " + str(s.stackpicker))
        screen.addstr(n+3,1," ")
        #screen.addstr(self.__repr__())
        
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
                                                            

if __name__ == '__main__':
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE)
    screen.keypad(1)
    pos = 1
    x = None
    h = curses.color_pair(1)
    n = curses.A_NORMAL
    s = SpiderKey()
    while x != ord('q'):
        screen.clear()
        screen.border(0)
        s.print_to_screen(screen, h, n)
        if x:
            screen.addstr(str(x))
        screen.refresh()
        x = screen.getch()
        if x == ord('d'):
            s.deal()
        elif x == 259:
            s.movecard(_UP)
        elif x == 258:
            s.movecard(_DOWN)
        elif x == 260:
            s.movestack(_LEFT)
        elif x == 261:
            s.movestack(_RIGHT)
        elif x == ord('\n'):
            s.switchmode()
        elif x == ord('r'):
            s.reset()
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()

