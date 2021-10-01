from tkinter import *
from tkinter import messagebox
import random
import time

# Game constants
GAME_WIDTH = 900
GAME_HEIGHT = 650
SPACE_SIZE = 50
BODYPARTS = 3
SNAKECOLOR = "#FFA500"
FOODCOLOR = "#FF0000"
BGCOLOR = "#000000"


# Snake object
class Snake:
    def __init__(self):
        self.body_size = BODYPARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODYPARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKECOLOR, tag="snake")
            self.squares.append(square)


# Food object
class Food:
    def __init__(self):
        x = random.randint(0, GAME_WIDTH/SPACE_SIZE - 1) * SPACE_SIZE
        y = random.randint(0, GAME_HEIGHT/SPACE_SIZE - 1) * SPACE_SIZE

        self.coordinates = [x,y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOODCOLOR, tag="food")


# characteristics of the next turn
def next_turn(snake, food):
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down": 
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE



    # updates coordinates of the snake's head
    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKECOLOR)
    
    # add snake head forward (shows movement)
    snake.squares.insert(0, square)

    # When snake eats food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        
        global speed
        # Increase game speed for every 2 food eaten
        if score % 2 == 0:
            speed = int(speed * 0.91)

        canvas.delete("food")
        food = Food()
    
    # remove snake tail (shows movement) when food isn't eaten
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # End the game if snake makes a collision
    if check_collisions(snake):
        gameover()
    else:
        # updates
        window.after(speed, next_turn, snake, food)

# changing direction of the snake
def change_direction(new_direction):
    global direction

    # Change direction based on arrow key pressed
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

# snake collisions
def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    
    for bodypart in snake.coordinates[1:]:
        if x == bodypart[0] and y == bodypart[1]:
            return True

    return False

# gameover characteristics
def gameover():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 70),
    text="GAME OVER", fill="red", tag="gameover")
    
# Create the window of the game
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

# Create score, direction and speed
speed = 75
score = 0
direction = 'down'
label = Label(window, text="Score: {}".format(score), font=('consolas', 40))
label.pack()

# Set Gameboard parameters to a canvas
canvas = Canvas(window, bg=BGCOLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Center the game window upon initialization
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Create snake and food objects
snake = Snake()
food = Food()

# Goes to next turn
next_turn(snake, food)

window.mainloop()