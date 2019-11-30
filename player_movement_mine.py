import os
import time
import curses



player_x = 0
player_y = 0


def color_screen(c, color, key, player_x, player_y):
    # Gen grid
    grid = []
    height, width = c.getmaxyx()
    for h in range(height - 1):
        for w in range(width - 1):
            grid.append([w, h])

    # Position player
    try:
        key = chr(key)
    except ValueError:
        key = ''

    if key == 'd':
        if player_x < (width-2) and player_x >= 0:
            player_x += 1
    if key == 'a':
        if player_x > 0 and player_x <= (width-1):
            player_x -= 1
    if key == 's':
        if player_y >= 0 and player_y < (height-2):
            player_y += 1
    if key == 'w':
        if player_y > 0 and player_y <= (height):
            player_y -= 1

    # Print grid with player
    for point in grid:
        
        if point[0] == player_x and point[1] == player_y:
            curses.init_pair(33, 10, -1)
            player_color = curses.color_pair(33)
            c.attron(player_color)
            c.addstr(point[1], point[0], u'\u2593')
        else:
            c.attron(color)
            c.addstr(point[1], point[0], u'\u2591')
    c.refresh()
    c.attroff(player_color)
    c.attroff(color)
    
    return [player_x, player_y]

def main(c):

    height, width = c.getmaxyx()

    #Disable cursor
    curses.curs_set(0)

    # Start without user action
    c.nodelay(1)

    # Set colors
    curses.use_default_colors()
    curses.init_pair(32, 200, -1)
    purple = curses.color_pair(32)

    # PLAYER
    player_x = 0
    player_y = 0

    while True:
        key = c.getch()
        player_xy = color_screen(c, purple, key, player_x, player_y)
        player_x = player_xy[0]
        player_y = player_xy[1]
        time.sleep(.05)


if __name__ == '__main__':
    try:
        # Prevent buggy terminal if error
        curses.wrapper(main)
    except KeyboardInterrupt:
        os.system('printf "\33c\e[3J"')
        exit()
