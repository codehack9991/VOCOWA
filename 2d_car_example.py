# You are given a car in a grid with initial state
# init = [x-position, y-position, orientation]
# where x/y-position is its position in a given
# grid and orientation is 0-3 corresponding to 'up',
# 'left', 'down' or 'right'.
#
# Your task is to compute and return the car's optimal
# path to the position specified in `goal'; where
# the costs for each motion are as defined in `cost'.

# EXAMPLE INPUT:

# grid format:
#     0 = navigable space
#     1 = occupied space
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]
goal = [2, 0]  # final position
init = [4, 3, 0]  # first 2 elements are coordinates, third is direction
cost = [2, 1, 20]  # the cost field has 3 values: right turn, no turn, left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D() should return the array
#
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
#
# ----------


# there are four motion directions: up/left/down/right
# increasing the index in this array corresponds to
# a left turn. Decreasing is is a right turn.

forward = [[-1, 0],  # go up
           [0, -1],  # go left
           [1, 0],  # go down
           [0, 1]]  # do right
forward_name = ['up', 'left', 'down', 'right']

# the cost field has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']


def optimum_policy2D():
    """
    This algorithm keeps track of all the paths through the grid. It
    always expands the least expensive path, thus avoiding unnecessary
    work on paths that are too expensive to follow.

    A path starts at the initial position. Each time a new position is
    found, a Cell object is created to represent that position. This
    new cell has a `previous` member that points to the cell and
    action that created it.

    We maintain the heads of all the paths in a priority queue. This
    means that all the paths are sorted by cost, so every time we pick
    a cell from the queue, we pick up the one with the smallest
    cost.

    Once we have a cell that reaches the goal, we conclude the
    algorithm, since it means we found the least expensive path from
    `init` to `goal`.
    """
    from heapq import heappush, heappop

    def action_from_directions(current, previous):
        """Given two directions, returns the action to take to move
        from one to another.
        """
        action_to_take = (current - previous + 4) % 4
        if action_to_take == 0:
            return 1  # There is no change in direction
        elif action_to_take == 1:
            return 2  # Left turn
        elif action_to_take == 2:
            return None  # U-turn. This is prohibited, so ignore it
        elif action_to_take == 3:
            return 0  # Right turn

    class Cell:
        """
        Simple linked list representation of a path through the grid.

        A Cell object holds the following:

        - x, y coordinates of a cell in the grid
        - the cost of the path starting at `init` and ending with the cell
        - the action that needs to be done to move from the previous
          cell to this one
        - the previous cell
        """

        def __init__(self, x, y, direction, cost=0, action=None, previous=None):
            self.x = x
            self.y = y
            self.direction = direction
            self.action = action
            self.previous = previous
            self.cost = cost

        def __repr__(self):
            previous = None
            if self.previous:
                previous = (self.previous.x, self.previous.y)

            action = None
            if not self.action is None:
                action = action_name[self.action]
            return "{x=%s, y=%s, direction=%s, action=%s, cost=%s, prev=%s}" % (
                self.x, self.y, forward_name[self.direction],
                action, self.cost, previous)

    policy2D = [[' ' for e in row] for row in grid]

    [x, y, direction] = init
    cell = Cell(x, y, direction, action=1)

    # The priority queue. Elements in `paths` are [cost, cell]. The
    # cost is the cost of the path starting at `init` and ending in
    # `cell`. The cell maintains a link to the the previous cell in
    # the path.
    paths = []
    heappush(paths, [cell.cost, cell])

    best_path = []
    while paths:
        # Pick the path with the lowest cost.
        [path_cost, cell] = heappop(paths)
        if [cell.x, cell.y] == goal:
            # We reached our goal. Compute the best path by walking
            # backwards from the goal cell.
            actstr = '*'
            while cell:
                policy2D[cell.x][cell.y] = actstr
                best_path.append(cell)
                actstr = action_name[cell.action]
                cell = cell.previous
            best_path.reverse()
            break
        for current_direction in range(len(forward)):
            f = forward[current_direction]
            dx, dy = cell.x + f[0], cell.y + f[1]
            if dx < 0 or dx > len(grid) - 1:
                continue
            if dy < 0 or dy > len(grid[0]) - 1:
                continue
            # Skip if the cell is a wall brick
            if grid[dx][dy] == 1:
                continue
            action = action_from_directions(current_direction, cell.direction)
            actname = None
            if not action is None:
                actname = action_name[action]
            if action is None:
                continue
            # Update the cost of the path so far
            new_path_cost = path_cost + cost[action]
            new_cell = Cell(dx, dy, current_direction, cost=new_path_cost,
                            action=action, previous=cell)
            heappush(paths, [new_cell.cost, new_cell])

    return policy2D  # Make sure your function returns the expected grid.


for r in optimum_policy2D():
    print r
