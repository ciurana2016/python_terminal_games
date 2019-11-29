import os
import sys
import tty
import termios


from time import sleep
from threading import Thread, Event




event = Event()
user_input = ''
player_position = [0, 0]
alto, ancho = os.popen('stty size', 'r').read().split()
alto = int(alto)
ancho = int(ancho)

LOOP_TIME = 0.10

UI_BLACK = u'\u2588'
UI_WHITE = u' '
#UI_WHITE = u'\u2591'


def print_with_player_input():
    """
    Loop del juego
    """
    global player_position
    global user_input

    # Generamos un grid vacio
    grid = []
    for x in range(alto):
        grid.append([UI_WHITE for _ in range(ancho)])

    # Movemos al jugador en este grid dependiendo de las teclas pulsadas
    if user_input == 'd':
        if player_position[1] >= 0 and player_position[1] < (ancho-1):
            player_position[1] += 1
        else:
            sys.stdout.write('\a')
    if user_input == 'a':
        if player_position[1] <= ancho and player_position[1] > 0:
            player_position[1] -= 1
        else:
            sys.stdout.write('\a')
    if user_input == 's':
        if player_position[0] >= 0 and player_position[0] < (alto-1):
            player_position[0] += 1
        else:
            sys.stdout.write('\a')
    if user_input == 'w':
        if player_position[0] <= alto and player_position[0] > 0:
            player_position[0] -= 1
        else:
            sys.stdout.write('\a')

    grid[player_position[0]][player_position[1]] = UI_BLACK

    # Pintamos el resultado
    for row in grid:
        for place in row:
            sys.stdout.write(place)
    sys.stdout.flush()


def monitor_user_input():
    while True:
        print_with_player_input()
        if event.is_set():
            print('Event set exit')
            break
        sleep(LOOP_TIME)
    os.system('printf "\33c\e[3J"')


t = Thread(target=monitor_user_input)
t.deamon = True
t.start()

os.system('printf "\33c\e[3J"')

while True:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    # I'm a noob cause I cant get how the finally gets executed
    try:
        tty.setraw(sys.stdin.fileno())
        user_input = sys.stdin.read(1)
        sleep(LOOP_TIME)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    # When this does ... wtfs
    if ord(user_input) == 3:
        event.set()
        break

    user_input = ''
 

t.join()
