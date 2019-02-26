
import timeit
from AStar import *


def Average(lst):
    return sum(lst) / len(lst)


def main():
    F_A = []
    B_A = []
    A_A = []

    for number in range(1, 51):
        filename = "map_{}.txt".format(number)
        f = open("maps/{}".format(filename), "r")
        str_grid = f.read()
        f.close()
        grid = eval(str_grid)
        start_state = (0, 0)
        goal_state = (len(grid) - 1, len(grid) - 1)
        rows = len(grid)

        a_star = AStar(rows, start_state, goal_state)

        start = timeit.default_timer()
        a_star.traverse_path(grid, "forward")
        stop = timeit.default_timer()

        F_A.append(stop - start)

        start = timeit.default_timer()
        a_star.traverse_path(grid, "backward")
        stop = timeit.default_timer()

        B_A.append(stop - start)

        start = timeit.default_timer()
        a_star.traverse_path(grid, "adaptive")
        stop = timeit.default_timer()

        A_A.append(stop - start)

    print("Forward A* average: {}".format(Average(F_A)))
    print("Backward A* average: {}".format(Average(B_A)))
    print("Adaptive A* average: {}".format(Average(A_A)))

    # Forward A * average: 7.828401298599999
    # Backward A * average: 4.9869322524399955
    # Adaptive A * average: 1.9747656781799916


if __name__ == "__main__":
    main()