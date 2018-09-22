from numpy import ones, multiply

"""
    Here is a planner that helps a robot
    find the shortest way in a warehouse filled with boxes
    to be picked and deliver to a drop zone.

    For example:

    warehouse = [[ 1, 2, 3],
                 [ 0, 0, 0],
                 [ 0, 0, 0]]
    dropzone = [2,0]
    todo = [2, 1]

    The robot starts at the dropzone.
    The dropzone can be in any free corner of the warehouse map.
    todo is a list of boxes to be picked up and delivered to the dropzone.

    Robot can move diagonally, but the cost of a diagonal move is 1.5.
    The cost of moving one step horizontally or vertically is 1.
    So if the dropzone is at [2, 0], the cost to deliver box number 2
    would be 5.

    To pick up a box, the robot has to move into the same cell as the box.
    When the robot picks up a box, that cell becomes passable (marked 0)
    The robot can pick up only one box at a time and once picked up
    it has to return the box to the dropzone by moving onto the dropzone cell.
    Once the robot has stepped on the dropzone, the box is taken away,
    and it is free to continue with its todo list.
    Tasks must be executed in the order that they are given in the todo list.
    You may assume that in all warehouse maps, all boxes are
    reachable from beginning (the robot is not boxed in).
"""


def heuristic(init, x, y):
    return abs(init[0] - x) + abs(init[1] - y)


def get_cost(grid, goal, dropzone):
    """
    Modified DP

    :returns: Cost for given goal and dropzone
    """
    values = multiply(ones((len(grid), len(grid[0]))), -1)
    open_set = [goal]

    delta = [[-1, 0],  # go up
             [0, -1],  # go left
             [1, 0],  # go down
             [0, 1]]  # go right

    beta = [[-1, 1],
            [1, -1],
            [1, 1],
            [-1, -1]]

    """
        Blocking those blocks which are occupied
    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != 0:
                values[i][j] = 99

    while open_set:
        [curr_x, curr_y] = [open_set[0][0], open_set[0][1]]
        open_set.remove(open_set[0])

        """
            Creating set of neighbours
            Format [Value,x,y,type]
            Type = 'd' => selected due to Delta, else 'b'
        """
        neighbours = []
        for d in delta:
            x = curr_x + d[0]
            y = curr_y + d[1]
            if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                neighbours.append([values[x][y], x, y, 'd'])

        for d in beta:
            x = curr_x + d[0]
            y = curr_y + d[1]
            if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                neighbours.append([values[x][y], x, y, 'b'])

        # separating them into valid(with some positive value) and new
        new = []
        valid = []
        for n in neighbours:
            if n[0] == -1:
                new.append([n[1], n[2]])
            elif n[0] != 99:
                valid.append(n)

        """
            Setting value of the current cell
            Select min value neighbour from surroundings
        """

        if valid:
            valid.sort()
            values[curr_x][curr_y] = valid[0][0] + {'d': 1, 'b': 1.5}[valid[0][3]]
        else:
            values[curr_x][curr_y] = 0

        # appending new to list of open cells
        for n in new:
            open_set.append(n)

    # What if 'values' has unreachable cells?
    for i in range(len(values)):
        for j in range(len(values[0])):
            if values[i][j] == -1:
                values[i][j] = 99

    # TODO 'return values' for debugging
    return values[dropzone[0]][dropzone[1]]


def plan(warehouse, dropzone, todo):
    """
    :param warehouse:  grid of values, where 0 means that the cell is passable,
                        and a number 1 <= n <= 99 means that box n is located at that cell.
    :param dropzone:   determines the robot's start location and the place to return boxes
    :param todo:       list of tasks, containing box numbers that have to be picked up
    :return: Cost to take all boxes in the todo list to dropzone
    """
    cost = 0

    warehouse[dropzone[0]][dropzone[1]] = 0  # coz of the 'x'
    goals = dict()
    for i in range(len(warehouse)):
        for j in range(len(warehouse[0])):
            if warehouse[i][j] in todo:
                goals[warehouse[i][j]] = (i, j)

    for t in todo:
        # Note doing opposite way is important
        cost += get_cost(warehouse, dropzone=dropzone, goal=goals[t])
        warehouse[goals[t][0]][goals[t][1]] = 0

    return 2 * cost
    # TODO 'print get_cost(warehouse, dropzone=dropzone, goal=goals[0])' for debugging


def solution_check(test, epsilon=0.00001):
    answer_list = []

    import time
    start = time.clock()
    correct_answers = 0
    for i in range(len(test[0])):
        user_cost = plan(test[0][i], test[1][i], test[2][i])
        true_cost = test[3][i]
        if abs(user_cost - true_cost) < epsilon:
            print "\nTest case", i + 1, "passed!"
            answer_list.append(1)
            correct_answers += 1
        else:
            print "\nTest case ", i + 1, "unsuccessful. Your answer ", user_cost, "was not within ", epsilon, "of ", \
                true_cost
            answer_list.append(0)
    runtime = time.clock() - start
    if runtime > 1:
        print "Your code is too slow, try to optimize it! Running time was: ", runtime
        return False
    if correct_answers == len(answer_list):
        print "\nYou passed all test cases!"
        return True
    else:
        print "\nYou passed", correct_answers, "of", len(answer_list), "test cases. Try to get them all!"
        return False


# Testing environment
# Test Case 1
warehouse1 = [[1, 2, 3],
              [0, 0, 0],
              [0, 0, 0]]
dropzone1 = [2, 0]
todo1 = [2, 1]
true_cost1 = 9
# Test Case 2
warehouse2 = [[1, 2, 3, 4],
              [0, 0, 0, 0],
              [5, 6, 7, 0],
              ['x', 0, 0, 8]]
dropzone2 = [3, 0]
todo2 = [2, 5, 1]
true_cost2 = 21

# Test Case 3
warehouse3 = [[1, 2, 3, 4, 5, 6, 7],
              [0, 0, 0, 0, 0, 0, 0],
              [8, 9, 10, 11, 0, 0, 0],
              ['x', 0, 0, 0, 0, 0, 12]]
dropzone3 = [3, 0]
todo3 = [5, 10]
true_cost3 = 18

# Test Case 4
warehouse4 = [[1, 17, 5, 18, 9, 19, 13],
              [2, 0, 6, 0, 10, 0, 14],
              [3, 0, 7, 0, 11, 0, 15],
              [4, 0, 8, 0, 12, 0, 16],
              [0, 0, 0, 0, 0, 0, 'x']]
dropzone4 = [4, 6]
todo4 = [13, 11, 6, 17]
true_cost4 = 41

testing_suite = [[warehouse1, warehouse2, warehouse3, warehouse4],
                 [dropzone1, dropzone2, dropzone3, dropzone4],
                 [todo1, todo2, todo3, todo4],
                 [true_cost1, true_cost2, true_cost3, true_cost4]]

solution_check(testing_suite)  # UNCOMMENT THIS LINE TO TEST YOUR CODE
# print plan(warehouse2, dropzone2, todo2)
