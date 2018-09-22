grid = [[0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [0, 1, 1, 0, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0]]
goal = [0, 6]
cost_step = 1
collision_cost = 100
success_prob = 0.8

delta = [[-1, 0],  # go up
         [0, -1],  # go left
         [1, 0],  # go down
         [0, 1]]  # go right

delta_name = ['^', '<', 'v', '>']  # Use these when creating your policy grid.


def stochastic_value(grid, goal, cost_step, collision_cost, success_prob):
    failure_prob = (1.0 - success_prob) / 2.0  # Probability(stepping left) = prob(stepping right) = failure_prob
    value = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

    progress = True
    while progress:
        progress = False
        for x in range(len(grid)):
            for y in range(len(grid[0])):

                if goal == [x, y]:
                    if value[x][y] > 0:  # check if obstacle
                        value[x][y] = 0
                        policy[x][y] = '*'
                        progress = True

                elif grid[x][y] == 0:  # no obstacle

                    for i in range(len(delta)):
                        neighbours = [[x + delta[i][0], y + delta[i][1]],
                                      [x + delta[i - 1][0], y + delta[i - 1][1]],
                                      [x + delta[(i + 1) % len(delta)][0], y + delta[(i + 1) % len(delta)][1]]]
                        value_new = 0
                        probability_set = [success_prob, failure_prob, failure_prob]

                        for n in neighbours:
                            p = probability_set[neighbours.index(n)]
                            if 0 <= n[0] < len(grid) and 0 <= n[1] < len(grid[0]) and grid[n[0]][n[1]] == 0:
                                value_new += value[n[0]][n[1]] * p
                            else:
                                value_new += collision_cost * p

                        value_new += cost_step

                        if value_new < value[x][y]:
                            progress = True
                            value[x][y] = value_new
                            policy[x][y] = delta_name[i]
    return value, policy

r1, r2 = stochastic_value(grid, goal, cost_step, collision_cost, success_prob)
for r in r2:
    print r
