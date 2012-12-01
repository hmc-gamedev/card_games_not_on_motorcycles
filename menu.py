import curses
from spiderkey2 import SpiderKey as DoubleSuit
from spiderkey import SpiderKey as SingleSuit

class Menu():

    def __init__(self):
        self.entries = []
        self.pointer = -1
        curses.init_pair(1,curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.colormap = {'h':curses.color_pair(2),
                         'n':curses.color_pair(1)}
        self.initEntries()

    def initEntries(self):
        """ puts initial entries in list """
        self.addEntry("Spider Solitaire - Single Suit", SingleSuit())
        self.addEntry("Spider Solitaire - Double Suit", DoubleSuit())
        
    def upPointer(self):
        """ moves the pointer up an entry if possible """
        if len(self.entries) != 0 and self.pointer > 0:
            self.pointer += -1

    def downPointer(self):
        """ moves the poitner down an entry if possible """
        if len(self.entries) != 0 and self.pointer < len(self.entries)-1:
            self.pointer += 1
            
    def keypress(self, c):
        """ deals with keypresses """
        if c == 259:
            self.upPointer()
        elif c == 258:
            self.downPointer()
        elif c == ord('\n'):
            if len(self.entries) != 0:
                return self.entries[self.pointer][1]
        elif c == ord("q"):
            return "QUIT"
        return self

    def addEntry(self, d, o):
        """ adds entries to entry list """
        self.entries.append( (d,o) )
        if self.pointer < 0:
            self.pointer = 0

    def print_to_screen(self, screen):
        """ prints itself to the curses screen """
        screen.addstr(2, 2, "Play some card games not on motorcycles!")
        for i in xrange(len(self.entries)):
            if i == self.pointer:
                screen.addstr(4+i, 2, self.entries[i][0], self.colormap['h'])
            else:
                screen.addstr(4+i, 2, self.entries[i][0], self.colormap['n'])
            
        
