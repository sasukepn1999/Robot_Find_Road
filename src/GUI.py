import turtle as tt
import doan


LENGTH = 30  # each grid element will be LENGTH x LENGTH pixels
Color = ["white", "gray", "red", "orange", "yellow", "violet"]
# matrix = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'G', 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, '+', 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, '+', 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, '+', 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, '+', 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '+', 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, '+', 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, '+', 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, '+', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, '+', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, '+', 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 1, 0, 0, 1, 1, 1, '+', 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 1, 1, 1, 0, 0, '+', 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, '+', 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 'S', '+', '+', '+', '+', '+', 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3 ,0, 0, 0, 0, 0, 0, 0, 1],
# [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


# Draw the map
def grid(turtle, m, n, length=LENGTH):  # matrix m x n
    turtle.speed(0)
    turtle.penup()
    turtle.goto(-n * length / 2, m * length / 2)
    turtle.pendown()

    sign = -1
    for _ in range(m):
        turtle.forward(n * length)
        turtle.left(sign * 90)
        turtle.forward(length)
        turtle.left(sign * 90)
        sign = 0 - sign
    turtle.forward(n * length)
    turtle.left(-sign * 90)

    for _ in range(n):
        turtle.forward(m * length)
        turtle.left(-sign * 90)
        turtle.forward(length)
        turtle.left(-sign * 90)
        sign = 0 - sign
    turtle.forward(m * length)

    [turtle.right, turtle.left][n % 2](90)
    turtle.penup()
    turtle.goto(-n * length / 2, -m * length / 2)


# Fill color for shapes
def fillColorOneElementOnGrid(turtle, x, y, color, length, text=""):
    x0, y0 = turtle.pos()  # Coordinate O(0, 0)

    turtle.penup()
    turtle.goto(x0 + x * length, y0 + y * length)
    turtle.pendown()
    # Fill color each element on grid
    turtle.begin_fill()
    turtle.fillcolor(color)
    for _ in range(4):
        turtle.forward(length)
        turtle.left(90)
    turtle.end_fill()
    turtle.fillcolor("black")

    # Move turtle to O(0, 0)
    turtle.penup()
    turtle.goto(x0, y0)
    turtle.pendown()

    turtle.color("white")
    if (text != ""):
        writeTexttOnGrid(turtle, x, y, length, text)
    turtle.color("black")


# Draw the way
def fillDotOnGrid(turtle, x, y, length):
    x0, y0 = turtle.pos()  # Coordinate O(0, 0)

    turtle.penup()
    turtle.goto(x0 + x * length + length / 2, y0 + y * length + length / 2)
    turtle.pendown()

    turtle.dot()

    # Move turtle to O(0, 0)
    turtle.penup()
    turtle.goto(x0, y0)
    turtle.pendown()


# Write text on grid
def writeTexttOnGrid(turtle, x, y, length, text):
    x0, y0 = turtle.pos()  # Coordinate O(0, 0)

    turtle.penup()
    turtle.goto(x0 + x * length + length / 2.5, y0 + y * length + length / 4)
    turtle.pendown()

    turtle.write(text, font=("Arial", 10, "bold"))

    # Move turtle to O(0, 0)
    turtle.penup()
    turtle.goto(x0, y0)
    turtle.pendown()


# Load map by matrix
def fillColorOneElementOnGridByMatrix(turtle, matrix, length):
    # Get height and width of matrix m x n
    m = len(matrix)
    n = len(matrix[0])

    for i in range(m):
        for j in range(n):
            if (matrix[i][j] == -1):
                fillColorOneElementOnGrid(turtle,
                                          j,
                                          i,
                                          "white",
                                          length,
                                          matrix[i][j])
            elif (matrix[i][j] == 0):
                continue
            elif (matrix[i][j] == "G" or matrix[i][j] == "S"):
                fillColorOneElementOnGrid(turtle,
                                          j,
                                          i,
                                          "blue",
                                          length,
                                          matrix[i][j])
            elif (matrix[i][j] == "P"):
                fillColorOneElementOnGrid(turtle,
                                          j,
                                          i,
                                          "wheat",
                                          length,
                                          matrix[i][j])
            elif(matrix[i][j] == "+"):
                fillDotOnGrid(turtle, j, i, length)
            else:
                fillColorOneElementOnGrid(turtle,
                                          j,
                                          i,
                                          Color[matrix[i][j] % len(Color)],
                                          length)


# Load way by matrix (matrix contains coordinates of way)
def findWay(turtle, way, matrix, length):
    for i in range(1, len(way) - 1):
        if (matrix[way[i][0]][way[i][1]] == 0):
            fillDotOnGrid(turtle, way[i][1], way[i][0], length)


def process(turtle):
    fileName = input("Nhap ten file: ")

    inp = doan.readData(fileName)

    n = int(inp[0][0])  # column
    m = int(inp[0][1])  # row
    start = list([int(inp[1][1]), int(inp[1][0])])
    goal = list([int(inp[1][3]), int(inp[1][2])])
    numPoly = inp[2][0]
    # numVer = inp[2][1]
    poly = inp[3]
    # ver = inp[4]

    matrix = doan.init(m, n, start, goal, numPoly, poly)
    path = doan.findPath(matrix, m, n, start, goal)

    # return matrix, path
    grid(turtle, len(matrix), len(matrix[0]))
    fillColorOneElementOnGridByMatrix(turtle, matrix, LENGTH)
    findWay(turtle, path, LENGTH)


# ----------------------------------------------------------MAIN----------------------------------------------------------
if __name__ == '__main__':
    screen = tt.Screen()

    Long = tt.Turtle()
    Long.hideturtle()
    process(Long)

    screen.exitonclick()
# --------------------------------------------------------EXIT MAIN--------------------------------------------------------