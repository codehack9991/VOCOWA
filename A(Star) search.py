delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right


# delta_name = ['^', '<', 'v', '>']


def search(grid, init, goal, cost, heuristic):
    closed = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]
    expand = [[-1 for col in range(len(grid[0]))] for row in range(len(grid))]

    closed[init[0]][init[1]] = 1
    x = init[0]
    y = init[1]
    g = 0
    f = g + heuristic[x][y]

    open = [[f, g, x, y]]

    found = False  # flag that is set when search is complete
    count = 0

    while not found:
        if len(open) == 0:
            return "Fail"
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[2]
            y = next[3]
            g = next[1]
            expand[x][y] = count
            count += 1

            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    [x2, y2] = [x + delta[i][0], y + delta[i][1]]
                    if len(grid) > x2 >= 0 and len(grid[0]) > y2 >= 0:
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + cost
                            f2 = g2 + heuristic[x2][y2]
                            open.append([f2, g2, x2, y2])
                            closed[x2][y2] = 1

    return expand


def main():
    grid = [[0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0]]
    heuristic = [[9, 8, 7, 6, 5, 4],
                 [8, 7, 6, 5, 4, 3],
                 [7, 6, 5, 4, 3, 2],
                 [6, 5, 4, 3, 2, 1],
                 [5, 4, 3, 2, 1, 0]]

    # initial and goal positions
    init = [0, 0]
    goal = [len(grid) - 1, len(grid[0]) - 1]
    cost = 1  # to move a step

    for i in search(grid, init, goal, cost, heuristic):
        print i


if __name__ == '__main__':
    main()
