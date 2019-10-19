from find_way.base_find_path import Base_Find_Path
import os
# from base_find_path import Base_Find_Path


class Dac_Find_Path(Base_Find_Path):
    """docstring for Dac_Find_Path"""

    def __init__(self, file_name):
        super().__init__(file_name)
        self.current_pos = self.start
        self.visited = [[False] * self.cols] * self.rows
        self.poly_to_pass = 0
        self.adj_poly = [[False] * (self.numPoly + 2)] * (self.numPoly + 2)
        for i in range(self.rows):
            for j in range(self.cols):
                for k in range(8):
                    (x, y) = self.next_cell((i, j), k)
                    if self.is_valid_cell((x, y)):
                        p1 = self.map_mat[i][j]
                        p2 = self.map_mat[x][y]
                        if ((p1 in range(self.numPoly + 2)) and
                                (p2 in range(self.numPoly + 2))):
                            self.adj_poly[p1][p2] = True
                            self.adj_poly[p2][p1] = True

    def cell_next_to_poly(self, cell, polyID):
        if not(self.is_valid_cell(cell)):
            return -1
        ret = []
        for i in range(8):
            (x, y) = self.next_cell(cell, i)
            if not(self.is_valid_cell((x, y))):
                continue
            if (self.map_mat[x][y] in polyID):
                ret.append(i)
        i = 0
        while (i < len(ret)):
            (x0, y0) = self.next_cell(cell, ret[i])
            for d in range(8):
                (x, y) = self.next_cell(cell, d)
                if (not(self.is_valid_cell((x, y))) or (d in ret) or
                        self.map_mat[x][y] in ['S', 'G', 'P', 0]):
                    continue
                if self.is_adjacent_cell((x0, y0), (x, y)):
                    ret.append(d)
            i += 1
        # print(cell, polyID, ret)
        return ret

    def next_2_adjacent_cell(self, polyID, cell=None):
        # dx = [-1, -1, 0, 1, 1, 1, 0, -1, 0]
        # dy = [0, 1, 1, 1, 0, -1, -1, -1, 0]
        d = [1, 2, 1, 2, 1, 2, 1, 2, 1]
        if (cell is None):
            cell = self.current_pos
        adj_poly = []
        for i in self.cell_next_to_poly(cell, [polyID]):
            (x, y) = self.next_cell(cell, i)
            if (self.map_mat[x][y] not in adj_poly):
                adj_poly.append(self.map_mat[x][y])
        # print(cell, polyID, adj_poly)
        next_clockwise = -1
        next_anticlockwise = -1
        for i in range(8):
            if self.move_into_poly(cell, i):
                continue
            (x, y) = self.next_cell(cell, i)
            d_nextto_poly = self.cell_next_to_poly((x, y), adj_poly)
            # print((x, y), i, adj_poly, d_nextto_poly)
            if (len(d_nextto_poly) == 0):
                continue
            is_clockwise = False
            if (i % 2 == 0):
                if ((i + 2) % 8 in d_nextto_poly):
                    is_clockwise = True
            if ((i + 3) % 8 in d_nextto_poly):
                is_clockwise = True
            if (is_clockwise):  # clockwise
                # print('clockwise')
                if (self.cost[next_clockwise] / d[next_clockwise] >
                        self.cost[i] / d[i]):
                    next_clockwise = i
            else:  # anticlockwise
                # print('anticlockwise')
                if (self.cost[next_anticlockwise] / d[next_anticlockwise] >
                        self.cost[i] / d[i]):
                    next_anticlockwise = i
            # # opposite direction
            # j = (i + 4) % 8
            # if (i < j):
            #     # print(i, j)
            #     is_clockwise = False
            #     # for t in d_nextto_poly:
            #     #     if (i < t < j):
            #     #         is_clockwise = True
            #     if ((i + 1) % 8 in d_nextto_poly):
            #         is_clockwise = True
            #     if (is_clockwise):  # clockwise
            #         # print('clockwise')
            #         if (self.cost[next_clockwise] / d[next_clockwise] >
            #                 self.cost[i] / d[i]):
            #             next_clockwise = i
            #     else:  # anticlockwise
            #         # print('anticlockwise')
            #         if (self.cost[next_anticlockwise] / d[next_anticlockwise] >
            #                 self.cost[i] / d[i]):
            #             next_anticlockwise = i
            # else:
            #     # print(i, j)
            #     is_anticlockwise = False
            #     # for t in d_nextto_poly:
            #     #     if (j < t < i):
            #     #         is_anticlockwise = True
            #     if ((i - 1 + 8) % 8 in d_nextto_poly):
            #         is_anticlockwise = True
            #     if (is_anticlockwise):  # anticlockwise
            #         # print('anticlockwise')
            #         if (self.cost[next_anticlockwise] / d[next_anticlockwise] >
            #                 self.cost[i] / d[i]):
            #             next_anticlockwise = i
            #     else:  # clockwise
            #         # print('clockwise')
            #         if (self.cost[next_clockwise] / d[next_clockwise] >
            #                 self.cost[i] / d[i]):
            #             next_clockwise = i
        return (self.next_cell(cell, next_clockwise),
                self.next_cell(cell, next_anticlockwise))

    def move_around_poly(self, start_cell, polyID, move_clockwise=True):
        # print("move_around_poly", start_cell, polyID, move_clockwise)
        (next_clockwise, next_anticlockwise) = \
            self.next_2_adjacent_cell(polyID, start_cell)
        # print("clockwise & anticlock", next_clockwise, next_anticlockwise)
        d = {start_cell: 0}
        prev_cell = start_cell
        if move_clockwise:
            di = self.get_direct(start_cell, next_clockwise)
            (x2, y2) = self.next_cell(start_cell, (di + 1) % 8)
            polyID = self.map_mat[x2][y2]
            # print(start_cell, di, (x2, y2), polyID)
            (x, y) = next_clockwise
        else:
            di = self.get_direct(start_cell, next_anticlockwise)
            (x2, y2) = self.next_cell(start_cell, (di - 1 + 8) % 8)
            polyID = self.map_mat[x2][y2]
            # print(start_cell, di, (x2, y2), polyID)
            (x, y) = next_anticlockwise
        is_circle = True
        s = 0
        i = 0
        while (start_cell != (x, y) and
               # not(self.is_adjacent_cell(start_cell, (x, y))) and
               not((x, y) in d.keys())):
            # print("(x, y) = ", (x, y))
            if (i > 4 * (self.rows + self.cols)) or (prev_cell == (x, y)):
                # print("break, cur_pos = ", self.current_pos, next_clockwise)
                is_circle = False
                break
            c = self.cost[self.get_direct(prev_cell, (x, y))]
            d[(x, y)] = d[prev_cell] + c
            s = s + c
            i = i + 1
            prev_cell = (x, y)
            (next_clockwise, next_anticlockwise) = \
                self.next_2_adjacent_cell(polyID, (x, y))
            # print(next_clockwise, (x, y), next_anticlockwise)
            if move_clockwise:
                di = self.get_direct((x, y), next_clockwise)
                (x2, y2) = self.next_cell((x, y), (di + 1) % 8)
                polyID = self.map_mat[x2][y2]
                # print((x, y), di, (x2, y2), polyID)
                (x, y) = next_clockwise
            else:
                di = self.get_direct((x, y), next_anticlockwise)
                (x2, y2) = self.next_cell((x, y), (di - 1 + 8) % 8)
                polyID = self.map_mat[x2][y2]
                # print((x, y), di, (x2, y2), polyID)
                (x, y) = next_anticlockwise
        # print("end move_around_poly")
        return (is_circle, d)

    def poly_chan_cell(self, cell):
        ret = []
        cur_cell = cell
        while cur_cell != self.goal:
            # polyID = self.map_mat[cur_cell[0]][cur_cell[1]]
            # if polyID not in ['S', 'G', 'P', 0]:
            #     if polyID not in ret:
            #         ret.append(polyID)
            #     for i in range(1, self.numPoly + 2):
            #         if self.adj_poly[polyID][i] and (i not in ret):
            #             ret.append(i)
            _next_cell = cur_cell
            direct = -1
            for i in range(8):
                (x, y) = self.next_cell(cur_cell, i)
                if not(self.is_valid_cell((x, y))):
                    continue
                if (self.euclidean_dist((x, y), self.goal) + self.cost[i] <
                        self.euclidean_dist(_next_cell, self.goal) +
                        self.cost[direct]):
                    _next_cell = (x, y)
                    direct = i
            polyID = self.move_into_poly(cur_cell, direct)
            if polyID > 0:
                if polyID not in ret:
                    ret.append(polyID)
                i = 0
                while i < len(ret):
                    for p in range(1, self.numPoly + 2):
                        if (self.adj_poly[ret[i]][p]) and (p not in ret):
                            ret.append(p)
                    i += 1
            cur_cell = _next_cell
        # print(cell, ret)
        return ret

    def next_move(self):
        _next_cell = self.current_pos
        direct = -1
        for i in range(8):
            # (x_cur, y_cur) = self.current_pos
            # if self.map_mat[x_cur][y_cur] not in ['S', 'G', 'P', 0]:
            #     if self.move_into_poly(self.current_pos, i) == 0:
            #         self.current_pos = self.next_cell(self.current_pos, i)
            #         return
            (x, y) = self.next_cell(self.current_pos, i)
            if not(self.is_valid_cell((x, y))):
                continue
            if (self.euclidean_dist((x, y), self.goal) + self.cost[i] <
                    self.euclidean_dist(_next_cell, self.goal) +
                    self.cost[direct]):
                # print((x, y))
                _next_cell = (x, y)
                direct = i
        # print(self.current_pos, _next_cell, self.poly_to_pass)
        if self.poly_to_pass not in self.poly_chan_cell(self.current_pos):
            self.poly_to_pass = 0
        polyID = self.move_into_poly(self.current_pos, direct)
        if (polyID == 0):
            polyID = self.poly_to_pass
        if (polyID != 0):
            # polyID = self.map_mat[_next_cell[0]][_next_cell[1]]
            # print('move_into_poly', polyID)
            (next_clockwise, next_anticlockwise) = \
                self.next_2_adjacent_cell(polyID)
            # print("clockwise & anticlock", next_clockwise, next_anticlockwise)
            # d = {self.current_pos: 0}
            # prev_cell = self.current_pos
            # (x, y) = next_clockwise
            # s = 0
            # i = 0
            # while (self.current_pos != (x, y) or
            #        not(self.is_adjacent_cell(self.current_pos, (x, y)))):
            #     print("(x, y) = ", (x, y))
            #     if (i > 4 * (self.rows + self.cols)) or (prev_cell == (x, y)):
            #         self.current_pos = next_anticlockwise
            #         print("break, cur_pos =", self.current_pos, next_clockwise)
            #         return
            #     c = self.cost[self.get_direct(prev_cell, (x, y))]
            #     d[(x, y)] = d[prev_cell] + c
            #     s = s + c
            #     i = i + 1
            #     prev_cell = (x, y)
            #     ((x, y), _) = self.next_2_adjacent_cell(polyID, (x, y))
            #     # print(prev_cell, (x, y), _)
            (is_circle, d1) = self.move_around_poly(self.current_pos,
                                                    polyID,
                                                    True)
            (is_circle, d2) = self.move_around_poly(self.current_pos,
                                                    polyID,
                                                    False)
            # print(d1)
            # print(d2)
            b_dist = 2 * (self.rows + self.cols)
            b_cell = self.current_pos
            for cell, dist in d1.items():
                if self.euclidean_dist(cell, self.goal) < b_dist:
                    b_dist = self.euclidean_dist(cell, self.goal)
                    b_cell = cell
            for cell, dist in d2.items():
                if self.euclidean_dist(cell, self.goal) < b_dist:
                    b_dist = self.euclidean_dist(cell, self.goal)
                    b_cell = cell
            # print("b_cell=", b_cell)
            # print((x, y), d[(x, y)], s - d[(x, y)])
            if (b_cell not in d2.keys()):
                # print(b_cell, "not in d2")
                _next_cell = next_clockwise
            elif (b_cell not in d1.keys()):
                # print(b_cell, "not in d1")
                _next_cell = next_anticlockwise
            elif (d1[b_cell] < d2[b_cell]):
                # print(b_cell, "d1 < d2")
                _next_cell = next_clockwise
            else:
                # print(b_cell, "else")
                _next_cell = next_anticlockwise
            direct = self.get_direct(self.current_pos, _next_cell)
            (x, y) = _next_cell
            if _next_cell == next_clockwise:
                (x, y) = self.next_cell(self.current_pos, (direct + 1) % 8)
            else:
                (x, y) = self.next_cell(self.current_pos, (direct - 1 + 8) % 8)
            self.poly_to_pass = self.map_mat[x][y]

        # if self.visited[_next_cell[0]][_next_cell[1]] is True:
        #     for i in range(8):
        #         (x, y) = self.next_cell(self.current_pos, i)
        #         if self.is_valid_cell((x, y)) and self.visited[x][y] is True:
        #             _next_cell = (x, y)
        #             break
        # if self.visited[_next_cell[0]][_next_cell[1]] is True:
        #     _next_cell = self.current_pos
        self.current_pos = _next_cell
        self.visited[self.current_pos[0]][self.current_pos[1]] = True

    def get_path(self):
        self.current_pos = self.start
        path = [self.start]
        i = 0
        while ((i < 4 * (self.rows + self.cols)) and
               (self.current_pos != self.goal)):
            # print(self.current_pos)
            self.next_move()
            path.append(self.current_pos)
            i += 1
        return (len(path), path)


