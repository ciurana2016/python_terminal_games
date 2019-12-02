import os
import time
import curses
import random



"""
    Try and create some clases and functions to make
    drawing things easy
"""

SAVE_PRINT = True


class GameEngine(object):

    GAME_TICK_TIME = .25
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


class MazeMaker(object):

    def __init__(self, max_x, max_y, ge):
        self.max_x = max_x
        self.max_y = max_y
        self.ge = ge
        self.stack = []
        self.visited = 0
        self.max_visited = self.max_y * self.max_x
        self.make_matrix_start()
        self.choice_count = 0

    def stack_push(self, _):
        self.stack.append(_)

    def stack_pop(self):
        del self.stack[len(self.stack) - 1]

    def make_matrix_start(self):
        """
            Matrix point
                x, y, visited, pixel content
        """
        self.matrix = []
        for y in range(self.max_y):
            for x in range(self.max_x):
                self.matrix.append([x, y, False, ''])

    def get_neighbors(self, point):
        posibles = [
            [point[0] -1, point[1]], # 0 Left
            [point[0], point[1] +1], # 1 Up
            [point[0] +1, point[1]], # 2 Right
            [point[0], point[1] -1]  # 3 Down
        ]

        # Exceptions of screen
        # Cant go more down
        if point[1] == 0:
            del posibles[3]
        # Cant go more up
        if point[1] == self.max_y:
            del posibles[1]
        # Cant go more right
        if point[0] == self.max_x:
            del posibles[2]
        # Cant go more left
        if point[0] == 0:
            del posibles[0]

        # Exceptions of already visted
        for m in self.matrix:
            if m[2] == True:
                for p in posibles:
                    if m[0] == p[0] and m[1] == p[1]:
                        posibles.remove(p)

        return posibles

    def generate_maze(self):

        # Start
        self.matrix[0][2] = True
        self.matrix[0][3] = '±'
        self.stack_push(self.matrix[0])
        self.choice_count += 1

        while self.choice_count != self.max_visited:

            # Get stack top
            point = self.stack[-1]

            # Neighbors of point
            neighbors = self.get_neighbors(point)

            # If no neighbors backtrack
            if len(neighbors) == 0:
                self.stack_pop()
                continue
    
            # Choose a random neighbor (path)
            neighbor = random.choice(neighbors)

            # Edit it on matrix, set visited, add to stack
            for m in self.matrix:
                if m[0] == neighbor[0] and m[1] == neighbor[1]:
                    m[2] = True
                    m[3] = '±'
                    self.stack_push(m)
                    self.choice_count += 1
                    neighbors.remove(neighbor)
                    self.ge.paint_pixel(m[0], m[1], 'green')
                    break

            # Choose another random nehbor (wall)
            try:
                neighbor = random.choice(neighbors)
                for m in self.matrix:
                    if m[0] == neighbor[0] and m[1] == neighbor[1]:
                        m[2] = True
                        m[3] = '#'
                        self.ge.paint_pixel(m[0], m[1], 'red')
                        # self.stack_push(m)
                        self.choice_count += 1
                        break
            except IndexError:
                pass

            self.ge.c.addstr(0, 0, str(neighbor))
            self.ge.loop()



def main(c):

    # Create game
    ge = GameEngine(c)

    # MazeMaker
    mm = MazeMaker(ge.max_x, ge.max_y, ge)

    # Set colors
    ge.create_rgb_color('red', 255, 0, 0)
    ge.create_rgb_color('green', 0, 255, 0)

    mm.generate_maze()

    # Intinite loop
    # while True:
    #     # ge.paint_pixel(0, 0, 'red')   # Bottom
    #     ge.loop()


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        if not SAVE_PRINT:
            os.system('printf "\33c\e[3J"')
        exit()
