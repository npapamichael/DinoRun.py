# DinoRun.py
# Author: Nikolas Papamichael (G20970040)
# Email: NPapamichael@uclan.ac.uk
# Description: The DinoRun.py program demonstrates the Dino Runner game with additional
# features and original graphics added and modified

# all the imports
import os
import random
import sys
import time
from tkinter import *

# standard dimensions for our window
WIDTH = 800
HEIGHT = 600

win = Tk()  # as before, creates a window
win.title('DinoRun')

canvas = Canvas(win, width=WIDTH, height=HEIGHT)
canvas.config(bg='light blue')
canvas.pack()

# values that ensure the program works as intended during different stages of the script
r = random.randint(1, 4)
in_a_jump = False
jump_offsets = [0, -80, -57, -45, -35, -30, -20, -10, -5, 0, 5, 10, 20, 30, 35, 45, 57, 80, 0]
jump_index = 0
j = 0
frame_index = 0
frame4 = True
pause = False
score = 0
f_r = open('HS.txt', "r")
hs = int(f_r.readlines().pop(0))
cloud_speed = True
speed1 = 5
speed2 = 7
stage_speed = 0

# define DELAYs
DELAY = 85  # 85 ms = 0.1 sec
pause_delay = 1  # this is crucial for the pause to work
# load the background images
dino_img = [PhotoImage(file='dino%i.png' % i) for i in range(5)]
cactus_mix1_img = PhotoImage(file='cactus_mix1.png')
cactus_mix2_img = PhotoImage(file='cactus_mix2.png')
cactus_big_img = PhotoImage(file='cactus-big.png')
cactus_small_img = PhotoImage(file='cactus-small.png')
ground_img = PhotoImage(file='ground.png')
cloud_img = PhotoImage(file='cloud.png')  # a static image for decoration purposes
gameover_img = PhotoImage(file='gameover.png')

# display the background images and texts
ground_obj = canvas.create_image(WIDTH / 2, HEIGHT - ground_img.height() / 2 + 2, image=ground_img)
cloud_obj = canvas.create_image(WIDTH - cloud_img.width(), cloud_img.height() + 200, image=cloud_img)
cloud2_obj = canvas.create_image(WIDTH - (cloud_img.width() + 120), cloud_img.height() + 130, image=cloud_img)
cactus_big_obj = canvas.create_image(WIDTH + cactus_big_img.width() / 2, 473, image=cactus_big_img)
cactus_small_obj = canvas.create_image(WIDTH + cactus_small_img.width() / 2, 473, image=cactus_small_img)
cactus_mix1_obj = canvas.create_image(WIDTH + 140, 465, image=cactus_mix1_img)
cactus_mix2_obj = canvas.create_image(WIDTH + 230, 465, image=cactus_mix2_img)
dino_obj = canvas.create_image(100, 466, image=dino_img[0])
pause_obj = canvas.create_text(WIDTH / 2, HEIGHT / 2, text="PAUSE", fill='black', font=('arial narrow', 40))
canvas.itemconfig(pause_obj, state='hidden')
manual_obj = canvas.create_text(175, 560, text="Press: (Q) to Quit, (R) to Restart, (P) to Pause/Play", fill='black',
                                font=('Helvetica bold', 11))
score_obj = canvas.create_text(780, 20, text=score, fill='black', font=('bold', 11))
score_text = canvas.create_text(730, 20, text="SCORE: ", font=('bold', 11))
HS_obj = canvas.create_text(650, 20, text="HS: " + str(hs), font=('bold', 11))


# the function that applies the quit and restart feature
def press(event):
    if event.char == 'Q' or event.char == 'q':
        quit()
    if event.char == 'R' or event.char == 'r':
        time.sleep(0.2)
        os.execl(sys.executable, sys.executable, *sys.argv)  # restarts the whole script from step 1
    win.after(DELAY, press(event))


