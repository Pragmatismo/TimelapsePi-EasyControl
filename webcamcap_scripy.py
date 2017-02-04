#!/usr/bin/python
import time
import os
import sys
import pygame
from PIL import Image
import numpy
from scipy.ndimage.interpolation import zoom


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
additonal_commands = "-d/dev/video1 -w"

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

loop = False
trig = False
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

print(" Saving files to, " + str(cappath))

pygame.init()
display_width = x_dim
display_height = y_dim
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Most recent image')
black = (0,0,0)
white = (255,255,255)
clock = pygame.time.Clock()
crashed = False

def photo():
    # take and save photo
    timenow = time.time()
    timenow = str(timenow)[0:10]
    filename= "cap_"+str(timenow)+".jpg"
    os.system("uvccapture "+additonal_commands+" -x"+str(x_dim)+" -y"+str(y_dim)+" -v -t0 -o"+cappath+filename)
    print("Image taken and saved to "+cappath+filename)
    return cappath+filename

def show_pic(imgtaken, x=0,y=0):
    gameDisplay.blit(imgtaken, (x,y))

def edit_image(imgtaken):
    pil_c_photo = Image.open(imgtaken)    #load the just taken photo
    numpy_pic = numpy.array(pil_c_photo) #turn it into a numpy array

    edit_pic = numpy_pic.copy()
    edit_pic = zoom(edit_pic, (0.5,0.5,1))
    

    e_loc = imgtaken.split("/")
    e_path = ""
    for e in range(len(e_loc)-1):
        e_path += "/" + str(e_loc[e])
    e_path += "edited_" + str(e_loc[-1])
    Image.fromarray(edit_pic).save(e_path)
    print ("Edited picture at " + e_path)
    return e_path


while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    imgtaken = photo()
    edited_img = edit_image(imgtaken)
    #os.remove(imgtaken)
    py_img = pygame.image.load(edited_img)
    gameDisplay.blit(py_img, (0,0))

    #gameDisplay.blit(imgtaken, (0,0), special_flags=pygame.BLEND_ADD)
    #special_flags=
    #   BLEND_ADD, BLEND_SUB, BLEND_MULT, BLEND_MIN, BLEND_MAX
    #   BLEND_RGBA_ADD, BLEND_RGBA_SUB, BLEND_RGBA_MULT,
    #   BLEND_RGBA_MIN, BLEND_RGBA_MAX BLEND_RGB_ADD,
    #   BLEND_RGB_SUB, BLEND_RGB_MULT, BLEND_RGB_MIN, BLEND_RGB_MAX
    pygame.display.update()

    if trig == True:
        print("Waiting for input before taking next image...")
        tp = raw_input("press return to take picture; ")
        if tp == "q":
            print("---bye!")
            exit()
        elif tp == "o":
            if onion == True:
                onion = False
                print("---Turning onion mode off")
            else:
                onion = True
                print("---Turning onion mode on")
        clock.tick(20)
    if loop == True:
        pygame.time.wait(num)
        clock.tick(20)
    elif trig == False and loop == False:
        crashed = True

pygame.quit()
quit()