if __name__ == '__main__':
    file_name = input("File name: ")
    if not (os.path.exists(file_name)):
        print("File does not exist! ")
        exit(0)
    m_find_path = Dac_Find_Path(file_name)
    path = m_find_path.get_path()
    print(path)
    exit(0)

    m_find_path = Dac_Find_Path([[0, 0, 1],
                                 [0, 1, 1],
                                 [0, 0, 0]],
                                (0, 0),
                                (2, 2))
    print(m_find_path.get_path())

    m_find_path = Dac_Find_Path([[0, 0, 0, 0, 0, 0],
                                 [0, 0, 1, 1, 1, 0],
                                 [0, 1, 0, 0, 1, 0],
                                 [0, 1, 0, 0, 1, 0],
                                 [0, 1, 0, 0, 1, 0],
                                 [0, 0, 1, 1, 1, 0],
                                 [0, 0, 0, 0, 0, 0]],
                                (6, 0), (0, 5))
    print(m_find_path.get_path())

    m_find_path = Dac_Find_Path(
        [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 'S', 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 2, 0, 0, 2, 2, 2, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 2, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'G', 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
        (2, 2), (16, 19))
    print(m_find_path.get_path())
    # print(m_find_path.next_2_adjacent_cell(2, (9, 9)))
    # print(m_find_path.next_2_adjacent_cell(3, (15, 11)))

    m_find_path = Dac_Find_Path(
        [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 5, 5, 0, 0, 0, 0, 1],
         [1, 0, 'S', 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 5, 5, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 5, 5, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 4, 0, 0, 4, 0, 5, 5, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 2, 0, 0, 2, 2, 2, 0, 4, 0, 0, 4, 0, 5, 5, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 4, 4, 4, 4, 0, 5, 5, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 2, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 5, 5, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 5, 5, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 5, 5, 0, 'G', 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
        (2, 2), (16, 19))
    print(m_find_path.get_path())

    m_find_path = Dac_Find_Path(
        [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 1],
         [1, 0, 0, 'G', 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 1],
         [1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 0, 1],
         [1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 0, 1],
         [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 'S', 0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
        (12, 17), (3, 3))
    print(m_find_path.get_path())

    m_find_path = Dac_Find_Path(
        [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 'G', 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 1],
         [1, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 'S', 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
        (13, 23), (5, 5))
