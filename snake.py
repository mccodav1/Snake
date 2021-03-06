import turtle
import random
import time
import winsound
import sqlite3
from datetime import date

SPEED = 12
TICK_TIME = 60
SNAKE_COLOR = '#a8ccc9'
BORDER_COLOR = '#4da1a9'
FOOD_COLOR = '#ffa630'
BACKGROUND_COLOR = '#2e5077'
RED_COLOR = '#611c35'
TEXT_COLOR = '#ffa630'


def go_up():
    """
    Turns snake north
    :return:
    """
    if head.heading() == 90 or head.heading() == 270:
        win.tracer(0)
        head.setheading(360)
        win.tracer(1)


def go_down():
    """
    Turns snake south
    :return:
    """
    if head.heading() == 90 or head.heading() == 270:
        win.tracer(0)
        head.setheading(180)
        win.tracer(1)


def go_left():
    """
    Turns snake west
    :return:
    """
    if head.heading() == 0 or head.heading() == 180:
        win.tracer(0)
        head.setheading(270)
        win.tracer(1)


def go_right():
    """
    Turns snake east
    :return:
    """
    if head.heading() == 0 or head.heading() == 180:
        win.tracer(0)
        head.setheading(90)
        win.tracer(1)


def bite():
    """
    Move food, play sound, add tail segment
    :return:
    """
    winsound.PlaySound('bite2.wav', winsound.SND_ASYNC)
    win.tracer(0)
    food.goto(random.randint(-260, 260), random.randint(-260, 260))
    new_tail = turtle.Turtle()
    new_tail.color(SNAKE_COLOR)
    new_tail.shape('circle')
    new_tail.speed(0)
    new_tail.pu()
    if segments:
        segments[-1].shape('square')
        new_tail.goto(segments[-1].xcor(), segments[-1].ycor())
    else:
        new_tail.goto(head.xcor(), head.ycor())
    segments.append(new_tail)
    win.tracer(1)


def increaseTick():
    global tick
    tick += 1


def writeScore(turt, scoreList):
    """
    Use specified turtle to write a list of high scores.
    :param turt: Turtle writer
    :param scoreList: List of scores in format [name, score, date]
    :return: None
    """
    turt.goto(-385, 255)
    turt.write('RECORD HOLDERS')
    turt.goto(282, 255)
    turt.write('SCORE\tDATE')
    turt.goto(-355, 255)
    x, y = turt.xcor(), turt.ycor()
    for record in range(25):
        turt.goto(x, y - 20)
        if record < len(scoreList):
            turt.write(scoreList[record][0])
        else:
            turt.write('-----')
        turt.goto(x+637, y - 20)
        if record < len(scoreList):
            turt.write(str(scoreList[record][1]) + '\t' + str(scoreList[record][2]))
        else:
            turt.write('-----\t-----')
        y = y-20


win = turtle.Screen()
win.setup(800, 600)
win.bgcolor(BACKGROUND_COLOR)
win.title('Snake by David McConnell')
win.mode("logo")
win.tracer(0)

byline = turtle.Turtle()
byline.color(TEXT_COLOR)
byline.pu()
byline.hideturtle()
byline.goto(-275, 280)
byline.write("Snake Game by David McConnell")
byline.goto(-60, 280)
byline.write("Originally created 19 May 2020")
byline.goto(140, 280)
byline.write(r"https://github.com/mccodav1")
del byline

border = turtle.Turtle()
border.pu()
border.hideturtle()
border.goto(-275, -275)
border.pd()
border.pensize(5)
border.color(BORDER_COLOR)
for side in range(4):
    border.fd(550)
    border.rt(90)
del border

connection = sqlite3.connect("scores.db")
cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS scores (name TEXT, score INTEGER, date DATE)')
connection.commit()

cursor.execute('SELECT * FROM scores ORDER BY score DESC')
scores = [[x[0], x[1], x[2]] for x in cursor.fetchall()]

scoreWriter = turtle.Turtle()
scoreWriter.color(TEXT_COLOR)
scoreWriter.pu()
scoreWriter.hideturtle()
writeScore(scoreWriter, scores)
win.update()

gameOver = False
name = win.textinput('Welcome!', 'Enter your name, and press ENTER to begin!')
while not name:
    if name is None:
        gameOver = True
        break
    name = win.textinput('Invalid Entry!', 'Your name cannot be blank! Enter your name, and press ENTER to begin!')

win.listen()
win.onkeypress(go_up, "w")
win.onkeypress(go_down, "s")
win.onkeypress(go_left, "a")
win.onkeypress(go_right, "d")

head = turtle.Turtle()
head.pu()
head.color(SNAKE_COLOR)
head.shape('circle')
head.setheading(0)


food = turtle.Turtle()
food.pu()
food.color(FOOD_COLOR)
food.shape('circle')
food.shapesize(.5, .5)
food.goto(0, 100)

score = turtle.Turtle()
score.pu()
score.color(TEXT_COLOR)
score.hideturtle()
score.goto(-265, 255)
score.write('Score: 0')

segments = []

win.tracer(1)

tick = 0
win.ontimer(increaseTick, TICK_TIME)
now = tick
askGameOver = False

while not askGameOver and not gameOver:
    win.update()
    currentScore = tick * len(segments)
    if tick > now:
        win.tracer(0)
        score.clear()
        now = tick
        score.write('Score: ' + str(currentScore))
        if segments:
            for index in range(len(segments)-1, 0, -1):
                segments[index].goto(segments[index-1].xcor(), segments[index-1].ycor())
            segments[0].goto(head.xcor(), head.ycor())
        head.fd(SPEED)

        win.tracer(1)
        win.ontimer(increaseTick, TICK_TIME)
    if abs(head.xcor()) > 275 or abs(head.ycor()) > 275:
        askGameOver = True
    if segments:
        for segment in segments[3:]:
            if head.distance(segment) < 10:
                askGameOver = True
    if head.distance(food) < 15:
        bite()

    if askGameOver and not gameOver:
        def blink():
            head.color(RED_COLOR)
            win.tracer(0)
            for piece in segments:
                piece.color(RED_COLOR)
            win.tracer(1)
            time.sleep(.25)
            head.color(SNAKE_COLOR)
            win.tracer(0)
            for piece in segments:
                piece.color(SNAKE_COLOR)
            win.tracer(1)
            time.sleep(.25)
        blink()
        blink()
        blink()
        try:
            cursor.execute('INSERT INTO scores (name, score, date) VALUES (?, ?, ?)', (name, currentScore, date.today()))
            connection.commit()
        except Exception as e:
            print(f'Error occurred: {e}')
        playAgain = win.textinput('You died!', f'Great job, {name}! '
                                               f'If you want to play again, enter Y! Any other input exits the game.')
        if playAgain.lower() == 'y':
            askGameOver = False
            score.write('Score: 0')
            tick = 0
            win.ontimer(increaseTick, TICK_TIME)
            now = tick
            head.hideturtle()
            del head
            head = turtle.Turtle()
            head.pu()
            head.color(SNAKE_COLOR)
            head.shape('circle')
            head.setheading(0)
            for item in segments:
                item.clear()
                item.hideturtle()
            segments.clear()
            del segments[:]
            segments = []
            win.listen()
        else:
            gameOver = True
    if gameOver:
        turtle.bye()
