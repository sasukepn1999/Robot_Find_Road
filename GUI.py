import turtle as tt

LENGTH = 30 # each grid element will be LENGTH x LENGTH pixels
Color = ["white", "gray", "red", "orange", "yellow", "violet"]
matrix = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'G', 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, '+', 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, '+', 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, '+', 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, '+', 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '+', 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, '+', 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, '+', 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, '+', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 1, 0, 0, 0, 1, '+', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 0, 0, 0, 0, 1, '+', 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 0, 0, 1, 1, 1, '+', 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 1, 1, 1, 0, 0, '+', 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, '+', 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 'S', '+', '+', '+', '+', '+', 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3 ,0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

matrix_input = matrix
way = []
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        if (matrix_input[i][j] == "+"):
            matrix_input[i][j] = 0
            way.append([len(matrix) - i - 1, j])

# Draw the map
def grid(turtle, m, n, length = LENGTH): # matrix m x n
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

    [turtle.right, turtle.left][n%2](90)
    turtle.penup()
    turtle.goto(-n * length / 2, -m * length / 2)

# Fill color for shapes
def fillColorOneElementOnGrid(turtle, x, y, color, length, text = ""):
    x0, y0 = turtle.pos() # Coordinate O(0, 0)

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
    if (text != ""): writeTexttOnGrid(turtle, x, y, length, text)
    turtle.color("black")

# Draw the way
def fillDotOnGrid(turtle, x, y, length):
    x0, y0 = turtle.pos() # Coordinate O(0, 0)

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
    x0, y0 = turtle.pos() # Coordinate O(0, 0)

    turtle.penup()
    turtle.goto(x0 + x * length + length / 2.5, y0 + y * length + length / 4)
    turtle.pendown()

    turtle.write(text, font = ("Arial", 10, "bold"))

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
            if (matrix[i][j] == 0):
                continue
            elif (matrix[i][j] == "G" or matrix[i][j] == "S"):
                fillColorOneElementOnGrid(turtle, j, m - i - 1, "blue", length, matrix[i][j])
            elif(matrix[i][j] == "+"):
                fillDotOnGrid(turtle, j, m - i - 1, length)
            else:
                fillColorOneElementOnGrid(turtle, j, m - i - 1, Color[matrix[i][j] % len(Color)], length)

# Load way by matrix (matrix contains coordinates of way)
def findWay(turtle, way, length):
    for i in range(len(way)):
        fillDotOnGrid(turtle, way[i][1], way[i][0], length)


# ----------------------------------------------------------MAIN----------------------------------------------------------
screen = tt.Screen()

Long = tt.Turtle()
Long.hideturtle()
grid(Long, 19, 23)
fillColorOneElementOnGridByMatrix(Long, matrix_input, LENGTH)
findWay(Long, way, LENGTH)

screen.exitonclick()
# --------------------------------------------------------EXIT MAIN--------------------------------------------------------