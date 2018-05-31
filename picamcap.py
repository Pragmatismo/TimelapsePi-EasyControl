#!/usr/bin/python
import time
import os
import sys
from picamera import PiCamera

print("")
print("")
print(" USE l=3 to take a photo every 3 somethings")
print("      t  to take triggered photos ")
print("     cap=/home/pi/folder/ to set caps path other than current dir")
print("      ")
pi_paper = False  #updates pi wall paper, use -nopaper to turn it off.

s_val = "0"   # saturation -100 to 100
c_val = "0"   # contrast -100 to 100
g_val = "800"  # iso 100 - 800
b_val = "15"
x_dim = 1600
y_dim = 1200
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

# take and save photo
camera = PiCamera()
camera.resolution = (int(x_dim),int(y_dim))
camera.contrast = int(c_val)
camera.saturation = int(s_val)
camera.iso =  int(g_val)
camera.vflip = True
time.sleep(1)
def photo():

    timenow = time.time()
    timenow = str(timenow)[0:10]
    filename= "cap_"+str(timenow)+".jpg"
    camera.capture(cappath+filename)

    print("Image taken and saved to "+cappath+filename)
    #os.system("gpicview " + cappath+filename)
    if pi_paper == True:
        os.system("export DISPLAY=:0 && pcmanfm --set-wallpaper "+cappath+filename)

def TRIGGERED():
    while True:
        red = raw_input("press return to take picture")
        if red == "q":
            camera.close()
            exit()
        else:
            photo()

def LOOPED(num=10):
    while True:
        photo()
        time.sleep(num)

if 'np' in sys.argv or 'nopaper' in sys.argv:
    pi_paper = False
    print(" Not going to try changing wall paper")

loop = False
trig = False
for argu in sys.argv[1:]:
    try:
        thearg = str(argu).split('=')[0]
    except:
        thearg = str(argu)

    if thearg == 'cap' or thearg =='cappath':
        cappath = str(argu).split('=')[1]

    if thearg == 'l' or thearg == 'looped':
        try:
            num = float(str(argu).split('=')[1])
        except:
            print("No speed supplied, taking every 10")
            num = 10
        loop = True

    if thearg == 't' or thearg == 'TRIGGERED':
        trig = True

print(" Saving files to, " + str(cappath))

if loop == True:
    LOOPED(num)
elif trig == True:
    TRIGGERED()
else:
    photo()

camera.close()
