# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up

def sense(p, Z, pRight, world):
    # Z = Measurement color
    # p = prior prop.
    # pRight = prop. correct measurement
    # world = underlying world

    rows = len(p)
    cols = len(p[0])

    q = [[None for _ in range(cols)] for _ in range(rows)]

    # non normalized
    for r in range(rows):
        for c in range(cols):
            hit = (Z == world[r][c])
            q[r][c] = p[r][c] * (pRight if hit else 1 - pRight)

    # sum
    sum = 0
    for r in range(rows):
        for c in range(cols):
            sum = sum + q[r][c]

    # normalized
    for r in range(rows):
        for c in range(cols):
            q[r][c] = q[r][c] / sum

    return q


def move(p, U, pMove):
    # prior prop.
    # U movement, 2D
    # pMove, prop. that moved correctly otherwise stood
    rows = len(p)
    cols = len(p[0])

    q = [[None for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            s1 = pMove * p[(r-U[0] % rows)][(c-U[1] % cols)]  # moved
            s2 = (1-pMove) * p[r][c]
            q[r][c] = s1 + s2

    return q


def localize(colors, measurements, motions, sensor_right, p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))]
         for col in range(len(colors))]

    # >>> Insert your code here <<<
    for i in range(len(measurements)):
        p = move(p, motions[i], p_move)
        p = sense(p, measurements[i], sensor_right, colors)

    return p


def show(p):
    rows = [
        '[' + ','.join(map(lambda x: '{0:.5f}'.format(x), r)) + ']' for r in p]
    print('[' + ',\n '.join(rows) + ']')


colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R', 'R']
motions = [[0, 0], [0, 1]]

p = localize(colors, measurements, motions, sensor_right=0.8, p_move=0.5)
show(p)  # displays your answer
