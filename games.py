import curses
from menu import Menu


if __name__ == '__main__':
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    screen.keypad(1)
    pos = 1
    x = None
    curr = Menu()
    while curr != "QUIT":
        screen.clear()
        screen.border(0)
        curr.print_to_screen(screen)
        screen.refresh()
        x = screen.getch()
        catcher = curr.keypress(x)
        if catcher:
            curr = catcher
        else:
            curr = Menu()
        
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