# the dino frame update to appear as moving
def frame_update():
    global frame_index, in_a_jump, jump_index, frame4, pause, pause_delay  # use global variables (defined outside the function)
    if pause:  # have a variable that makes sure if its 0 the game gets paused along with all following frames
        canvas.itemconfig(pause_obj, state='normal')
        pause_delay = 0
    else:  # else if it is unpaused it becomes a 1 and the game goes on as intended
        canvas.itemconfig(pause_obj, state='hidden')
        pause_delay = 1
    if pause_delay > 0:
        # set the next frame if unit has not collided
        if frame4 == True:
            canvas.itemconfig(dino_obj, image=dino_img[frame_index])
            # handle the 'jump' part of the animation
            if in_a_jump:  # if in a jump, move the character by jump_offset
                jump_offset = jump_offsets[jump_index]  # pick the current offset
                canvas.move(dino_obj, 0,
                            jump_offset)  # the 'canvas.move' function moves the specified object by the given X,Y pixels
                jump_index = jump_index + 1  # prepare for the next phase of the jump
                if jump_index > len(jump_offsets) - 1:  # when the jump ends...
                    jump_index = 0  # ...reset the jump_index...
                    in_a_jump = False  # ...and set in_a_jump back to False
            # update the frame picture
            frame_index += 1
            if frame_index == 3:
                frame_index = 0

    win.after(DELAY, frame_update)


# This function is called when a jump is initiated
def jump(__self__):
    global in_a_jump  # use global variable (defined outside the function)
    if not in_a_jump:  # only process the jump event if no other jump is in progress
        in_a_jump = True


# changing the value to determine if paused on unpaused
def game_pause(self):
    global pause
    pause = not pause


