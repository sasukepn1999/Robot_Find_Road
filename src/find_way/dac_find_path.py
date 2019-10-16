from find_way.base_find_path import Base_Find_Path
import os
# from base_find_path import Base_Find_Path


class Dac_Find_Path(Base_Find_Path):
    """docstring for Dac_Find_Path"""

    def __init__(self, file_name):
        super().__init__(file_name)
        self.current_pos = self.start

    def cell_next_to_poly(self, cell, polyID):
        if not(self.is_valid_cell(cell)):
            return -1
        ret = []
        for i in range(8):
            (x, y) = self.next_cell(cell, i)
            if not(self.is_valid_cell((x, y))):
                continue
            if (self.map_mat[x][y] == polyID):
                ret.append(i)
        return ret

    def next_2_adjacent_cell(self, polyID, cell=None):
        # dx = [-1, -1, 0, 1, 1, 1, 0, -1, 0]
        # dy = [0, 1, 1, 1, 0, -1, -1, -1, 0]
        d = [1, 2, 1, 2, 1, 2, 1, 2, 1]
        if (cell is None):
            cell = self.current_pos
        next_clockwise = -1
        next_anticlockwise = -1
        for i in range(8):
            if self.move_into_poly(cell, i):
                continue
            (x, y) = self.next_cell(cell, i)
            d_nextto_ploy = self.cell_next_to_poly((x, y), polyID)
            # print((x, y), d_nextto_ploy)
            if (len(d_nextto_ploy) == 0):
                continue
            # opposite direction
            j = (i + 4) % 8
            if (i < j):
                # print(i, j)
                is_clockwise = False
                for t in d_nextto_ploy:
                    if (i < t < j):
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
            else:
                # print(i, j)
                is_clockwise = False
                for t in d_nextto_ploy:
                    if (j < t < i):
                        is_clockwise = True
                if (j <= t < i):  # anticlockwise
                    # print('anticlockwise')
                    if (self.cost[next_anticlockwise] / d[next_anticlockwise] >
                            self.cost[i] / d[i]):
                        next_anticlockwise = i
                else:  # clockwise
                    # print('clockwise')
                    if (self.cost[next_clockwise] / d[next_clockwise] >
                            self.cost[i] / d[i]):
                        next_clockwise = i
        return (self.next_cell(cell, next_clockwise),
                self.next_cell(cell, next_anticlockwise))

    def move_around_poly(self, start_cell, polyID, move_clockwise=True):
        (next_clockwise, next_anticlockwise) = \
            self.next_2_adjacent_cell(polyID, start_cell)
        # print("clockwise & anticlock", next_clockwise, next_anticlockwise)
        d = {start_cell: 0}
        prev_cell = start_cell
        if move_clockwise:
            (x, y) = next_clockwise
        else:
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
            # print(prev_cell, (x, y), _)
            if move_clockwise:
                (x, y) = next_clockwise
            else:
                (x, y) = next_anticlockwise
        return (is_circle, d)

    def next_move(self):
        _next_cell = self.current_pos
        direct = -1
        for i in range(8):
            (x, y) = self.next_cell(self.current_pos, i)
            if not(self.is_valid_cell((x, y))):
                continue
            if (self.euclidean_dist((x, y), self.goal) + self.cost[i] <
                    self.euclidean_dist(_next_cell, self.goal) +
                    self.cost[direct]):
                # print((x, y))
                _next_cell = (x, y)
                direct = i
        # print(self.current_pos, _next_cell)
        polyID = self.move_into_poly(self.current_pos, direct)
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
                self.current_pos = next_clockwise
            elif (b_cell not in d1.keys()):
                # print(b_cell, "not in d1")
                self.current_pos = next_anticlockwise
            elif (d1[b_cell] < d2[b_cell]):
                # print(b_cell, "d1 < d2")
                self.current_pos = next_clockwise
            else:
                # print(b_cell, "else")
                self.current_pos = next_anticlockwise
        else:
            self.current_pos = _next_cell

    def get_path(self):
        self.current_pos = self.start
        path = [self.start]
        i = 0
        while ((i < 4 * (self.rows + self.cols)) and
               (self.current_pos != self.goal)):
            # print(self.current_pos)
            self.next_move()
            path.append(self.current_pos)
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