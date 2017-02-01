#!/usr/bin/python
import time
import os
import sys
import pygame
import numpy
from PIL import Image, ImageDraw, ImageChops

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
    cmd = str("uvccapture "+additonal_commands+" -x"+str(x_dim)+" -y"+str(y_dim)+" -v -t0 -o"+cappath+filename)
    print("####")
    print("####")
    print cmd
    print("####")
    print("####")
    os.system(cmd)
    print("Image taken and saved to "+cappath+filename)
    if pi_paper == True:
        os.system("export DISPLAY=:0 && pcmanfm --set-wallpaper "+cappath+filename)
    return filename

if 'wp' in sys.argv or 'wallpaper' in sys.argv:
    pi_paper = True
    print(" Going to try changing wall paper")

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

import matplotlib.pyplot as plt


def show_pic(imgtaken, x=0,y=0):
    gameDisplay.blit(imgtaken, (x,y))

gameDisplay.fill(white)

c_photo = photo()
pil_c_photo = Image.open(c_photo)
numpy_pic = numpy.array(pil_c_photo)

b_photo = photo()
pil_b_photo = Image.open(b_photo)
numpy_pic_b = numpy.array(pil_b_photo)

mask  = numpy_pic_b > numpy_pic + 30 #the +30 gets rid of noise
mask2 = numpy_pic_b < numpy_pic - 30
lol = mask + mask2
e_pic = numpy_pic.copy()
e_pic[:,:,:] = 0  #hash this out to start with a photo

margin = 0
num = 0
colour_values = []

def t_impcent(part):
    return 100 * float(part)/float(1096704000)