# the main function that checks collision, pause, score update, speed of the objects, randomizes how cacti appear
# .. and changes the difficulty and stages based on the score reached
def update():
    global r, frame_index, in_a_jump, jump_offsets, jump_index, frame4, pause, score, pause_delay, cloud_speed, stage_speed
    if pause:
        canvas.itemconfig(pause_obj, state='normal')
        pause_delay = 0
    else:
        canvas.itemconfig(pause_obj, state='hidden')
        pause_delay = 1
    if pause_delay > 0:
        # stages and difficulty change
        if score > 80:
            canvas.config(bg='blue')
            stage_speed = 5
        if score > 120:
            canvas.config(bg='dark grey')
            stage_speed = 8
        if 144 < score < 150:
            canvas.config(bg='grey')
            stage_speed = 11
        if score >= 150:
            canvas.config(bg='black')
            canvas.itemconfig(score_obj, fill='white')
            canvas.itemconfig(HS_obj, fill='white')
            canvas.itemconfig(score_text, fill='white')
            stage_speed = 15
        if score > 300:
            canvas.config(bg='dark red')
            stage_speed = 23
        score += 1 # updates the score
        (x1, y1) = canvas.coords(dino_obj)
        (x, y) = canvas.coords(cloud_obj)  # this picks the coordinates of the given object
        if x >= 0:
            if cloud_speed == True:
                canvas.move(cloud_obj, -speed1, 0)  # move the background to the left by changing the X
            if cloud_speed == False:
                canvas.move(cloud_obj, -speed2, 0)
            canvas.itemconfig(score_obj, text=score + 1)
        else:
            cloud_speed = not cloud_speed
            canvas.move(cloud_obj, WIDTH + 15, 0)  # reset the background, moving it back to the starting point
            # next handle the 'ground' part of the background - it moves at a faster pace: 15 pixels / frame
        (x, y) = canvas.coords(cloud2_obj)  # this picks the coordinates of the given object
        if x >= 0:
            if cloud_speed == True:
                canvas.move(cloud2_obj, -speed2, 0)  # move the background to the left by changing the X
            if cloud_speed == False:
                canvas.move(cloud2_obj, -speed1, 0)
        else:
            cloud_speed = not cloud_speed
            canvas.move(cloud2_obj, WIDTH + 15, 0)  # reset the background, moving it back to the starting point
        # next handle the 'ground' part of the background - it moves at a faster pace: 15 pixels / frame
        (x, y) = canvas.coords(ground_obj)
        if x >= 0:
            canvas.move(ground_obj, -40 + (-stage_speed), 0)  # move the background to the left by changing the X
        else:
            canvas.move(ground_obj, WIDTH + 40, 0)  # reset the background, moving it back to the starting point
        (x, y) = canvas.coords(cactus_small_obj)  # this picks the coordinates of the given object
        if r == 1:
            if x >= 0:
                if x - cactus_small_img.width() / 2 <= x1 + dino_img[0].width() / 2:
                    if y - cactus_small_img.height() / 2 <= y1 + dino_img[0].height() / 2:
                        if x + cactus_small_img.width() / 2 >= x1 - dino_img[0].width() / 2:
                            frame4 = False
                            canvas.itemconfig(dino_obj, image=dino_img[4])
                            canvas.create_image(400, 300, image=gameover_img)
                            highscore()
                            return 0
                canvas.move(cactus_small_obj, -35 + (-stage_speed),
                            0)  # move the background to the left by changing the X
            else:
                r = random.randint(1, 4)
                canvas.move(cactus_small_obj, WIDTH + 100,
                            0)  # reset the background, moving it back to the starting point
        (x, y) = canvas.coords(cactus_big_obj)  # this picks the coordinates of the given object
        if r == 2:
            if x >= 0:
                if x - cactus_big_img.width() / 2 <= x1 + dino_img[0].width() / 2:
                    if y - cactus_big_img.height() / 2 <= y1 + dino_img[0].height() / 2:
                        if x + cactus_big_img.width() / 2 >= x1 - dino_img[0].width() / 2:
                            frame4 = False
                            canvas.itemconfig(dino_obj, image=dino_img[4])
                            canvas.create_image(400, 300, image=gameover_img)
                            highscore()
                            return 0
                canvas.move(cactus_big_obj, -35 + (-stage_speed),
                            0)  # move the background to the left by changing the X
            else:
                r = random.randint(1, 4)
                canvas.move(cactus_big_obj, WIDTH + 100,
                            0)  # reset the background, moving it back to the starting point
        (x, y) = canvas.coords(cactus_mix1_obj)
        if r == 3:
            if x >= 0:
                if x - cactus_mix1_img.width() / 2 <= x1 + dino_img[0].width() / 2:
                    if y - cactus_mix1_img.height() / 2 <= y1 + dino_img[0].height() / 2:
                        if x + cactus_mix1_img.width() / 2 >= x1 - dino_img[0].width() / 2:
                            frame4 = False
                            canvas.itemconfig(dino_obj, image=dino_img[4])
                            canvas.create_image(400, 300, image=gameover_img)
                            highscore()
                            return 0
                canvas.move(cactus_mix1_obj, -35 + (-stage_speed),
                            0)  # move the background to the left by changing the X
            else:
                r = random.randint(1, 4)
                canvas.move(cactus_mix1_obj, WIDTH + 100,
                            0)  # reset the background, moving it back to the starting point
        (x, y) = canvas.coords(cactus_mix2_obj)
        if r == 4:
            if x >= 0:
                if x - cactus_mix2_img.width() / 2 <= x1 + dino_img[0].width() / 2:
                    if y - cactus_mix2_img.height() / 2 <= y1 + dino_img[0].height() / 2:
                        if x + cactus_mix2_img.width() / 2 >= x1 - dino_img[0].width() / 2:
                            frame4 = False
                            canvas.itemconfig(dino_obj, image=dino_img[4])
                            canvas.create_image(400, 300, image=gameover_img)
                            highscore()
                            return 0
                canvas.move(cactus_mix2_obj, -35 + (-stage_speed),
                            0)  # move the background to the left by changing the X
            else:
                r = random.randint(1, 4)
                canvas.move(cactus_mix2_obj, WIDTH + 100,
                            0)  # reset the background, moving it back to the starting point
        if in_a_jump:
            frame_index = 3
            canvas.move(dino_obj, 0, jump_offsets[jump_index])
            jump_index += 1
        else:
            jump_index = 0
            frame_index = frame_index + 1
            canvas.move(dino_obj, 0, jump_offsets[jump_index])
        if frame_index == 3:
            frame_index = 0
        if frame_index == 4:
            return 0
    win.bind("<space>", jump)
    win.after(DELAY, update)  # repeat the loop


# establishes a highscore
def highscore():
    global score, hs
    if hs < score:
        f_w = open('HS.txt', "w")
        # Put the contents of the file into a variable
        f_w.write(repr(score))
        # Close the file
        f_w.close()


win.bind("p", game_pause)
win.bind("P", game_pause)
win.bind('<KeyPress>', press)
win.after(0, frame_update)
win.after(0, update)
win.mainloop()
