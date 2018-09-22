# Function smooth that takes a path as its input
# (with optional parameters for weight_data, weight_smooth,
# and tolerance) and returns a smooth path. The first and
# last points remain unchanged.

# Currently using gradient descent
from copy import deepcopy


def printpaths(path, newpath):
    for old, new in zip(path, newpath):
        print '[' + ', '.join('%.3f' % x for x in old) + \
              '] -> [' + ', '.join('%.3f' % x for x in new) + ']'


path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]


def smooth(path, weight_data=0.5, weight_smooth=0.1, tolerance=0.000001):
    # Make a deep copy of path into newpath
    newpath = deepcopy(path)
    delta = 1000

    while abs(delta) >= tolerance:
        for i in range(1, len(path) - 1):
            for j in range(len(path[0])):
                delta = weight_data * (path[i][j] - newpath[i][j]) + weight_smooth * (
                    newpath[i - 1][j] + newpath[i + 1][j] - 2.0 * newpath[i][j])

                newpath[i][j] += delta

    return newpath


printpaths(path, smooth(path))
