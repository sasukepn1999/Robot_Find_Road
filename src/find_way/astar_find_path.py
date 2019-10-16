import os
import permutation as pm
from find_way.base_find_path import Base_Find_Path
import GUI_V2 as gv2

class AStar_Find_Path(Base_Find_Path):
    def __init__(self, file_name):
        super().__init__(file_name)

    def h(self, start, goal):
        length = max(abs(start[0] - goal[0]), abs(start[1] - goal[1]))
        width = min(abs(start[0] - goal[0]), abs(start[1] - goal[1]))

        manhattan = (length + width) * 2

        euclid = (length - width) * 2 + width * 3

        return (manhattan + euclid) / 2

    def find_path(self, start, goal):
        mat = self.map_mat
        m = len(mat)
        n = len(mat[0])

        f = []
        for i in range(m):
            col = []
            for j in range(n):
                col.append(-1)
            f.append(col)

        t = []
        for i in range(m):
            col = []
            for j in range(n):
                col.append(-1)
            t.append(col)

        closed = []
        for i in range(m):
            col = []
            for j in range(n):
                col.append(0)
            closed.append(col)

        trace = []
        for i in range(m):
            col = []
            for j in range(n):
                col.append((0, 0))
            trace.append(col)

        g = []
        g.append((start[0], start[1]))
        f[start[0]][start[1]] = 0
        trace[start[0]][start[1]] = (-1, -1)

        while len(g) > 0:
            x = g[0][0]
            y = g[0][1]
            for i in range(len(g)):
                if t[x][y] > t[g[i][0]][g[i][1]]:
                    x = g[i][0]
                    y = g[i][1]
            closed[x][y] = 1
            g.remove((x, y))
            if x == goal[0] and y == goal[1]:
                break

            hx = [1, 0, -1, 0, 1, -1, -1, 1]
            hy = [0, 1, 0, -1, 1, 1, -1, -1]
            hv = [2, 2, 2, 2, 3, 3, 3, 3]
            # top, right, bot, left

            cM = []         # canMove
            for i in range(4):
                u = x + hx[i]
                v = y + hy[i]
                if mat[u][v] == 0 and closed[u][v] == 0:
                    cM.append(1)
                else:
                    cM.append(0)

            cM.append(cM[0] | cM[1])
            cM.append(cM[1] | cM[2])
            cM.append(cM[2] | cM[3])
            cM.append(cM[3] | cM[0])

            for i in range(4, 8):
                u = x + hx[i]
                v = y + hy[i]
                if mat[u][v] != 0 or closed[u][v] == 1:
                    cM[i] = 0

            for i in range(8):
                if cM[i] == 1:
                    u = x + hx[i]
                    v = y + hy[i]
                    if f[u][v] != -1 and f[u][v] <= f[x][y] + hv[i]:
                        continue
                    f[u][v] = f[x][y] + hv[i]
                    t[u][v] = f[u][v] + self.h((u, v), goal)
                    trace[u][v] = (x, y)
                    if g.count((u, v)) == 0:
                        g.append((u, v))

        res = []

        if f[goal[0]][goal[1]] != -1:
            x = goal[0]
            y = goal[1]

            while x != -1 and y != -1:
                res.append([x, y])
                tra = trace[x][y]
                x = tra[0]
                y = tra[1]

        res.reverse()

        return f[goal[0]][goal[1]], res

    def get_path(self):
        matrix = self.map_mat
        ver = self.ver

        numVer = len(ver) // 2
        for i in range(numVer * 2):
            ver[i] = int(ver[i])

        f = list()
        for i in range(numVer):
            col = list()
            for j in range(numVer):
                col.append(0)
            f.append(col)

        for i in range(numVer):
            for j in range(i + 1, numVer):
                start = [ver[i * 2 + 1], ver[i * 2]]
                goal = [ver[j * 2 + 1], ver[j * 2]]
                val, move = self.find_path(start, goal)
                f[i][j] = f[j][i] = val

        hv = list(range(2, numVer))
        res = 100000

        while 1:
            p = [0] + hv + [1]
            tmp = 0
            for i in range(len(p) - 1):
                val = f[p[i]][p[i + 1]]
                if val < 0:
                    res = -1
                    ttMove = []
                    break
                else:
                    tmp += val

            if res == -1:
                break
            if res > tmp:
                res = tmp
                ttMove = p

            if not pm.next_permutation(hv):
                break
        if res > 0:
            if res % 2 == 0:
                res //= 2
            else:
                res /= 2

        path = []
        for i in range(len(ttMove) - 1):
            start = [ver[ttMove[i] * 2 + 1], ver[ttMove[i] * 2]]
            goal = [ver[ttMove[i + 1] * 2 + 1], ver[ttMove[i + 1] * 2]]
            val, move = self.find_path(start, goal)
            if len(path):
                del path[len(path) - 1]
            path = path + move

        return (res, path)

# main
if __name__ == '__main__':
    file_name = input("File name: ")
    if not (os.path.exists(file_name)):
        print("File does not exist! ")
        exit(0)
    m_find_path = AStar_Find_Path(file_name)
    path = m_find_path.get_path()
    m_find_path.update_map_mat()
    matrix = m_find_path.map_mat
    surface = gv2.init(matrix)
    gv2.loop(surface, matrix, path)