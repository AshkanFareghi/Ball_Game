# This is Ash.
import pygame as pg
from pygame import mixer
import tkinter as tk
from time import sleep
from sys import exit


#Game over Screen
def show_game_over(score):
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Game over!")

    this_score = score

    try:
        with open("High_score.txt", "r") as f:
            high_score = int(f.read())
            if this_score > high_score:
                high_score = this_score
                with open("High_score.txt", "w") as f:
                    f.write(str(high_score))
    except FileNotFoundError:
        with open("High_score.txt", "w") as f:
            f.write(str(this_score))
        high_score = this_score

    #Labels
    Label = tk.Label(root, text="Game Over!\n")
    Label.config(font=("Arial", 42))
    Label.pack()

    Label = tk.Label(root, text="Score: " + str(this_score) + "\nHigh score: " + str(high_score) + "\n")
    Label.config(font=("Arial", 32))
    Label.pack()
    Button = tk.Button(root, text="Confirm", command = exit)
    Button.config(font=("Arial", 24))
    Button.pack()

    root.mainloop()

#Initialize pygame
pg.init()

#Images
Icon = pg.image.load('ufo.png')
Player = pg.image.load('player.png')
Ball = pg.image.load('ball.png')


# Creating the game window
window = pg.display.set_mode((800, 600))

# Background Music
mixer.music.load('music.mp3')
mixer.music.play(-1)

#Window title and Icon
pg.display.set_caption('Save the ball')
pg.display.set_icon(Icon)

# Initialize variables
player_change = 0
x = 400 - 64
y = 500 - 64
x_ball = 400
y_ball = 300
x_change_ball = -3
y_change_ball = -3
state = "mirror"
score = 0

# Main loop
while True:
    for event in pg.event.get():
        # Handle quit events
        if event.type == pg.QUIT:
            exit()

        # Handle key events
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                exit()
            elif event.key == pg.K_LEFT:
                player_change -= 5
            elif event.key == pg.K_RIGHT:
                player_change += 5
        elif event.type == pg.KEYUP:
            player_change = 0

    # Update game elements and screen
    window.fill((255, 255, 255))
    x_ball += x_change_ball
    y_ball += y_change_ball
    x += player_change

    if int(x_ball) >= 800 - 64 or int(x_ball) <= 0:
        x_change_ball = -1 * x_change_ball
    elif int(y_ball) <= 0:
        y_change_ball = -1 * y_change_ball
    elif int(y_ball) >= 600 - 64:
        show_game_over(score)

    if x <= 0:
        x = 0
    elif x >= 800 - 128:
        x = 800 - 128

    statement1 = y_ball + 64 >= y + 64
    statement2 = x_ball + 64 > x and x_ball + 64 < x + 128

    if state == "mirror":
        if statement1:
            if statement2:
                y_change_ball = -1 * y_change_ball
                state = "mirror off"
                score += 1
    else:
        if not statement1 and not statement2:
            state = "mirror"
    
    window.blit(Ball, (x_ball, y_ball))
    window.blit(Player, (x, y))
    pg.display.update()

    sleep(0.008)