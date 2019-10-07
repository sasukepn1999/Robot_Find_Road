import os

hx = [1, 0, -1, 0, 1, -1, -1, 1]
hy = [0, 1, 0, -1, 1, 1, -1, -1]
hv = [2, 2, 2, 2, 3, 3, 3, 3]
# top, right, bot, left

fileName = input("Nhap ten file: ")
if os.path.exists(fileName) == False:
    print("File khong ton tai! ")
    exit(0)
inpfile = open(fileName, "r")
inp = list(inpfile.readline().replace('\n', '').split(','))
n = int(inp[0])     #column
m = int(inp[1])     #row

inp = list(inpfile.readline().replace('\n', '').split(','))
start = list([int(inp[1]), int(inp[0])]);
goal = list([int(inp[3]), int(inp[2])]);
numVer = 0
if len(inp) == 5:
    numVer = int(inp[4])

numPoly = int(inpfile.readline())
poly = list()
for i in range(numPoly):
    inp = list(inpfile.readline().replace('\n', '').split(','))
    for j in range(len(inp)):
        inp[j] = int(inp[j])
    inp += list([inp[0], inp[1]])
    poly.append(inp)

ver = list()
if numVer != 0:
    for i in range(numVer):
        inp = list(inpfile.readline().replace('\n', '').split(','))
        for j in range(len(inp)):
            inp[i] = int(inp[i])
        ver.append(inp)

inpfile.close()

mat = list()
for i in range(m + 1):
    col = list()
    for i in range(n + 1):
        col.append(0)
    mat.append(col)

for i in range(m + 1):
    for j in range(n + 1):
        if i == start[0] and j == start[1]:
            mat[i][j] = 'S'
        if i == goal[0] and j == goal[1]:
            mat[i][j] = 'G'
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
            mat[x1][y1] = i + 1
            if d == 1:
                tx = cx
                if crx > 0:
                    tx += 1
                    crx -= 1
                while tx > 0:
                    x1 += xx
                    tx -= 1
                    mat[x1][y1] = i + 1
            else:
                ty = cy
                if cry > 0:
                    ty += 1
                    cry -= 1
                while ty > 0:
                    y1 += yy
                    ty -= 1
                    mat[x1][y1] = i + 1

            if x1 == x2 and y1 == y2:
                break
            else:
                x1 += xx
                y1 += yy


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

    cM = list()     #canMove
    for i in range(4):
        u = x + hx[i]
        v = y + hy[i]
        if (mat[u][v] == 0 or mat[u][v] == 'G') and closed[u][v] == 0:
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
        if (mat[u][v] != 0 and mat[u][v] != 'G')  or closed[u][v] == 1:
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

if f[goal[0]][goal[1]] == -1:
    print("Khong ton tai duong di")
else:
    print(f[goal[0]][goal[1]] / 2)

    tra = trace[goal[0]][goal[1]]
    x = tra[0]
    y = tra[1]

    while x != start[0] or y != start[1]:
        mat[x][y] = '+'
        tra = trace[x][y]
        x = tra[0]
        y = tra[1]

for i in range(m, -1, -1):
    for j in range(n + 1):
        print(mat[i][j], end=" ")
    print()