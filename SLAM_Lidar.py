# Creating Occupancy grid using LIDAR sensor
# Its non cascading model i.e. dimensions of actual map will be almost equal to resultant
# That's actually a poor way - more size, slower computation

# TODO Stopping condition
# TODO Increase cell size of resultant map
# TODO Set botL = botW = 60 and edit move_bot() to move to centroid of unvisited cells

from numpy import array, add, subtract
from os import listdir
from PIL import Image
from PIL import ImageOps
from pygame_arena import colors
from merge_images import merge
import pygame
import pygame.locals
from math import sin, cos, radians

specs = (500, 3, 1, 1, 300, 20)
# specs[0] - Frequency of LIDAR in Hz
# specs[1] - Time taken for servo motor to complete 1 revolution
# specs[2] - Bot Length (Y Axis, using standard cartesian Coordinates)
# specs[3] - Bot Width (X Axis)
# specs[4] - Max Distance LIDAR can measure, in cm. Turn it 40k cm later
# specs[5] - Min Distance for bot to turn back from an obstacle


# --------- Global variables start------------------
actual_map = []
all_coordinates = []  # Points which are detected as obstacle or Out Of Sensor Bounds
obstacles = []  # Self Explanatory
bot = []  # bot's coordinates
direction = -1
# --------- Global variables end ------------------


# Turns 'jpg' to actual_map array
# Initializes x,y,result_map to some values
def init():
    global actual_map, bot
    im = Image.open('map.jpg')
    actual_map = array(im)

    # TODO Starting Point Issue
    # Change the starting point here. Default is the center of the map
    bot.append((actual_map.shape[1] / 2, actual_map.shape[0] / 2))
    # bot.append((2,300))


# --------------------------
#   Decides motion of the bot
# --------------------------
def move_bot():
    global actual_map, direction, bot
    (x, y) = bot[-1]

    # given code will update bot's position
    # note that i'm going in anticlockwise sense using 4 complex roots of 1 viz. 1,-1,i,-i
    delta = 1
    while delta < specs[4]:
        if 0 <= x < actual_map.shape[1] and 0 <= y < actual_map.shape[0] and 0 == actual_map[y][x]:
            x += 1 * int(direction.real)
            y += 1 * int(direction.imag)
            delta += 1
        else:
            direction *= 1j
            break

    if 0 > x:
        x = 1
    elif x >= actual_map.shape[1]:
        x = actual_map.shape[1] - 1

    if 0 > y:
        y = 1
    elif y == actual_map.shape[0]:
        y = actual_map.shape[0] - 1

    bot.append((x, y))


def get_readings():
    global bot, actual_map, all_coordinates, obstacles
    n = specs[0] * specs[1]
    (x, y) = (int(bot[-1][0]), int(bot[-1][1]))

    for i in range(1, n):
        r = 1
        (_x, _y) = (x - int(cos(radians(i * 360 / n)) * r), y - int(sin(radians(i * 360 / n)) * r))

        while 0 <= _x < actual_map.shape[1] and 0 <= _y < actual_map.shape[0] and r < specs[4]:
            if actual_map[_y][_x] != 0:
                if (_x, _y) not in obstacles:  # to avoid same point being detected again in same session
                    obstacles.append((_x, _y))
                    all_coordinates.append((_x, _y))
                break
            r += 1
            (_x, _y) = (x - int(cos(radians(i * 360 / n)) * r), y - int(sin(radians(i * 360 / n)) * r))

        # TODO Edge Issue
        # This is the situation when sensor's reading reach the max value
        (_x, _y) = (x - int(cos(radians(i * 360 / n)) * (r - 1)), y - int(sin(radians(i * 360 / n)) * (r - 1)))
        if r == specs[4] and (_x, _y) not in obstacles:
            all_coordinates.append((_x, _y))

    # TODO Center Point Issue
    # coordinates.append((x, y))


def update_image():
    global all_coordinates, bot, actual_map, obstacles

    pygame.init()
    screen = pygame.display.set_mode((2 * specs[4], 2 * specs[4]))
    screen.fill(colors['BLACK'])

    for i in range(0, len(all_coordinates)):
        # TODO Image Merge Issue
        all_coordinates[i] = add(all_coordinates[i], subtract((specs[4], specs[4]), bot[-1]))
    pygame.draw.polygon(screen, colors['LBLUE'], all_coordinates)

    for i in range(0, len(obstacles)):
        # TODO Image Merge Issue
        obstacles[i] = add(obstacles[i], subtract((specs[4], specs[4]), bot[-1]))
        # TODO Grey Area Issue
        # pygame.draw.circle(screen, colors['LGREY'], obstacles[i], specs[5])
        pygame.draw.circle(screen, colors['RED'], obstacles[i], 5)

    pygame.image.save(screen, 'temp.jpg')
    pygame.quit()

    if len(bot) > 1:
        shift = tuple(subtract(bot[-2], bot[-1]))
        result = merge('temp.jpg', 'result.jpg', shift)
        result.save('result.jpg')
    else:
        # TODO BW Issue: Convert 'L'
        Image.open('temp.jpg').save('result.jpg')

    all_coordinates = []  # this is important else u'll be using points of previous readings again
    obstacles = []


# -------------------
#   Prints result map
# -------------------
def finish():
    if 'result.jpg' in listdir('.'):
        Image.open('result.jpg').show()


def main():
    init()
    start = raw_input("Press 'y' to start: ").startswith('y')

    while start:
        print "started scanning at ", bot[-1]
        get_readings()
        update_image()
        move_bot()
        start = raw_input("Press 'y' to continue scanning: ").startswith('y')

    finish()


if __name__ == '__main__':
    main()
