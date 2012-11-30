import curses
from spiderkey2 import SpiderKey as DoubleSuit
from spiderkey import SpiderKey as SingleSuit

if __name__ == '__main__':
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    screen.keypad(1)
    pos = 1
    x = None
    h = curses.color_pair(1)
    S = curses.color_pair(2)
    s = DoubleSuit()
    while x != ord('q'):
        screen.clear()
        screen.border(0)
        s.print_to_screen(screen)
        #if x:
        #    screen.addstr(str(x))
        screen.refresh()
        x = screen.getch()
        s.keypress(x)
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
