import abc
import math


class Base_Find_Path(abc.ABC):
    """docstring for Base_Find_Path"""

    dx = [-1, -1, 0, 1, 1, 1, 0, -1, 0]
    dy = [0, 1, 1, 1, 0, -1, -1, -1, 0]
    cost = [1, 1.5, 1, 1.5, 1, 1.5, 1, 1.5, 10]

    def __init__(self, file_name):

        inpfile = open(file_name, "r")
        inp = list(inpfile.readline().replace('\n', '').split(','))
        n = int(inp[0])  # column
        m = int(inp[1])  # row

        inp = list(inpfile.readline().replace('\n', '').split(','))
        for i in range(len(inp)):
            inp[i] = int(inp[i])
        self.ver = inp

        self.start = (inp[1], inp[0])
        self.goal = (inp[3], inp[2])

        self.numPoly = int(inpfile.readline())

        poly = list()
        for i in range(self.numPoly):
            inp = list(inpfile.readline().replace('\n', '').split(','))
            for j in range(len(inp)):
                inp[j] = int(inp[j])
            inp += [inp[0], inp[1]]
            poly.append(inp)

        inpfile.close()

        mat = list()
        for i in range(m + 1):
            col = list()
            for i in range(n + 1):
                col.append(0)
            mat.append(col)

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0 or j == 0 or i == m or j == n:
                    mat[i][j] = 1

        for i in range(self.numPoly):
            for j in range(len(poly[i]) // 2 - 1):
                x1 = poly[i][j * 2 + 1]
                y1 = poly[i][j * 2]
                x2 = poly[i][j * 2 + 3]
                y2 = poly[i][j * 2 + 2]

                if x1 < x2:
                    xx = 1
                else:
                    xx = -1

                if y1 < y2:
                    yy = 1
                else:
                    yy = -1

                dx = abs(x1 - x2) + 1
                dy = abs(y1 - y2) + 1

                if dx >= dy:
                    d = 1
                    cx = dx // dy - 1
                    crx = dx % dy
                else:
                    d = 2
                    cy = dy // dx - 1
                    cry = dy % dx

                while 1:
                    mat[x1][y1] = i + 2
                    if d == 1:
                        tx = cx
                        if crx > 0:
                            tx += 1
                            crx -= 1
                        while tx > 0:
                            x1 += xx
                            tx -= 1
                            mat[x1][y1] = i + 2
                    else:
                        ty = cy
                        if cry > 0:
                            ty += 1
                            cry -= 1
                        while ty > 0:
                            y1 += yy
                            ty -= 1
                            mat[x1][y1] = i + 2

                    if x1 == x2 and y1 == y2:
                        break
                    else:
                        x1 += xx
                        y1 += yy

        self.map_mat = mat
        self.rows = len(mat)
        self.cols = len(mat[0])

    def poly_move(self, direction):
        self.new_map = []
        if direction == 0 or direction == 4:
            for i in range(self.rows):
                x = i
                if x != 0 and x != self.rows - 1:
                    x -= self.dx[direction]
                    if x == 0:
                        x = self.rows - 2
                    if x == self.rows - 1:
                        x = 1
                row = []
                for j in range(self.cols):
                    row.append(self.map_mat[x][j])
                self.new_map.append(row)
        if direction == 2 or direction == 6:
            for i in range(self.rows):
                row = []
                for j in range(self.cols):
                    y = j
                    if y != 0 and y != self.cols - 1:
                        y -= self.dy[direction]
                        if y == 0:
                            y = self.cols - 2
                        if y == self.cols - 1:
                            y = 1
                    row.append(self.map_mat[i][y])
                self.new_map.append(row)

    def update_map_mat(self):
        self.map_mat[self.ver[1]][self.ver[0]] = 'S'
        self.map_mat[self.ver[3]][self.ver[2]] = 'G'
        for i in range(2, len(self.ver) // 2):
            self.map_mat[self.ver[i * 2 + 1]][self.ver[i * 2]] = 'P'

    def get_matrix(self, c):
        mat = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.map_mat[i][j])
            mat.append(row)

        if c is True:
            mat[self.ver[1]][self.ver[0]] = 'S'
            mat[self.ver[3]][self.ver[2]] = 'G'
        else:
            self.new_map[self.ver[1]][self.ver[0]] = 0
            self.new_map[self.ver[3]][self.ver[2]] = 0
            for i in range(self.rows):
                for j in range(self.cols):
                    if mat[i][j] == self.new_map[i][j]:
                        mat[i][j] = 0
                        continue
                    if mat[i][j] == 0 and self.new_map[i][j] != 0:
                        mat[i][j] = -1

        return mat

    def next_cell(self, cell, direction):
        assert (-1 <= direction < 8), "0-7 to move or -1 to stand (not move)"
        return (cell[0] + self.dx[direction], cell[1] + self.dy[direction])

    def get_direct(self, cell1, cell2):
        for i in range(8):
            if ((cell2[0] - cell1[0] == self.dx[i]) and
                    (cell2[1] - cell1[1] == self.dy[i])):
                return i
        return -1

    def is_adjacent_cell(self, cell1, cell2):
        for i in range(8):
            if ((cell2[0] - cell1[0] == self.dx[i]) and
                    (cell2[1] - cell1[1] == self.dy[i])):
                return True
        return False

    def is_valid_cell(self, cell):
        return ((0 <= cell[0] < self.rows) and (0 <= cell[1] < self.cols))

    def move_cross_edge(self, cell, direction):
        (x, y) = self.next_cell(cell, direction)
        if not(self.is_valid_cell((x, y))):
            return -1
        if self.map_mat[x][y] not in ['S', 'G', 'P', 0]:
            return self.map_mat[x][y]
        if direction % 2 != 0:
            d1 = (direction - 1 + 8) % 8
            (x1, y1) = self.next_cell(cell, d1)
            d2 = (direction + 1 + 8) % 8
            (x2, y2) = self.next_cell(cell, d2)
            if ((self.is_valid_cell((x1, y1))) and
                (self.is_valid_cell((x2, y2))) and
                (self.map_mat[x1][y1] != 0) and
                    (self.map_mat[x2][y2] != 0)):
                return self.map_mat[x1][y1]
        return 0

    def try_move_out_poly(self, cell, polyID, visited):
        visited[cell[0]][cell[1]] = True
        if self.map_mat[cell[0]][cell[1]] == polyID:
            return False
        for i in range(8):
            (x, y) = self.next_cell(cell, i)
            if self.map_mat[x][y] not in [polyID, 'S', 'G', 'P', 0]:
                return True
            if self.move_cross_edge(cell, i) == 0 and not(visited[x][y]):
                can_move = self.try_move_out_poly((x, y), polyID, visited)
                if can_move:
                    return can_move
        return False

    def move_into_poly(self, cell, direction):
        (x, y) = self.next_cell(cell, direction)
        if not(self.is_valid_cell((x, y))):
            return -1
        for i in range(2, self.numPoly + 2):
            visited = [[False] * self.cols] * self.rows
            if self.try_move_out_poly((x, y), i, visited) is False:
                return i
        return self.move_cross_edge(cell, direction)
        return 0

    def euclidean_dist(self, cell1, cell2):
        return math.sqrt(sum([(a - b) ** 2 for a, b in zip(cell1, cell2)]))

    @abc.abstractmethod
    def get_path(self):
        pass