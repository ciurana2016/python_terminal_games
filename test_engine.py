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


def main(c):

    # Create game
    ge = GameEngine(c)

    # TODO
    # Set colors
    # -- DONE
    ge.create_rgb_color('red', 255, 0, 0)
    ge.create_rgb_color('green', 0, 255, 0)
    ge.create_rgb_color('blue', 0, 0, 255)
    ge.create_rgb_color('skyblue', 200, 200, 255)
    ge.create_rgb_color('white', 255, 255, 255)
    # Use the colors on the paint_pixel
    # -- DONE
    # Make "structures", and background
    obstacle_object = {
        'color': 'green',
        'pixels': [
            [ge.max_x - 1, 5], [ge.max_x - 2, 5], [ge.max_x - 3, 5], [ge.max_x - 4, 5],
                    [ge.max_x - 2, 4], [ge.max_x - 3, 4],
                    [ge.max_x - 2, 3], [ge.max_x - 3, 3],
                    [ge.max_x - 2, 2], [ge.max_x - 3, 2],
                    [ge.max_x - 2, 1], [ge.max_x - 3, 1],
                    [ge.max_x - 2, 0], [ge.max_x - 3, 0],
        ]
    }
    # Different textures
    # -- DONE
    ge.create_texture({
        'name': 'sky',
        'code': u'\u2591',
        'color': 'skyblue'
    })
    # Paint background 
    # -- DONE
    # Move objects (+-x, +-y) remove part of object that gets out of screen
    #   if full object out of screen delete it, and update for colision
    # Save structures position to get colisions
    # user input
    # User is few pixels
    # User can jump
    # User can shoot

    # Intinite loop
    while True:
        # [1] Paint background
        ge.paint_background(texture='sky')
        # [2] Paint anything else
        ge.paint_pixel(0, 0, 'red')   # Bottom
        ge.paint_pixel(0, ge.max_y, 'green')  # Top
        ge.paint_pixel(ge.max_x, 0, 'blue')  # Right
        ge.paint_pixel(ge.max_x, ge.max_y, 'white') # Right Top
        # ge.paint_object(obstacle_object, texture='sky')
        ge.paint_object(obstacle_object)
        # Move object
        # for pixel in obstacle_object['pixels']:
        #     pixel[0] = pixel[0] - 1
        #ge.paint_pixel(20, 20, texture='sky')
        ge.loop()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        if not SAVE_PRINT:
            os.system('printf "\33c\e[3J"')
        exit()
