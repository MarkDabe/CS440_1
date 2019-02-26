from heapq import *
from random import shuffle
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (211, 211, 211)

WIDTH = 5
HEIGHT = 5
MARGIN = 1

NEIGHBOURS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class AStar:

    def __init__(self, grid_size, screen, start_state, goal_state):
        self.grid_size = grid_size
        self.screen = screen
        self.start_state = start_state
        self.goal_state = goal_state
        self.f = {}
        self.h = {}
        self.g = {}
        self.closed_list = set()
        self.blocked = set()
        self.grid = []

    def re_init(self):
        self.f = {}
        self.g = {}
        self.h = {}
        self.closed_list = set()
        self.blocked = set()
        self.grid = []

    @classmethod
    def manhattan_distance(cls, s1, s2):
        return abs(s1[0] - s2[0]) + abs(s1[1] - s2[1])

    def compute_path_adaptive(self, start):
        closed_list = set()

        came_from = {}

        open_list = []

        g_score = {start: 0}

        h_score = {start: self.h.get(start, AStar.manhattan_distance(start, self.goal_state))}

        f_score = {start: h_score[start] + g_score[start]}

        heappush(open_list, (f_score[start], start))

        while open_list:

            smallest_f = open_list[0][0]

            pointer = 0

            tie_breaking_list = []

            list_len = len(open_list)

            while pointer < list_len and open_list[pointer][0] == smallest_f :
                temp = open_list[pointer]
                # temp2 = (101 * temp[0] - g_score[temp[1]], temp[1])
                temp2 = (101 * temp[0] + g_score[temp[1]], temp[1])
                heappush(tie_breaking_list, temp2)
                pointer += 1
            current = heappop(tie_breaking_list)
            pointer = 0
            while True:
                if open_list[pointer][1] == current[1]:
                    open_list.remove(open_list[pointer])
                    break
                pointer +=1
            heapify(open_list)
            current = current[1]

            # current = heappop(open_list)[1]

            if current == self.goal_state:
                total_path = []
                while current in came_from:
                    total_path.append(current)
                    current = came_from[current]
                gd = len(total_path)
                total_path.append(start)
                for node in closed_list:
                    self.h[node] = gd - g_score[node]
                self.h[self.goal_state] = 0
                return total_path

            closed_list.add(current)
            self.closed_list.add(current)

            # shuffle(NEIGHBOURS)
            for i, j in NEIGHBOURS:

                neighbor = current[0] + i, current[1] + j

                if (self.grid_size <= neighbor[0]) or (neighbor[0] < 0) or \
                        (self.grid_size <= neighbor[1]) or (neighbor[1] < 0) or (neighbor in self.blocked):
                    continue

                else:
                    neighbour_g_score = g_score[current] + 1

                    neighbor_previous_g_score = g_score.get(neighbor, 0)

                    # if (neighbor in closed_list) and (neighbour_g_score >= neighbor_previous_g_score):
                    #     continue

                    if neighbor in closed_list:
                        continue

                    # if (neighbour_g_score < neighbor_previous_g_score) or (neighbor not in [i[1] for i in open_list]):
                    if neighbour_g_score < neighbor_previous_g_score or neighbor_previous_g_score == 0:
                        if neighbour_g_score < neighbor_previous_g_score:
                            open_list.remove((f_score[neighbor], neighbor))
                            heapify(open_list)

                        came_from[neighbor] = current
                        g_score[neighbor] = neighbour_g_score

                        h_score[neighbor] = self.h.get(neighbor, AStar.manhattan_distance(neighbor, self.goal_state))

                        f_score[neighbor] = neighbour_g_score + h_score[neighbor]
                        # self.closed_list.add(neighbor)
                        heappush(open_list, (f_score[neighbor], neighbor))
        return False

    def compute_path(self, start, state):

        closed_list = set()

        came_from = {}

        open_list = []

        if state == "forward":

            self.closed_list.add(start)

            g_score = {start: 0}

            h_score = {start: AStar.manhattan_distance(start, self.goal_state)}

            f_score = {start: AStar.manhattan_distance(start, self.goal_state)}

            heappush(open_list, (f_score[start], start))

        else:

            self.closed_list.add(self.goal_state)

            g_score = {self.goal_state: 0}

            h_score = {self.goal_state: AStar.manhattan_distance(self.goal_state, start)}

            f_score = {self.goal_state: AStar.manhattan_distance(self.goal_state, start)}

            heappush(open_list, (f_score[self.goal_state], self.goal_state))

        while open_list:

            smallest_f = open_list[0][0]

            pointer = 0

            tie_breaking_list = []

            list_len = len(open_list)

            while pointer < list_len and open_list[pointer][0] == smallest_f :
                temp = open_list[pointer]
                # temp2 = (101 * temp[0] - g_score[temp[1]], temp[1])
                temp2 = (101 * temp[0] + g_score[temp[1]], temp[1])
                heappush(tie_breaking_list, temp2)
                pointer += 1
            current = heappop(tie_breaking_list)
            pointer = 0
            while True:
                if open_list[pointer][1] == current[1]:
                    open_list.remove(open_list[pointer])
                    break
                pointer += 1
            heapify(open_list)
            current = current[1]

            # current = heappop(open_list)[1]

            if ((state == "forward" and current == self.goal_state) or
                (state == "backward" and current == start)):

                total_path = []
                while current in came_from:
                    total_path.append(current)
                    current = came_from[current]

                if state == "forward":
                    total_path.append(start)
                else:
                    total_path.append(self.goal_state)
                return total_path

            closed_list.add(current)
            self.closed_list.add(current)

            # shuffle(NEIGHBOURS)
            for i, j in NEIGHBOURS:

                neighbor = current[0] + i, current[1] + j

                if (self.grid_size <= neighbor[0]) or (neighbor[0] < 0) or\
                        (self.grid_size <= neighbor[1]) or (neighbor[1] < 0) or (neighbor in self.blocked):
                    continue

                else:
                    neighbour_g_score = g_score[current] + 1

                    neighbor_previous_g_score = g_score.get(neighbor, 0)

                    # if (neighbor in closed_list) and (neighbour_g_score >= tentative_previous_g_score):
                    #     continue

                    if neighbor in closed_list:
                        continue

                    # if (neighbour_g_score < tentative_previous_g_score) or (neighbor not in [i[1] for i in open_list]):

                    if neighbour_g_score < neighbor_previous_g_score or neighbor_previous_g_score == 0:
                        if neighbour_g_score < neighbor_previous_g_score:
                            open_list.remove((f_score[neighbor], neighbor))
                            heapify(open_list)

                        came_from[neighbor] = current
                        g_score[neighbor] = neighbour_g_score

                        if state == "forward":

                            h_score[neighbor] = AStar.manhattan_distance(neighbor, self.goal_state)

                            f_score[neighbor] = neighbour_g_score + h_score[neighbor]

                        elif state == "backward":

                            h_score[neighbor] = AStar.manhattan_distance(neighbor, start)

                            f_score[neighbor] = neighbour_g_score + h_score[neighbor]

                        # self.closed_list.add(neighbor)
                        heappush(open_list, (f_score[neighbor], neighbor))
        return False

    def traverse_path(self, array, state):

        paths = []

        start = self.start_state

        check = None

        path = None

        while check != self.goal_state:
            if state == "adaptive":
                path = self.compute_path_adaptive(start)
            else:
                path = self.compute_path(start, state)

            if path is False:
                print("Path not found")
                return [[], ], set(), set()

            if state == "forward" or state == "adaptive":
                path.reverse()

            for node in path:
                if array[node[0]][node[1]] == 1:
                    blocked_index = path.index(node)
                    path = path[:blocked_index]
                    paths.append(path)
                    pivot = path[blocked_index - 1]
                    for i, j in NEIGHBOURS:
                        neighbor = pivot[0] + i, pivot[1] + j
                        if (self.grid_size <= neighbor[0]) or (neighbor[0] < 0) or\
                                (self.grid_size <= neighbor[1]) or (neighbor[1] < 0) or\
                                (array[neighbor[0]][neighbor[1]] == 1):
                                    self.blocked.add(neighbor)
                    start = pivot
                    break

                else:
                    check = node

        paths.append(path)

        self.closed_list = self.closed_list - self.blocked

        result = (paths, self.blocked, self.closed_list)

        return result