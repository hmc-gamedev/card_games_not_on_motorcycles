from minesweeper import Board
import curses

_UP = "up"
_DOWN = "down"
_RIGHT = "right"
_LEFT = "left"

class MineBoardKey(Board):
    def __init__(self, width, height, mines):
        Board.__init__(self, width, height, mines)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.colormap = {'n':curses.color_pair(1), 'h':curses.color_pair(2)}
        self.marker = [0,0]

    def move_marker(self, direction):
        """ move marker over board """
        if direction == _UP and self.marker[1]+1 < self.height:
            self.marker[1] += 1
        elif direction == _DOWN and self.marker[1] > 0:
            self.marker[1] += -1
        elif direction == _LEFT and self.marker[0] > 0:
            self.marker[0] += -1
        elif direction == _RIGHT and self.marker[0]+1 < self.width:
            self.marker[0] += 1
            
    def keypress(self, c):
        """ deals with keypresses """
        if c == ord('q'):
            return None
        elif c == 259:
            self.move_marker(_DOWN)
        elif c == 258:
            self.move_marker(_UP)
        elif c == 260:
            self.move_marker(_LEFT)
        elif c == 261:
            self.move_marker(_RIGHT)
        elif c == ord('d'):
            self.reveal(self.marker[0], self.marker[1])
        elif c == ord('s'):
            self.switchMark(self.marker[0], self.marker[1])
        elif c == ord('r'):
            self.reset()
            
        return self

    def print_to_screen(self, screen):
        """ prints itself to the curses screen """
        h = "arrows to move, q to return, r to reveal, e to mark"
        screen.addstr(1,2,h)
        n = 5

        for i in xrange(self.width):
            for j in xrange(self.height):
                if [i,j] == self.marker:
                    color = self.colormap["h"]
                else:
                    color = self.colormap["n"]
                screen.addstr(n+j, i+1, str(self.board[i][j]), color)
        
