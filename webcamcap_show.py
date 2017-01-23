#!/usr/bin/python
import time
import os
import sys
import pygame
from PIL import Image

print("")
print("")
print(" USE l=3 to take a photo every 3 somethings, try a 1000 or 2")
print("      t  to take triggered photos ")
print("     cap=/home/pi/folder/ to set caps path other than current dir")
print("      ")
pi_paper = False  #updates pi wall paper, use -nopaper to turn it off.

s_val = "10"
c_val = "2"
g_val = "10"
b_val = "15"
x_dim = 1600
y_dim = 896
additonal_commands = "-d/dev/video0 -w"

try:
    cappath = os.getcwd()
    cappath += "/"
except:
    print("  COULD NOT GET CURRENT DIR SET WITH A FLAG ")
    cappath = "./"
    print("  COULD NOT GET CURRENT DIR SET WITH A FLAG ")


#cappath = "./"   #wont update wallpaper, i dunno, it might..

loc_settings = "./camera_settings.txt"
try:
    with open(loc_settings, "r") as f:
        for line in f:
            s_item = line.split("=")
            if s_item[0] == "s_val":
                s_val = s_item[1].split("\n")[0]
            elif s_item[0] == "c_val":
                c_val = s_item[1].split("\n")[0]
            elif s_item[0] == "g_val":
                g_val = s_item[1].split("\n")[0]
            elif s_item[0] == "b_val":
                b_val = s_item[1].split("\n")[0]
            elif s_item[0] == "x_dim":
                x_dim = s_item[1].split("\n")[0]
            elif s_item[0] == "y_dim":
                y_dim = s_item[1].split("\n")[0]
            elif s_item[0] == "additonal_commands":
                additonal_commands = s_item[1].split("\n")[0]
except:
    print("No config file for camera, using default")
    print("Run cam_config.py to create one")


def photo():
    # take and save photo
    timenow = time.time()
    timenow = str(timenow)[0:10]
    filename= "cap_"+str(timenow)+".jpg"

    #os.system("uvccapture "+additonal_commands+" -S"+s_val+" -C" + c_val + " -G"+ g_val +" -B"+ b_val +" -x"+str(x_dim)+" -y"+str(y_dim)+" -v -t0 -o"+cappath+filename)

    os.system("uvccapture "+additonal_commands+" -x"+str(x_dim)+" -y"+str(y_dim)+" -v -t0 -o"+cappath+filename)

    print("Image taken and saved to "+cappath+filename)

    if pi_paper == True:
        os.system("export DISPLAY=:0 && pcmanfm --set-wallpaper "+cappath+filename)
    return filename


def TRIGGERED():
    while True:
        red = raw_input("press return to take picture; ")
        if red == "q":
            exit()
        else:
            photo()

def LOOPED(num=10):
    while True:
        photo()
        time.sleep(num)

if 'wp' in sys.argv or 'wallpaper' in sys.argv:
    pi_paper = True
    print(" Going to try changing wall paper")

loop = False
trig = False
onion = False
for argu in sys.argv[1:]:
    try:
        thearg = str(argu).split('=')[0]
    except:
        thearg = str(argu)

    if thearg == 'cap' or thearg =='cappath':
        cappath = str(argu).split('=')[1]

    elif thearg == 'l' or thearg == 'looped':
        try:
            num = int(str(argu).split('=')[1])
        except:
            print("No speed supplied, taking every 10")
            num = 10
        loop = True

    elif thearg == 't' or thearg == 'TRIGGERED':
        trig = True
    elif thearg == 'o' or thearg == 'onion':
        onion = True

print(" Saving files to, " + str(cappath))

#if loop == True:
#    LOOPED(num)
#elif trig == True:
#    TRIGGERED()
#else:
    #photo()
#    print("running pygame loop")

pygame.init()
display_width = x_dim
display_height = y_dim
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Most recent image')
black = (0,0,0)
white = (255,255,255)
clock = pygame.time.Clock()
crashed = False


def show_pic(imgtaken, x=0,y=0):
    gameDisplay.blit(imgtaken, (x,y))

gameDisplay.fill(white)
if onion == True:
    imgtaken = photo()
    imgtaken = pygame.image.load(imgtaken)
    gameDisplay.blit(imgtaken, (0,0))
    pygame.display.update()

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    if onion == True:
        penImg = imgtaken
        penImg.set_alpha(255)
        imgtaken = photo()
        imgtaken = pygame.image.load(imgtaken)
        gameDisplay.blit(penImg, (0,0))
        imgtaken.set_alpha(100)
    else:
        imgtaken = photo()
        imgtaken = pygame.image.load(imgtaken)
        #gameDisplay.fill(white)

    gameDisplay.blit(imgtaken, (0,0))
    pygame.display.update()

    if trig == True:
        print("Waiting for input before taking next image...")
        tp = raw_input("press return to take picture; ")
        if tp == "q":
            exit()
        clock.tick(20)
    if loop == True:
        pygame.time.wait(num)
        clock.tick(20)
    elif trig == False and loop == False:
        crashed = True

pygame.quit()
quit()
