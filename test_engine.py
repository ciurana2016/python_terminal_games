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
    PIXEL = u'\u2588'           # PIXEL => █
    COLOR_COUNT = 0             # Index for colors

    def __init__(self, c):
        self.c = c
        self.initial_config()
        self.colors = {}

    def initial_config(self):
        # Disable cursor
        curses.curs_set(0)
        # Colors
        #curses.use_default_colors()
        curses.start_color()
        # Set max X and Y
        y, x = self.c.getmaxyx()
        self.max_y = y - 1
        self.max_x = x - 2

    def loop(self):
        self.c.refresh()
        time.sleep(self.GAME_TICK_TIME)

    def create_rgb_color(self, name, r, g, b):
        # "Save" on our index
        self.COLOR_COUNT += 1
        self.colors[name] = self.COLOR_COUNT
        # Create the color on curses
        curses.init_color(
            self.COLOR_COUNT,
            (r * 1000) // 255,
            (g * 1000) // 255,
            (b * 1000) // 255
        )
        curses.init_pair(
            self.COLOR_COUNT,
            self.COLOR_COUNT,
            curses.COLOR_BLACK
        )

    def use_color(self, name):
        self.c.attron(
            curses.color_pair(self.colors[name])
        )

    def paint_pixel(self, x, y, color):
        x, y = self.fix_xy(x, y)
        self.use_color(color)
        self.c.addstr(y, x, self.PIXEL)
    
    def fix_xy(self, x, y):
        new_y = self.max_y - y
        return x, new_y


def main(c):

    # Create game
    ge = GameEngine(c)

    # TODO
    # Set colors
    # -- DONE
    ge.create_rgb_color('red', 255, 0, 0)
    ge.create_rgb_color('green', 0, 255, 0)
    ge.create_rgb_color('blue', 0, 0, 255)
    ge.create_rgb_color('white', 255, 255, 255)
    # Use the colors on the paint_pixel
    # -- DONE
    # Make "structures", and background
    # Move structures
    # user input

    # Intinite loop
    while True:
        ge.paint_pixel(0, 0, 'red')   # Bottom
        ge.paint_pixel(0, ge.max_y, 'green')  # Top
        ge.paint_pixel(ge.max_x, 0, 'blue')  # Right
        ge.paint_pixel(ge.max_x, ge.max_y, 'white') # Right Top
        ge.loop()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        if not SAVE_PRINT:
            os.system('printf "\33c\e[3J"')
        exit()