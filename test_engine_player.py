import os
import time
import curses



"""
    Try and create some clases and functions to make
    drawing things easy
"""

SAVE_PRINT = True


class GameEngine(object):

    GAME_TICK_TIME = .025
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
        # Mouse
        curses.mousemask(1)
        # Start without user action
        self.c.nodelay(1)
        # Colors
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

    def create_texture(self, texture):
        self.textures[texture['name']] = {
            'code': texture['code'],
            'color': texture['color']
        }

    def paint_pixel(self, x, y, color=False, texture=False):
        x, y = self.fix_xy(x, y)
        if not texture:
            self.use_color(color)
            self.c.addstr(y, x, self.PIXEL)
        else:
            self.use_color(
                self.textures[texture]['color']
            )
            self.c.addstr(
                y,
                x,
                self.textures[texture]['code']
            )
    
    def paint_object(self, obj, texture=False):
        color = obj['color']
        for pixel in obj['pixels']:
            self.paint_pixel(pixel[0], pixel[1], color, texture)

    def paint_background(self, color=False, texture=False):
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                self.paint_pixel(x, y, color, texture)

    def fix_xy(self, x, y):
        new_y = self.max_y - y
        return x, new_y

    def paint_player(self, player):
        for y in range(player['dimensions'][1]):
            for x in range(player['dimensions'][0]):
                self.use_color('white')
                self.c.addstr(
                    self.max_y - y,
                    x,
                    player['style'][-(y+1)][x]
                )

def main(c):

    # Create game
    ge = GameEngine(c)

    # Set colors
    ge.create_rgb_color('white', 255, 255, 255)
    ge.create_rgb_color('black', 0, 0, 0)

    # Background texture
    ge.create_texture({
        'name': 'background',
        'code': u' ',
        'color': 'black'
    })

    # Create the player object
    #  ▗ 
    # /▒▒▒\▛
    #` ░░
    #  ▏▏
    player_object = {
        'name': 'player',
        'dimensions': [6, 4],
        'style': [
            [' ', ' ', u'\u2597', ' ', ' ', ' ',],
            [' ', '/', u'\u2592', u'\u2592', '\\', u'\u259B',],
            ['', ' ', u'\u2591', u'\u2591', ' ', ' ',],
            [' ', ' ', u'\u258F', u'\u258F', ' ', ' '],
        ],
        'x': 0,
        'y': 0
    }
    
    # Intinite loop
    while True:
        # [1] Paint background
        ge.paint_background(texture='background')

        # [2] Paint anything else
        ge.paint_pixel(19, 19, 'white')

        # [Paint anything that interacts with player (for collision)]

        # [Try painting the player]
        ge.paint_player(player_object)
        
        # [LAST] Loop the game
        ge.loop()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        if not SAVE_PRINT:
            os.system('printf "\33c\e[3J"')
        exit()