def s_impcent(part):
    return 100 * float(part)/float(365568000)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    timenow = time.time()
    e_photo = str(timenow).split(".")[0]
    e_photo= "numpy_"+str(timenow)+".jpg"
    num = num + 1

    b_photo = c_photo

    c_photo = photo()
    numpy_pic_b = numpy_pic.copy()
    pil_c_photo = Image.open(c_photo)
    numpy_pic = numpy.array(pil_c_photo)

    print numpy_pic.size
    #print len(numpy_pic[3])
    print "###"
    #print numpy_pic[1:,1,1]

    #a = np.arange(100)
    print "##########"
    #numpy_pic[1:500, range(0, len(numpy_pic[2]), 10), 1] = 0
    #for x in numpy_pic[1:500, range(0, len(numpy_pic[2])), 1]:
    #    if x >= 100:
    #        x = 255
    #for x in range(10,170,10):
    #    mask = numpy_pic < x
    #    numpy_pic[mask] = 255-x #numpy_pic[mask] + numpy_pic[mask]
    #for x in range(200,255,5):
    #    mask = numpy_pic > x
    #    numpy_pic[mask] = 0+(x/10) # numpy_pic[mask] / numpy_pic[mask]+(numpy_pic[mask]/numpy_pic[mask])


    #print numpy_pic[1:,1,1]
    #print numpy_pic.min()
    print "###"
    #print numpy_pic.shape #Array dimensions
    #print numpy_pic.ndim #Number of array dimensions
    #print numpy_pic.dtype #Data type of array elements
    #print numpy_pic.dtype.name #Name of data type
    #print numpy_pic.mean()
    #print numpy_pic.max()
    #print numpy_pic.min()
    #print numpy.info(numpy.ndarray.dtype)
    #print numpy_pic.astype(int)



    #mask = numpy_pic > numpy_pic_b
    #mask = numpy_pic[:, :, 2] > 150
    #numpy_pic[mask] = [0, 0, 255]
    #lol = numpy_pic +

    #mask  = numpy_pic_b > numpy_pic + 30 #the +30 gets rid of noise
    #mask2 = numpy_pic_b < numpy_pic - 30
    margin = 21 # margin + 1
    pygame.display.set_caption(str(margin))
    maskr = numpy_pic[:, :, 0] < numpy_pic_b[:, :, 0] - margin
    maskg = numpy_pic[:, :, 1] < numpy_pic_b[:, :, 1] - margin
    maskb = numpy_pic[:, :, 2] < numpy_pic_b[:, :, 2] - margin
    maskr2 = numpy_pic[:, :, 0] > numpy_pic_b[:, :, 0] + margin
    maskg2 = numpy_pic[:, :, 1] > numpy_pic_b[:, :, 1] + margin
    maskb2 = numpy_pic[:, :, 2] > numpy_pic_b[:, :, 2] + margin
    #numpy_pic[mask] = [0, 0, 255]

    #lol_old = lol
    #lol = mask + mask2
    #lol = lol + lol_old
    persist = 'ohhh'
    if persist == 'True':
        numpy_pic[maskr] = [255, 0, 0]
        numpy_pic[maskg] = [0, 255, 0]
        numpy_pic[maskb] = [0, 0, 255]
        numpy_pic[maskb2] = [0, 0, 100]
        numpy_pic[maskr2] = [100, 0, 0]
        numpy_pic[maskg2] = [0, 100, 0]
        Image.fromarray(numpy_pic).save(e_photo)
    elif persist == 'False':
        old_e = e_pic
        e_pic = numpy_pic.copy()
        e_pic[maskr] = [255, 0, 0]
        e_pic[maskg] = [0, 255, 0]
        e_pic[maskb] = [0, 0, 255]
        e_pic[maskr2] = [100, 0, 0]
        e_pic[maskg2] = [0, 100, 0]
        e_pic[maskb2] = [0, 0, 100]
        show1 = 'waa'
        if show1 == '1':
            e_pic = ((e_pic/4) - (numpy_pic))*3
            e_pic = e_pic / 3 + old_e / 2
        elif show1 == 'tripsy':
            e_pic = ((e_pic/4) - (numpy_pic))*3
            e_pic = e_pic - old_e / 2
        elif show1 == 'waa':
            e_pic = ((e_pic/4) - (numpy_pic))*3
            #e_pic = old_e * 0.8 + e_pic * 0.2
        Image.fromarray(e_pic).save(e_photo)

    elif persist == 'ohhh':
        old_e = e_pic.copy()
        mask_b_pic = numpy_pic.copy()
        mask_d_pic = numpy_pic.copy()
        mask_m_pic = numpy_pic.copy()
        e_pic[:,:,2] = 0
        e_pic[:,:,1] = 0
        e_pic[:,:,0] = 0
        mask_b_pic[maskr] = [255, 255, 255]
        mask_b_pic[maskg] = [255, 255, 255]
        mask_b_pic[maskb] = [255, 255, 255]
        #mask_d_pic[maskr2] = [0, 0, 0]
        #mask_d_pic[maskg2] = [0, 0, 0]   -two tone, good for many of the below modes
        #mask_d_pic[maskb2] = [0, 0, 0]
        mask_d_pic[maskr2] = [255, 255, 255]
        mask_d_pic[maskg2] = [255, 255, 255]
        mask_d_pic[maskb2] = [255, 255, 255]

        m_mask = mask_b_pic[:, :, 0] < 254
        mask_m_pic[m_mask] = [0,0,0]

        #m_mask = mask_d_pic[:, :, 0] < 254
        #mask_m_pic[m_mask] = [100,0,0]

        e_pic =  mask_m_pic #+ old_e #_pic
        show_pic = e_pic + (numpy_pic/2)


        #e_pic = e_pic/6 + old_e

        #e_pic = e_pic/2 - ((mask_d_pic) + (mask_b_pic))
        #e_pic = e_pic/2 + ((mask_d_pic) + (mask_b_pic))
                                      #choose one of the following
        #e_pic = mask_d_pic               #shows when pixel is darker than it was
        #e_pic = mask_b_pic              #shows when pixel is lighter than prior
        #e_pic = mask_d_pic - mask_b_pic  #black execpt for movement
        #e_pic = mask_b_pic / (mask_d_pic / 100)  #odd
        #e_pic = mask_d_pic + mask_b_pic  #looks odd
        #e_pic = mask_d_pic - (old_e/3)*2  #persists and looks cool
        #e_pic = ((mask_d_pic + mask_b_pic) - (old_e/8)*2)
        #e_pic = ( ((mask_d_pic + mask_b_pic) ) - (old_e)) #* 2


        #show_pic = e_pic
        Image.fromarray(show_pic).save(e_photo)
        r_sum = numpy_pic[:,:,0].sum()
        g_sum = numpy_pic[:,:,1].sum()
        b_sum = numpy_pic[:,:,2].sum()
        tot_sum = r_sum + g_sum + b_sum
        print " ---- Current Photo ---"
        print "Red:" + str(r_sum) + " Green:" + str(g_sum) + " Blue:" + str(b_sum)
        print "Total;" + str(tot_sum) #+ " also " + str(numpy_pic[:,:,:].sum())
        #e_pic[:,:,:] = 255
        e_r_sum = e_pic[:,:,0].sum()
        e_g_sum = e_pic[:,:,1].sum()
        e_b_sum = e_pic[:,:,2].sum()
        e_tot_sum = e_r_sum + e_g_sum + e_b_sum
        print " ---- Motion Edited Photo ---"
        print "Red:" + str(e_r_sum) + " Green:" + str(e_g_sum) + " Blue:" + str(e_b_sum)
        print "Total;" + str(e_tot_sum)
        colour_values.append([num, r_sum, g_sum, b_sum, tot_sum, e_r_sum, e_g_sum, e_b_sum, e_tot_sum])




    #plt.imshow(lol)
    #plt.show()
    #Image.fromarray(numpy_pic).save(e_photo)
    onscreen = pygame.image.load(e_photo)
    gameDisplay.blit(onscreen, (0,0))
    for x in colour_values:
        num = x[0]
        r_graph = s_impcent(x[1]) #*2.5
        g_graph = s_impcent(x[2]) #*2.5
        b_graph = s_impcent(x[3]) #*2.5
        tot_graph   = t_impcent(x[4]) *3

        e_r_graph = s_impcent(x[5]) #*2.5
        e_g_graph = s_impcent(x[6]) #*2.5
        e_b_graph = s_impcent(x[7]) #*2.5
        e_tot_graph = t_impcent(x[8]) *2.5

        pygame.draw.line(gameDisplay, (255,50,100), (num, 300-r_graph), (num, 300))
        pygame.draw.line(gameDisplay, (50,255,100), (num, 300-(r_graph+g_graph)), (num, 300-r_graph))
        pygame.draw.line(gameDisplay, (50,50,255), (num, 300-(r_graph+g_graph+b_graph)), (num, 300-(r_graph+g_graph)))
        #e_red_graph = impcent(x[5]) *250)
        #pygame.draw.line(gameDisplay, (255,50,50), (num,300-e_red_graph), (num, 300))
        #pygame.draw.line(gameDisplay, (255,50,100), (num+10,300-tot_graph), (num+10, 300))
        #pygame.draw.line(gameDisplay, (100,50,255), (num+200,600-e_tot_graph), (num+200, 600))

        pygame.draw.line(gameDisplay, (255,50,100), (num, 600 - e_r_graph), (num, 600))
        pygame.draw.line(gameDisplay, (50,255,100), (num, 600 - (e_r_graph + e_g_graph)), (num, 600-e_r_graph))
        pygame.draw.line(gameDisplay, (50,50,255), (num, 600 - (e_r_graph + e_g_graph + e_b_graph)), (num, 600-(e_r_graph + e_g_graph)))



        #print "graph point: " + str(num) + " , " + str(e_red_graph)
        #print "graph point: " + str(num) + " - total of source pic: " + str(tot_graph)
        #print "graph point: " + str(num) + " - total of edited pic: " + str(e_tot_graph)

    pygame.display.update()

    if trig == True:
        print("Waiting for input before taking next image...")
        tp = raw_input("press return to take picture; ")
        if tp == "q":
            print("---bye!")
            exit()
        clock.tick(20)
    if loop == True:
        pygame.time.wait(num)
        clock.tick(20)
    elif trig == False and loop == False:
        crashed = True

#while True:
    #pygame.time.wait(1000)
    #clock.tick(20)

pygame.quit()
quit()
