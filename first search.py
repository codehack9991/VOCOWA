grid = [[0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0]]
init = [0, 0]
goal = [len(grid) - 1, len(grid[0]) - 1]
cost = 1

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']


def search(grid, init, goal, cost):
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    expand = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
    result = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1

    x = init[0]
    y = init[1]
    g = 0
    count = 0
    open = [[g, x, y]]

    found = False  # flag that is set when search is complete
    resign = False  # flag set if we can't find expand

    while not found and not resign:
        if len(open) == 0:
            resign = True
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[1]
            y = next[2]
            g = next[0]
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
                            open.append([g2, x2, y2])
                            closed[x2][y2] = 1

    """
        Now the DP part to find path
    """
    current = goal
    result[current[0]][current[1]] = '*'
    min_score = expand[current[0]][current[1]]
    while current != init:
        for i in range(4):
            x = current[0] - delta[i][0]
            y = current[1] - delta[i][1]
            if 0 <= x < len(result) and 0 <= y < len(result[0]) and min_score > expand[x][y]:
                min_score = expand[x][y]
                result[x][y] = delta_name[i]
                current = [x, y]
                break

    # Starting point is still left
    for i in range(4):
        x = init[0] + delta[i][0]
        y = init[1] + delta[i][1]
        if 0 <= x < len(result) and 0 <= y < len(result[0]) and result[x][y] != ' ':
            result[init[0]][init[1]] = delta_name[i]
            break

    return result

for i in search(grid, init, goal, cost):
    print i
