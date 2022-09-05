import random
import time
import turtle
from turtle import *

screen = Screen()
screen.bgcolor("black")
screen.title("Space Invaders")
screen.setup(width=600, height=600)
screen.listen()
screen.tracer(0)
screen.bgpic("space.gif")

#Register shapes
turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")

DISTANCE = 10
INVADER_DISTANCE = 2
BULLET_SPEED = 15


# False: Bullet was fired
# True: Bullet has not been fired, so user can shoot
IS_BULLET_READY = True


# Move player functions
def move_right():
    new_x = player.xcor() + DISTANCE
    player.setx(new_x)
    if player.xcor() >= 280:
        player.setx(270)


def move_left():
    new_x = player.xcor() - DISTANCE
    player.setx(new_x)
    if player.xcor() <= -290:
        player.setx(-280)


# Move invader functions
def move_invader():
    invader_x = invader.xcor() + INVADER_DISTANCE
    invader.setx(invader_x)


def change_direction():
    global INVADER_DISTANCE
    INVADER_DISTANCE *= -1


def shift_y_cor(invader):
    invader_y = invader.ycor() - 40
    invader.sety(invader_y)


# Move bullet functions

def shoot_bullet():
    global IS_BULLET_READY
    if IS_BULLET_READY:
        IS_BULLET_READY = False
        bullet_y = player.ycor() + 10
        bullet_x = player.xcor()
        bullet.showturtle()
        bullet.goto(bullet_x, bullet_y)


#Draw game over
def game_over():
    game_over = Turtle()
    game_over.color("white")
    game_over.write("Game Over", align="center", font=('Arial', 20, 'normal'))

def update_score():
    global current_score
    current_score += 1
    score.clear()
    score.write(f"Score:{current_score}", font=("Arial", 10, "normal"))
    if current_score > highest_score:
        with open("score.txt", "w") as file:
            file.write(f"{current_score}")

#Draw score
current_score = 0
score = Turtle()
score.penup()
score.goto(x=-260, y=260)
score.color("white")
score.write(f"Score:{current_score}", font=("Arial", 10, "normal"))
score.hideturtle()

#Draw the highest score
with open("score.txt") as initial_score:
    highest_score = int(initial_score.read())
current_highest_score = Turtle()
current_highest_score.color("white")
current_highest_score.penup()
current_highest_score.hideturtle()
current_highest_score.goto(x=-190, y=260)
current_highest_score.write(f"Current highest score {highest_score}", font=("Arial", 10, "normal"))


# Draw border
border_pen = Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.goto(x=-290, y=-280)
border_pen.pensize(3)
for side in range(4):
    border_pen.pendown()
    border_pen.forward(570)
    border_pen.left(90)
border_pen.hideturtle()

# Create the player turtle
player = Turtle("player.gif")
player.speed(0)
player.color("red")
player.seth(90)
player.penup()
player.setposition(x=0, y=-260)
screen.onkeypress(move_right, "Right")
screen.onkeypress(move_left, "Left")


# Create invaders
number_of_invaders = 5
invaders_list = []
for _ in range(number_of_invaders):
    positions_x = random.randint(-100, 150)
    positions_y = random.randint(100, 280)
    invader = Turtle("invader.gif")
    invader.color("blue")
    invader.seth(270)
    invader.speed(0)
    invader.penup()
    invader.setposition(x=positions_x, y=positions_y)
    invaders_list.append(invader)

# Create player's bullet
bullet = Turtle("triangle")
bullet.color("yellow")
bullet.seth(90)
bullet.penup()
bullet.speed(0)
bullet.shapesize(0.5, 0.5)
bullet.forward(BULLET_SPEED)
bullet.setposition(x=0, y=-250)
bullet.hideturtle()
screen.onkey(shoot_bullet, "space")


# Main game loop
is_game_on = True
while is_game_on:
    screen.update()
    time.sleep(0.001)

    # Move the enemy
    for invader in invaders_list:
        move_invader()
        #  if invader gets to bottom of screen, then it will appear again in the top
        if invader.ycor() < -300:
            invader.setposition(x=random.randint(-100, 150), y=random.randint(100, 280))
        if invader.xcor() <= -290:
            #Move all invaders down
            for i in invaders_list:
                shift_y_cor(i)
            change_direction()
        if invader.xcor() >= 280:
            # Move all invaders down
            for i in invaders_list:
                shift_y_cor(i)
            change_direction()
        # Check if collision between invader and enemy
        if bullet.distance(invader) < 12:
            print("Hit")
            bullet.hideturtle()
            IS_BULLET_READY = True
            bullet.setpos(1000, 1000)
            positions_x = random.randint(-280, 280)
            positions_y = random.randint(100, 280)
            invader.setposition(x=positions_x, y=positions_y)
            update_score()
            print(highest_score)

        # Check if collision between invader and player
        if invader.distance(player) < 15:
            print("Game over")
            game_over()
            is_game_on = False

    # Move bullet
    if bullet.ycor() < 270:
        bullet_y = bullet.ycor() + BULLET_SPEED
        bullet.sety(bullet_y)
    if bullet.ycor() > 270:
        bullet.hideturtle()
        IS_BULLET_READY = True




screen.exitonclick()
