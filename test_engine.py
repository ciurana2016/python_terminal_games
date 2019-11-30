import os
import time
import curses

"""
    Try and create some clases and functions to make
    drawing things easy
"""

SAVE_PRINT = True


class GameEngine(object):

    GAME_TICK_TIME = .10
    # PIXEL => █
    PIXEL = u'\u2588'

    def __init__(self, c):
        self.c = c
        self.initial_config()

    def initial_config(self):
        # Disable cursor
        curses.curs_set(0)
        # Colors
        curses.use_default_colors()
        # Set max X and Y
        y, x = self.c.getmaxyx()
        self.max_y = y - 1
        self.max_x = x - 2

    def loop(self):
        self.c.refresh()
        time.sleep(self.GAME_TICK_TIME)

    def paint_pixel(self, x, y):
        x, y = self.fix_xy(x, y)
        curses.init_pair(33, 10, -1)
        self.c.attron(curses.color_pair(33))
        self.c.addstr(y, x, self.PIXEL)
        self.c.attroff(curses.color_pair(33))
    
    def fix_xy(self, x, y):
        new_y = self.max_y - y
        return x, new_y

def main(c):

    # Create game
    ge = GameEngine(c)

    # TODO
    # Set colors
    # Use the colors on the paint_pixel
    # Make "structures", and background
    # Move structures
    # user input

    # Intinite loop
    while True:
        ge.paint_pixel(0, 0)   # Bottom
        ge.paint_pixel(0, 29)  # Top
        ge.paint_pixel(94, 0)  # Right
        ge.paint_pixel(94, 29) # Right Top
        ge.loop()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        if not SAVE_PRINT:
            os.system('printf "\33c\e[3J"')
        exit()