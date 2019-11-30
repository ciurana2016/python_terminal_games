import os
import curses



def main(c):

    # Disable cursor
    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW)
    
    h, w = c.getmaxyx()
    test_text = 'Hola mundo'

    x = w//2 - len(test_text)//2
    y = h//2

    while True:
        c.attron(curses.color_pair(1))
        c.addstr(y, x, test_text)
        c.refresh()
        c.attroff(curses.color_pair(1))

if __name__ == '__main__':
    try:
        # Prevent buggy terminal if error
        curses.wrapper(main)
    except KeyboardInterrupt:
        os.system('printf "\33c\e[3J"')
        exit()