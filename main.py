import timeit
from AStar import *
import pygame
import random


def draw_fog(screen, grid, rows):
    for row in range(rows):
        for column in range(rows):
            if((grid[row][column] == 1) or (grid[row][column] == 0)):
                color = GREY
                pygame.draw.rect(screen, color,
                                 [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
            elif grid[row][column] == 2:
                color = RED
                pygame.draw.rect(screen, color,
                                 [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH,
                                  HEIGHT])
            elif grid[row][column] == -1:
                color = GREEN
                pygame.draw.rect(screen, color,
                                 [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH,
                                  HEIGHT])


def draw(screen, grid, rows):
    for row in range(rows):
        for column in range(rows):
            color = WHITE
            if grid[row][column] == 1:
                color = BLACK
            pygame.draw.rect(screen, color,
                             [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

            if grid[row][column] == 2:
                color = RED
                pygame.draw.rect(screen, color,
                                 [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH,
                                  HEIGHT])
            if grid[row][column] == -1:
                color = GREEN
                pygame.draw.rect(screen, color,
                                 [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH,
                                  HEIGHT])


def main():
    number = input("Please enter map number: ")
    filename = "map_{}.txt".format(number)
    f = open("maps/{}".format(filename), "r")
    str_grid = f.read()
    f.close()
    grid = eval(str_grid)

    # grid = []
    # for row in range(101):
    #     grid.append([])
    #     for col in range(101):
    #         grid[row].append(0)
    # gridLength = len(grid)
    # for i in range(gridLength):
    #     for j in range(gridLength):
    #         if random.random() < 0.80:
    #             continue
    #         else:
    #             grid[i][j] = 1
    # grid[0][0] = 2
    # grid[gridLength - 1][gridLength - 1] = -1

    start_state = (0, 0)
    goal_state = (len(grid)-1, len(grid)-1)
    rows = len(grid)

    pygame.display.init()
    screen = pygame.display.set_mode(((rows*6)+1, (rows*6)+1))
    pygame.display.set_caption("A* PathFinder")

    halt = False

    draw(screen, grid, rows)
    pygame.display.flip()

    a_star = AStar(rows, screen, start_state, goal_state)
    while not halt:
        counter = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                halt = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    draw(screen, grid, rows)
                    pygame.display.flip()
                elif event.key == pygame.K_RETURN:
                    draw_fog(screen, grid, rows)
                    pygame.display.flip()
                elif event.key == pygame.K_f:
                    start = timeit.default_timer()
                    paths, blocked_list, closed_list = a_star.traverse_path(grid, "forward")
                    stop = timeit.default_timer()
                    for node in blocked_list:
                            pygame.draw.rect(screen, BLACK,
                                             [(MARGIN + WIDTH) * node[1] + MARGIN, (MARGIN + HEIGHT) * node[0] + MARGIN,
                                              WIDTH, HEIGHT])
                    for path in paths:
                        for node in path:
                            counter +=1
                            pygame.draw.rect(screen, YELLOW,
                                             [(MARGIN + WIDTH) * node[1] + MARGIN, (MARGIN + HEIGHT) * node[0] + MARGIN,
                                              WIDTH, HEIGHT])
                    pygame.display.update()
                    time = stop - start
                    print('Forward A*. Time Taken: {} secs, Distance: {}'.format(time, counter))
                    a_star.re_init()

                elif event.key == pygame.K_b:
                    start = timeit.default_timer()
                    paths, blocked_list, closed_list = a_star.traverse_path(grid, "backward")
                    stop = timeit.default_timer()
                    for node in blocked_list:
                            pygame.draw.rect(screen, BLACK,
                                             [(MARGIN + WIDTH) * node[1] + MARGIN, (MARGIN + HEIGHT) * node[0] + MARGIN,
                                              WIDTH, HEIGHT])
                    for path in paths:
                        for node in path:
                            counter += 1
                            pygame.draw.rect(screen, YELLOW,
                                             [(MARGIN + WIDTH) * node[1] + MARGIN, (MARGIN + HEIGHT) * node[0] + MARGIN,
                                              WIDTH, HEIGHT])
                    pygame.display.update()
                    time = stop - start
                    print('Backwards A*. Time Taken: {} secs, Distance: {},'.format(time, counter))
                    a_star.re_init()
                elif event.key == pygame.K_a:
                    start = timeit.default_timer()
                    paths, blocked_list, closed_list = a_star.traverse_path(grid, "adaptive")
                    stop = timeit.default_timer()
                    for node in blocked_list:
                        pygame.draw.rect(screen, BLACK,
                                         [(MARGIN + WIDTH) * node[1] + MARGIN, (MARGIN + HEIGHT) * node[0] + MARGIN,
                                          WIDTH, HEIGHT])
                    for path in paths:
                        for node in path:
                            counter += 1
                            pygame.draw.rect(screen, YELLOW,
                                             [(MARGIN + WIDTH) * node[1] + MARGIN, (MARGIN + HEIGHT) * node[0] + MARGIN,
                                              WIDTH, HEIGHT])
                    pygame.display.update()
                    time = stop - start
                    print('Adaptive A*. Time Taken: {} secs, Distance: {}'.format(time, counter))
                    a_star.re_init()


if __name__ == "__main__":
    main()
