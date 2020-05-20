import turtle
import random
import time
import winsound

SPEED = 12
tick = 0
ticktime = 60
snakeColor = '#a8ccc9'  # cadet blue
borderColor = '#4da1a9'  # opal
foodColor = '#ffa630'  # yellow orange
bgColor = '#2e5077'  # yinmn blue
redColor = '#611c35'
textColor = '#ffa630'


def go_up():
    if head.heading() == 90 or head.heading() == 270:
        win.tracer(0)
        head.setheading(360)
        win.tracer(1)


def go_down():
    if head.heading() == 90 or head.heading() == 270:
        win.tracer(0)
        head.setheading(180)
        win.tracer(1)


def go_left():
    if head.heading() == 0 or head.heading() == 180:
        win.tracer(0)
        head.setheading(270)
        win.tracer(1)


def go_right():
    if head.heading() == 0 or head.heading() == 180:
        win.tracer(0)
        head.setheading(90)
        win.tracer(1)


def bite():
    winsound.PlaySound('bite2.wav', winsound.SND_ASYNC)


def ticker():
    global tick
    tick += 1


win = turtle.Screen()
win.setup(800, 600)
win.bgcolor(bgColor)
win.title('Snake by David McConnell')
win.mode("logo")

win.tracer(0)
byline = turtle.Turtle()
byline.color(textColor)
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
border.color(borderColor)
for side in range(4):
    border.fd(550)
    border.rt(90)
del border
win.update()

name = win.textinput('Welcome!', 'Enter your name, and press ENTER to begin!')
win.listen()
win.onkeypress(go_up, "w")
win.onkeypress(go_down, "s")
win.onkeypress(go_left, "a")
win.onkeypress(go_right, "d")

head = turtle.Turtle()
head.color(snakeColor)
head.shape('circle')
head.setheading(0)
head.pu()

food = turtle.Turtle()
food.pu()
food.color(foodColor)
food.shape('circle')
food.shapesize(.5, .5)
food.goto(0,100)

score = turtle.Turtle()
score.color(textColor)
score.pu()
score.hideturtle()
score.goto(-265, 255)
score.write('Score: 0')

segments = []

win.tracer(1)

win.ontimer(ticker, ticktime)
now = tick
gameOver = False
while not gameOver:
    win.update()
    if tick > now:
        win.tracer(0)
        score.clear()
        now = tick
        score.write('Score: ' + str(tick*len(segments)))
        if segments:
            for index in range(len(segments)-1, 0, -1):
                segments[index].goto(segments[index-1].xcor(), segments[index-1].ycor())
            segments[0].goto(head.xcor(), head.ycor())
        head.fd(SPEED)

        win.tracer(1)
        win.ontimer(ticker, ticktime)
    if abs(head.xcor()) > 275 or abs(head.ycor()) > 275:
        gameOver = True
    if segments:
        for segment in segments[3:]:
            if head.distance(segment) < 10:
                gameOver = True
    if head.distance(food) < 15:
        bite()
        win.tracer(0)
        food.goto(random.randint(-260, 260), random.randint(-260, 260))
        new_tail = turtle.Turtle()
        new_tail.color(snakeColor)
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

    if gameOver:
        def blink():
            head.color(redColor)
            win.tracer(0)
            for segment in segments:
                segment.color(redColor)
            win.tracer(1)
            time.sleep(.25)
            head.color(snakeColor)
            win.tracer(0)
            for segment in segments:
                segment.color(snakeColor)
            win.tracer(1)
            time.sleep(.25)
        blink()
        blink()
        blink()
        name2 = win.textinput('You lost!', f'Great job, {name}! If you want to change your name for recordskeeping, '
                                           'enter it now, or press ENTER to keep it the same!')
        if name2:
            name = name2
        print(name)
        turtle.bye()
