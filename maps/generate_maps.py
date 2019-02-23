from random import random

def build_grid():

    for counter in range(1, 51):
        grid = []
        for row in range(101):
            grid.append([])
            for col in range(101):
                grid[row].append(0)
        gridLength = len(grid)
        for i in range(gridLength):
            for j in range(gridLength):
                if random() < 0.70:
                    continue
                else:
                    grid[i][j] = 1
        grid[0][0] = 2
        grid[gridLength - 1][gridLength - 1] = -1

        filename = "map_{}.txt".format(counter)
        f = open(filename, "w")
        f.write("{}".format(grid))
        f.close()


if __name__ == "__main__":
    build_grid()