import os
import curses
import time


SAVE_PRINT = True


class GameEngine(object):

    GAME_TICK_TIME = .1
    PIXEL = u'\u2588'           # PIXEL => █
    COLOR_COUNT = 0             # Index for colors

    def __init__(self, c):
        self.c = c
        self.initial_config()
        self.colors = {}
        self.textures = {}

    def initial_config(self):
        # Disable cursor
        curses.curs_set(0)
        # Colors
        #curses.use_default_colors()
        curses.start_color()
        # Set max X and Y
        # Mult by 2 in Y axis because we split each 'pixel'
        # from the middle with ▄ \u2584
        y, x = self.c.getmaxyx()
        self.max_y = y -1
        self.max_x = x -2
        # Need to track all the grid every loop
        self.grid = []
        for right in range(self.max_x):
            self.grid.append([])
            for top in range(int(self.max_y * 2)):
                self.grid[right].append('')


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
        new_y = self.max_y - y

        self.use_color(color)

        has_b = (self.grid[x][y] == u'\u2584')
        has_t = (self.grid[x][y] == u'\u2580')
        has_bt = has_b and has_t

        if not (y % 2) and not has_bt:
            self.grid[x][y] = u'\u2580'
        elif y % 2 and not has_bt:
            self.grid[x][y] = u'\u2584'
        elif has_b or has_t:
            self.grid[x][y] = self.PIXEL

        # if len(self.grid[x][y]) and not has_b and not has_b:
        #     self.grid[x][y] = self.PIXEL
        # elif y % 2:
        #     self.grid[x][y] = u'\u2584'
        # else:
        #     self.grid[x][y] = u'\u2580'

        self.c.addstr(int(new_y/2), x, self.grid[x][y])
      
    


def main(c):

    # Create game
    ge = GameEngine(c)

    # Set colors
    ge.create_rgb_color('red', 255, 0, 0)
    ge.create_rgb_color('green', 0, 255, 0)
    ge.create_rgb_color('blue', 0, 0, 255)

    # Loop
    while True:
        for i in range(10):
            ge.paint_pixel(i, i, 'red')
        for i in range(10):
            ge.paint_pixel(i + 2, i, 'blue')

        ge.paint_pixel(20, 19, 'green') # not painted
        ge.paint_pixel(20, 20, 'green')
        ge.paint_pixel(20, 21, 'green')

        #ge.c.addstr(0, 0 , '%s, %s ' % (str(ge.max_y), str(ge.max_x)))
        ge.loop()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        if not SAVE_PRINT:
            os.system('printf "\33c\e[3J"')
        exit()
