import turtle

CELL_WIDTH = 200
TURN = True
TURTLE_IS_MOVING = False
OCCUPIED_CELLS = dict()
WINNER = None

turtle.speed(0)
turtle.width(10)

def draw_line(start_x, start_y, length):
    turtle.penup()
    turtle.goto(start_x, start_y)
    turtle.pendown()
    turtle.forward(length)

def draw_board():
    draw_line(-1.5 * CELL_WIDTH, 0.5 * CELL_WIDTH, 3 * CELL_WIDTH)
    draw_line(-1.5 * CELL_WIDTH, -0.5 * CELL_WIDTH, 3 * CELL_WIDTH)
    turtle.right(90)
    draw_line(-0.5 * CELL_WIDTH, 1.5 * CELL_WIDTH, 3 * CELL_WIDTH)
    draw_line(0.5 * CELL_WIDTH, 1.5 * CELL_WIDTH, 3 * CELL_WIDTH)
    turtle.left(90)

def draw_cross(x, y):
    turtle.color("red")
    cw = 0.8 * CELL_WIDTH
    turtle.right(45)
    draw_line(x - cw/2, y + cw/2, 1.41 * cw)
    turtle.right(90)
    draw_line(x + cw/2, y + cw/2, 1.41 * cw)
    turtle.left(135)
    

def draw_circle(x, y):
    turtle.color("blue")
    diameter = 0.8 * CELL_WIDTH
    turtle.penup()
    turtle.goto(x, y - diameter/2)
    turtle.pendown()
    turtle.circle(diameter/2)
    

def is_outside(x, y):
    if x > 1.5 * CELL_WIDTH:
        return True
    if y > 1.5 * CELL_WIDTH:
        return True
    if x < -1.5 * CELL_WIDTH:
        return True
    if y < -1.5 * CELL_WIDTH:
        return True

def detect_horizontal(x, y):
    if y > CELL_WIDTH * 0.5:
        return 1
    if y < -CELL_WIDTH * 0.5:
        return -1
    return 0

def detect_vertical(x, y):
    if x > CELL_WIDTH * 0.5:
        return 1
    if x < -CELL_WIDTH * 0.5:
        return -1
    return 0

def reset_game():
    global OCCUPIED_CELLS
    global TURN
    global WINNER
    turtle.clear()
    turtle.setheading(0)
    turtle.color("black")
    draw_board()
    OCCUPIED_CELLS = dict()
    WINNER = None
    TURN = True

def detect_winner():
    for row in (-1, 0, 1):
        values = []
        for key, value in OCCUPIED_CELLS.items():
            if key[0] == row:
                values.append(value)
        if len(values) == 3 and values[0] == values[1] == values[2]:
            turtle.color("green")
            draw_line(-1.7 * CELL_WIDTH, row * CELL_WIDTH, 3.4 * CELL_WIDTH)
            return values[0]
    
    for col in (-1, 0, 1):
        values = []
        for key, value in OCCUPIED_CELLS.items():
            if key[1] == col:
                values.append(value)
        if len(values) == 3 and values[0] == values[1] == values[2]:
            turtle.color("green")
            turtle.right(90)
            draw_line(col * CELL_WIDTH, 1.7 * CELL_WIDTH, 3.5 * CELL_WIDTH)
            return values[0]
        
    left_diag = [(1, -1), (0, 0), (-1, 1)]
    right_diag = [(1, 1), (0, 0), (-1, -1)]

    left_values = []
    right_values = []
    
    for key, value in OCCUPIED_CELLS.items():
        if key in left_diag:
            left_values.append(value)
        if key in right_diag:
            right_values.append(value)
    
    if len(left_values) == 3 and left_values[0] == left_values[1] == left_values[2]:
        turtle.right(45)
        turtle.color("green")
        draw_line(-1.6 * CELL_WIDTH, 1.6 * CELL_WIDTH, 4.35 * CELL_WIDTH)
        return left_values[0]
    
    if len(right_values) == 3 and right_values[0] == right_values[1] == right_values[2]:
        turtle.right(135)
        turtle.color("green")
        draw_line(1.6 * CELL_WIDTH, 1.6 * CELL_WIDTH, 4.35 * CELL_WIDTH)
        return right_values[0]


def respond_to_click(x, y):
    global TURN
    global TURTLE_IS_MOVING
    global WINNER
    
    if WINNER is not None:
        reset_game()
        return
    
    if TURTLE_IS_MOVING == True:
        return
    
    if is_outside(x, y):
        return
    
    horizontal_index = detect_horizontal(x, y)
    vertical_index = detect_vertical(x, y)
    
    if (horizontal_index, vertical_index) in OCCUPIED_CELLS:
        return
    
    OCCUPIED_CELLS[(horizontal_index, vertical_index)] = TURN
    
    x = CELL_WIDTH * vertical_index
    y = CELL_WIDTH * horizontal_index
    
    TURTLE_IS_MOVING = True
    if TURN == True:
        draw_cross(x, y)
        TURN = False
    else:
        draw_circle(x, y)
        TURN = True
    TURTLE_IS_MOVING = False
    
    WINNER = detect_winner()


reset_game()
turtle.onscreenclick(respond_to_click)
turtle.done()