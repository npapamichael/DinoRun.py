import random
from tkinter import *

# standard dimensions for our window
WIDTH = 800
HEIGHT = 600

win = Tk()  # as before, creates a window
win.title('Moving background in loops')

canvas = Canvas(win, width=WIDTH, height=HEIGHT)
canvas.config(bg='dark gray')
canvas.pack()
r = random.randint(1, 4)
in_a_jump = False
jump_offsets = [0, -60, -45, -30, -20, 0, 20, 30, 45, 50, 25, -15, 0]
jump_index = 0
j = 0
frame_index = 0

# define constants
DELAY = 100  # 100 ms = 0.1 sec

# load the background images
frames = [PhotoImage(file='dino%i.png' % i) for i in range(4)]

dino_img = PhotoImage(file='dino0.png')
cactus_mix1_img = PhotoImage(file='cactus_mix1.png')
cactus_mix2_img = PhotoImage(file='cactus_mix2.png')
cactus_big_img = PhotoImage(file='cactus-big.png')
cactus_small_img = PhotoImage(file='cactus-small.png')
ground_img = PhotoImage(file='ground.png')
cloud_img = PhotoImage(file='cloud.png')  # a static image for decoration purposes

# display the background images
ground_obj = canvas.create_image(WIDTH / 2, HEIGHT - ground_img.height() / 2, image=ground_img)
cloud_obj = canvas.create_image(WIDTH - cloud_img.width(), cloud_img.height() + 200, image=cloud_img)
cactus_big_obj = canvas.create_image(WIDTH + cactus_big_img.width() / 2, 473, image=cactus_big_img)
cactus_small_obj = canvas.create_image(WIDTH + cactus_small_img.width() / 2, 473, image=cactus_small_img)
cactus_mix1_obj = canvas.create_image(WIDTH + 140, 465, image=cactus_mix1_img)
cactus_mix2_obj = canvas.create_image(WIDTH + 230, 635, image=cactus_mix2_img)
dino_obj = canvas.create_image(50 + dino_img.width(), dino_img.height() + 390, image=frames[frame_index])


# This function is called when a jump is initiated
def jump(__self__):
    global in_a_jump  # use global variable (defined outside the function)
    if not in_a_jump:  # only process the jump event if no other jump is in progress
        in_a_jump = True


def update1():
    global frame_index, in_a_jump, jump_index  # use global variables (defined outside the function)
    canvas.itemconfig(dino_img, image=frames[frame_index])  # set the next frame to the 'flappy_wings' image

    # handle the 'jump' part of the animation
    if in_a_jump:  # if in a jump, move the character by jump_offset
        jump_offset = jump_offsets[jump_index]  # pick the current offset
        canvas.move(dino_img, 0,
                    jump_offset)  # the 'canvas.move' function moves the specified object by the given X,Y pixels
        jump_index = jump_index + 1  # prepare for the next phase of the jump
        if jump_index > len(jump_offsets) - 1:  # when the jump ends...
            jump_index = 0  # ...reset the jump_index...
            in_a_jump = False  # ...and set in_a_jump back to False

    # update the frame picture
    dino_obj.configure(text='frame %i' % frame_index)
    frame_index += 1
    if frame_index == 3:
        frame_index = 0
    win.after(DELAY, update1)


def update():
    global r, frame_index, in_a_jump, jump_offsets, jump_index
    (x, y) = canvas.coords(cloud_obj)  # this picks the coordinates of the given object
    if x >= 0:
        canvas.move(cloud_obj, -5, 0)  # move the background to the left by changing the X by -20
        canvas.move(cloud_obj, WIDTH, 0)  # reset the background, moving it back to the starting point
    # next handle the 'ground' part of the background - it moves at a faster pace: 20 pixels / frame
    (x, y) = canvas.coords(ground_obj)
    if x >= 0:
        canvas.move(ground_obj, -20, 0)  # move the background to the left by changing the X by -20
    else:
        canvas.move(ground_obj, WIDTH + 40, 0)  # reset the background, moving it back to the starting point
    (x, y) = canvas.coords(cactus_small_obj)  # this picks the coordinates of the given object
    if r == 1:
        if x >= 0:
            canvas.move(cactus_small_obj, -15, 0)  # move the background to the left by changing the X by -20
        else:
            r = random.randint(1, 4)
            canvas.move(cactus_small_obj, WIDTH + 40, 0)  # reset the background, moving it back to the starting point
    (x, y) = canvas.coords(cactus_big_obj)  # this picks the coordinates of the given object
    if r == 2:
        if x >= 0:
            canvas.move(cactus_big_obj, -15, 0)  # move the background to the left by changing the X by -20
        else:
            r = random.randint(1, 4)
            canvas.move(cactus_big_obj, WIDTH + 40, 0)  # reset the background, moving it back to the starting point
    (x, y) = canvas.coords(cactus_mix1_obj)
    if r == 3:
        if x >= 0:
            canvas.move(cactus_mix1_obj, -15, 0)  # move the background to the left by changing the X by -20
        else:
            r = random.randint(1, 4)
            canvas.move(cactus_mix1_obj, WIDTH + 120, 0)  # reset the background, moving it back to the starting point
    (x, y) = canvas.coords(cactus_mix2_obj)
    if r == 4:
        if x >= 0:
            canvas.move(cactus_mix2_obj, -15, 0)  # move the background to the left by changing the X by -20
        else:
            r = random.randint(1, 4)
            canvas.move(cactus_mix2_obj, WIDTH + 235, 0)  # reset the background, moving it back to the starting point
    (x, y) = canvas.coords(dino_obj)
    print ("x", x)
    print ("y", y)
    if in_a_jump == True:
        frame_index = 3
        canvas.move(dino_obj, 0, jump_offsets[jump_index])
        jump_index += 1
    else:
        jump_index = 0
        frame_index = frame_index + 1
        canvas.move(dino_obj, 0, jump_offsets[jump_index])
    if frame_index == 3:
        frame_index = 0

    win.bind("<space>", jump)
    win.after(DELAY, update)  # repeat the loop


win.after(0, update1)
win.after(0, update)
win.mainloop()
