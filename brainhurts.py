# Create the player object
#  ▗  
# /▒▒\▛
#` ░░
#  ▏▏
player_object = {
    'name': 'player',
    'dimensions': [6, 4],
    'style': [
        [' ', ' ', u'\u2597', u'\u2597', ' ', ' ',],
        [' ', '/', u'\u2592', u'\u2592', '\\', u'\u259B',],
        ['`', ' ', u'\u2591', u'\u2591', ' ', ' ',],
        [' ', ' ', u'\u258F', u'\u258F', ' ', ' '],
    ],
    'x': 20,
    'y': 20
}

# def paint_player(player):
#     for y in range(player['dimensions'][1])[::-1]:
#         for x in range(player['dimensions'][0]):
#             print(player['style'][y][x])
            

print(player_object['style'][-0])