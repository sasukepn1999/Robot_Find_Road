from base_find_path import Base_Find_Path


class Dac_Find_Path(Base_Find_Path):
    """docstring for Dac_Find_Path"""

    def __init__(self, map_mat, start, goal):
        super().__init__(map_mat, start, goal)
        self.current_pos = start

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
            t = self.cell_next_to_poly((x, y), polyID)
            if (t == -1):
                continue
            # opposite direction
            j = (i + 4) % 8
            if (i < j):
                if (i <= t < j):  # clockwise
                    if (self.cost[next_clockwise] / d[next_clockwise] >
                            self.cost[i] / d[i]):
                        next_clockwise = i
                else:  # anticlockwise
                    if (self.cost[next_anticlockwise] / d[next_anticlockwise] >
                            self.cost[i] / d[i]):
                        next_anticlockwise = i
            else:
                if (j <= t < i):  # anticlockwise
                    if (self.cost[next_anticlockwise] / d[next_anticlockwise] >
                            self.cost[i] / d[i]):
                        next_anticlockwise = i
                else:  # clockwise
                    if (self.cost[next_clockwise] / d[next_clockwise] >
                            self.cost[i] / d[i]):
                        next_clockwise = i
        return (self.next_cell(cell, next_clockwise),
                self.next_cell(cell, next_anticlockwise))

    def next_move(self):
        _next_cell = self.current_pos
        direct = -1
        for i in range(8):
            (x, y) = self.next_cell(self.current_pos, i)
            if not(self.is_valid_cell((x, y))):
                continue
            if (self.euclidean_dist((x, y), self.goal) + self.cost[i] <
                    self.euclidean_dist(_next_cell, self.goal) + self.cost[i]):
                _next_cell = (x, y)
                direct = i
        if (self.move_into_poly(self.current_pos, direct)):
            polyID = self.map_mat[_next_cell[0]][_next_cell[1]]
            (next_clockwise, next_anticlockwise) = \
                self.next_2_adjacent_cell(polyID)
            d = {self.current_pos: 0}
            prev_cell = self.current_pos
            (x, y) = next_clockwise
            s = 0
            i = 0
            while ((x, y) != self.current_pos):
                c = self.cost[self.get_direct(prev_cell, (x, y))]
                d[(x, y)] = d[prev_cell] + c
                s = s + c
                i = i + 1
                if i > 1000:
                    self.current_pos = next_anticlockwise
                    return
                prev_cell = (x, y)
                ((x, y), _) = self.next_2_adjacent_cell(polyID, (x, y))
            b_dist = self.rows + self.cols
            (x, y) = self.current_pos
            for cell, dist in d.items():
                if self.euclidean_dist(cell, self.goal) < b_dist:
                    b_dist = self.euclidean_dist(cell, self.goal)
                    (x, y) = cell
            if (d[(x, y)] < s - d[(x, y)]):
                self.current_pos = next_clockwise
            else:
                self.current_pos = next_anticlockwise
        else:
            self.current_pos = _next_cell

    def get_path(self):
        self.current_pos = self.start
        path = [self.start]
        i = 0
        while (i < 1000) and (self.current_pos != self.goal):
            self.next_move()
            path.append(self.current_pos)
        return path


m_find_path = Dac_Find_Path([[0, 0, 1],
                             [0, 1, 0],
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
# m_find_path.next_move()
# m_find_path.current_pos = (1, 1)
# print(m_find_path.next_2_adjacent_cell(1))
# m_find_path.current_pos = (0, 2)
# print(m_find_path.next_2_adjacent_cell(1))
# m_find_path.current_pos = (0, 3)
# print(m_find_path.next_2_adjacent_cell(1))
# m_find_path.current_pos = (0, 4)
# print(m_find_path.next_2_adjacent_cell(1))
# m_find_path.current_pos = (1, 5)
# print(m_find_path.next_2_adjacent_cell(1))
# m_find_path.current_pos = (2, 5)
# print(m_find_path.next_2_adjacent_cell(1))
# m_find_path.current_pos = (3, 5)
# print(m_find_path.next_2_adjacent_cell(1))
# m_find_path.current_pos = (4, 5)
# print(m_find_path.next_2_adjacent_cell(1))
# m_find_path.current_pos = (5, 5)
# print(m_find_path.next_2_adjacent_cell(1))
# m_find_path.current_pos = (6, 4)
# print(m_find_path.next_2_adjacent_cell(1))
# m_find_path.current_pos = (6, 3)
# print(m_find_path.next_2_adjacent_cell(1))
# m_find_path.current_pos = (6, 2)
# print(m_find_path.next_2_adjacent_cell(1))
# m_find_path.current_pos = (5, 1)
# print(m_find_path.next_2_adjacent_cell(1))
# m_find_path.current_pos = (4, 0)
# print(m_find_path.next_2_adjacent_cell(1))
# m_find_path.current_pos = (3, 0)
# print(m_find_path.next_2_adjacent_cell(1))
# m_find_path.current_pos = (2, 0)
# print(m_find_path.next_2_adjacent_cell(1))
