import abc
import math


class Base_Find_Path(abc.ABC):
    """docstring for Base_Find_Path"""

    dx = [-1, -1, 0, 1, 1, 1, 0, -1, 0]
    dy = [0, 1, 1, 1, 0, -1, -1, -1, 0]
    cost = [1, 1.5, 1, 1.5, 1, 1.5, 1, 1.5, 10]

    def __init__(self, map_mat, start, goal):
        self.map_mat = map_mat
        self.rows = len(map_mat)
        self.cols = len(map_mat[0])
        self.start = start
        self.goal = goal

    def next_cell(self, cell, direction):
        assert (-1 <= direction < 8), "0-7 to move or -1 to stand (not move)"
        return (cell[0] + self.dx[direction], cell[1] + self.dy[direction])

    def get_direct(self, cell1, cell2):
        for i in range(8):
            if ((cell2[0] - cell1[0] == self.dx[i]) and
                    (cell2[1] - cell1[1] == self.dy[i])):
                return i
        return -1

    def is_valid_cell(self, cell):
        return ((0 <= cell[0] < self.rows) and (0 <= cell[1] < self.cols))

    def move_into_poly(self, cell, direction):
        (x, y) = self.next_cell(cell, direction)
        if not(self.is_valid_cell((x, y))):
            return True
        if ((self.map_mat[x][y] != 0) and
                (self.map_mat[x][y] != 'S') and
                (self.map_mat[x][y] != 'G')):
            return True
        if direction % 2 != 0:
            d1 = (direction - 1 + 8) % 8
            (x1, y1) = self.next_cell(cell, d1)
            d2 = (direction + 1 + 8) % 8
            (x2, y2) = self.next_cell(cell, d2)
            if ((self.is_valid_cell((x1, y1))) and
                (self.is_valid_cell((x2, y2))) and
                    (self.map_mat[x1][y1] == self.map_mat[x2][y2])):
                return True
        return False

    def cell_next_to_poly(self, cell, polyID):
        if not(self.is_valid_cell(cell)):
            return -1
        for i in range(8):
            (x, y) = self.next_cell(cell, i)
            if not(self.is_valid_cell((x, y))):
                continue
            if (self.map_mat[x][y] == polyID):
                return i
        return -1

    def euclidean_dist(self, cell1, cell2):
        return math.sqrt(sum([(a - b) ** 2 for a, b in zip(cell1, cell2)]))

    @abc.abstractmethod
    def get_path(self):
        pass
