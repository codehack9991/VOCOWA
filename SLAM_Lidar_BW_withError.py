"""
Creating Occupancy grid using LIDAR sensor
Includes error defined below
"""

# TODO Stopping condition
# TODO Increase cell size of resultant map
# TODO Set botL = botW = 60 and edit move_bot() to move to centroid of unvisited cells

from numpy import array, add, subtract
from os import listdir
from PIL import Image
from pygame_arena import colors
from merge_images import merge_BW
import pygame
import pygame.locals
from random import gauss
from math import sin, cos, radians

specs = (500, 3, 1, 1, 300, 5)
"""
specs[0] - Frequency of LIDAR in Hz
specs[1] - Time taken for servo motor to complete 1 revolution
specs[2] - Bot Length (Y Axis, using standard cartesian Coordinates)
specs[3] - Bot Width (X Axis)
specs[4] - Max Distance LIDAR can measure, in cm. Turn it 40k cm later
specs[5] - Grey Area - Min Distance for bot to turn back from an obstacle
"""

errors = (0, 5)
"""
errors[0] - measurement error, per 100 cm
errors[1] - motion error, per 100 cm
"""

reality = []
all_points = []  # Points which are detected as obstacle or Out Of Sensor Bounds
OOB = []  # Out of Bound Area
real_coordinates = []  # bot's coordinates in real world
bot_center = []
direction = -1j


def init():
    """
    Turns 'jpg' to reality array
    Initializes x,y,result_map to some values
    """
    global reality, real_coordinates, bot_center
    im = Image.open('map.jpg')
    reality = array(im)

    # TODO Starting Point Issue
    real_coordinates.append((reality.shape[1] / 2, reality.shape[0] / 2))
    bot_center = (0, 0)


def move_bot():
    """
    Core of Motion Part
    Decides motion of the bot and tries to move it
    Includes Gaussian error
    """
    global reality, direction, real_coordinates, specs, direction, bot_center, errors
    (x, y) = (real_coordinates[-1][0], real_coordinates[-1][1])

    # given code will update bot's position
    # note that i'm going in anticlockwise sense using 4 complex roots of 1 viz. 1,-1,i,-i
    delta = 1
    while delta < specs[4]:
        if specs[5] <= x < reality.shape[1] - specs[5] and specs[5] <= y < reality.shape[0] - specs[5] \
                and 0 == reality[y][x]:
            x += 1 * int(direction.real)
            y += 1 * int(direction.imag)
            delta += 1
        else:
            break

    (x, y) = real_coordinates[-1]
    delta -= 1  # At this point, I'm assuming delta will always be greater than what we want
    x = int(x + delta * int(direction.real) + gauss(0, errors[1]))
    y = int(y + delta * int(direction.imag) + gauss(0, errors[1]))

    if specs[5] > x:
        x = specs[5]
        print 'Exceeding X limit'
    elif x >= reality.shape[1] - specs[5]:
        x = reality.shape[1] - specs[5] - 1
        print 'Exceeding X limit'

    if specs[5] > y:
        y = specs[5]
        print 'Exceeding Y limit'
    elif y >= reality.shape[0] - specs[5]:
        y = reality.shape[0] - specs[5] - 1
        print 'Exceeding Y limit'

    real_coordinates.append((x, y))
    bot_center = add(bot_center, subtract(real_coordinates[-1], real_coordinates[-2]))

    # Finally changing the direction
    direction *= 1j


def get_readings():
    """
    Core of measurement taking

    """
    global real_coordinates, reality, all_points, OOB
    n = specs[0] * specs[1]
    (x, y) = (int(real_coordinates[-1][0]), int(real_coordinates[-1][1]))

    for i in range(1, n):
        r = 1
        (_x, _y) = (x - int(cos(radians(i * 360 / n)) * r), y - int(sin(radians(i * 360 / n)) * r))

        while 0 <= _x < reality.shape[1] and 0 <= _y < reality.shape[0] and r < specs[4]:
            if reality[_y][_x] != 0:
                if (_x, _y) not in all_points:  # to avoid same point being detected again in same session
                    all_points.append((_x, _y))
                break
            r += 1
            (_x, _y) = (x - int(cos(radians(i * 360 / n)) * r), y - int(sin(radians(i * 360 / n)) * r))

        # TODO Out Of Bounds Issue
        # This is the situation when sensor's reading reach the max value
        (_x, _y) = (x - int(cos(radians(i * 360 / n)) * (r - 1)), y - int(sin(radians(i * 360 / n)) * (r - 1)))
        if r == specs[4]:
            OOB.append((_x, _y))
        if (_x, _y) not in all_points:
            all_points.append((_x, _y))


def update_image():
    """
    Merges the (short-lived, error-free) metric map to (global, error-prone) perspective map
    Also creates the grey-area for bot's motion

    """
    global all_points, OOB, real_coordinates, reality, bot_center

    pygame.init()
    screen = pygame.display.set_mode((2 * specs[4], 2 * specs[4]))
    screen.fill(colors['BLACK'])

    for i in range(0, len(all_points)):
        # TODO Image Merge Issue
        all_points[i] = add(all_points[i], subtract((specs[4], specs[4]), real_coordinates[-1]))
    pygame.draw.polygon(screen, colors['WHITE'], all_points)

    for i in range(0, len(OOB)):
        # TODO Image Merge Issue
        OOB[i] = add(OOB[i], subtract((specs[4], specs[4]), real_coordinates[-1]))
        # TODO Grey Area Issue
        pygame.draw.circle(screen, colors['LGREY'], OOB[i], specs[5])

    pygame.image.save(screen, 'temp.jpg')
    pygame.quit()

    if len(real_coordinates) > 1:
        bot_center = merge_BW('result.jpg', 'temp.jpg', bot_center)
    else:
        Image.open('temp.jpg').convert('L').save('result.jpg')
        bot_center = (specs[4], specs[4])

    all_points = []  # this is important else u'll be using points of previous readings again
    OOB = []


def finish():
    """ 
    :Prints Resultant map

    """
    if 'result.jpg' in listdir('.'):
        # TODO Invert Color Issue
        # ImageOps.invert(Image.open('result.jpg')).show()
        Image.open('result.jpg').show()


def main():
    init()
    start = raw_input("Press 'y' to start: ").startswith('y')

    while start:
        print "Started scanning at ", real_coordinates[-1]
        get_readings()
        update_image()
        move_bot()
        print "Ended Scanning. Bot moved ", subtract(real_coordinates[-1], real_coordinates[-2]), "\nNow at", \
            real_coordinates[-1]
        start = raw_input("\nPress 'y' to continue scanning: ").startswith('y')

    finish()


if __name__ == '__main__':
    main()
