import os
import permutation as pm
import GUI_V2 as gv2

hx = [1, 0, -1, 0, 1, -1, -1, 1]
hy = [0, 1, 0, -1, 1, 1, -1, -1]
hv = [2, 2, 2, 2, 3, 3, 3, 3]
# top, right, bot, left


def readData(fileName):
    res = list()
    if not(os.path.exists(fileName)):
        print("File khong ton tai! ")
        exit(0)
    inpfile = open(fileName, "r")
    res.append(list(inpfile.readline().replace('\n', '').split(',')))
    res.append(list(inpfile.readline().replace('\n', '').split(',')))

    numPoly = int(inpfile.readline())

    poly = list()
    for i in range(numPoly):
        inp = list(inpfile.readline().replace('\n', '').split(','))
        for j in range(len(inp)):
            inp[j] = int(inp[j])
        inp += list([inp[0], inp[1]])
        poly.append(inp)

    res.append(poly)

    inpfile.close()

    return res


def init(m, n, numPoly, poly):
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

    for i in range(numPoly):
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
    return mat


def findPath(mat, m, n, start, goal):
    f = list()
    for i in range(m + 1):
        col = list()
        for j in range(n + 1):
            col.append(-1)
        f.append(col)

    closed = list()
    for i in range(m + 1):
        col = list()
        for j in range(n + 1):
            col.append(0)
        closed.append(col)

    trace = list()
    for i in range(m + 1):
        col = list()
        for j in range(n + 1):
            col.append((0, 0))
        trace.append(col)

    g = list()
    g.append((start[0], start[1]))
    f[start[0]][start[1]] = 0
    trace[start[0]][start[1]] = (-1, -1)

    while len(g) > 0:
        x = g[0][0]
        y = g[0][1]
        for i in range(len(g)):
            if f[x][y] > f[g[i][0]][g[i][1]] and f[g[i][0]][g[i][1]] != -1:
                x = g[i][0]
                y = g[i][1]
        closed[x][y] = 1
        g.remove((x, y))
        if x == goal[0] and y == goal[1]:
            break

        cM = list()     # canMove
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
                trace[u][v] = (x, y)
                if g.count((u, v)) == 0:
                    g.append((u, v))

    res = list()

    if f[goal[0]][goal[1]] != -1:
        x = goal[0]
        y = goal[1]

        while x != -1 and y != -1:
            res.append(list([x, y]))
            tra = trace[x][y]
            x = tra[0]
            y = tra[1]

    res.reverse()

    return f[goal[0]][goal[1]], res

def find_path(matrix, m, n, ver, poly):
    numVer = len(ver) // 2
    for i in range(numVer * 2):
        ver[i] = int(ver[i])

    numPoly = len(poly)

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
            val, move = findPath(matrix, m, n, start, goal)
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
        val, move = findPath(matrix, m, n, start, goal)
        if len(path):
            del path[len(path) - 1]
        path = path + move

    p = [res]
    p.append(path)

    return p


def process():
    fileName = input("Nhap ten file: ")

    inp = readData(fileName)

    n = int(inp[0][0])  # column
    m = int(inp[0][1])  # row

    ver = inp[1]

    poly = inp[2]

    matrix = init(m, n, len(poly), poly)

    path = find_path(matrix, m, n, ver, poly)

    matrix[ver[1]][ver[0]] = 'S'
    matrix[ver[3]][ver[2]] = 'G'
    for i in range(2, len(ver) // 2):
        matrix[ver[i * 2 + 1]][ver[i * 2]] = 'P'

    return matrix, path



# main
if __name__ == '__main__':
    matrix, path = process()
    surface = gv2.init(matrix)
    gv2.loop(surface, matrix, path)
