#!/usr/bin/python
import time
import os
import sys
import pygame
import numpy
from PIL import Image, ImageDraw, ImageChops
#import matplotlib.pyplot as plt
#from scipy.misc import imread, imsave, imresize
from scipy import misc
from scipy.ndimage import gaussian_filter, median_filter


print("")
print("")
print(" USE l=3 to take a photo every 3 somethings, try a 1000 or 2")
print("      t  to take triggered photos ")
print("     cap=/home/pi/folder/ to set caps path other than current dir")
print("      ")

s_val = "10"
c_val = "2"
g_val = "10"
b_val = "15"
x_dim = 1600
y_dim = 896
additonal_commands = "-d/dev/video0 -w"

ypos = 50 #size of buttons
to_graph = False

#try:
#    cappath = os.getcwd()
##except:
#    print("  COULD NOT GET CURRENT DIR SET WITH A FLAG ")
cappath = "./"
#    print("  COULD NOT GET CURRENT DIR SET WITH A FLAG ")

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
    os.system(cmd)
    print("Image taken and saved to "+cappath+filename)
    return filename

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
            wait_num = int(str(argu).split('=')[1])
        except:
            print("No speed supplied, taking every 10")
            wait_num = 10
        loop = True
    elif thearg == 't' or thearg == 'TRIGGERED':
        trig = True
print(" Saving files to, " + str(cappath))

pygame.init()
display_width = x_dim+75
display_height = y_dim+55
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Most recent image')
clock = pygame.time.Clock()
crashed = False

def show_pic(imgtaken, x=0,y=0):
    gameDisplay.blit(imgtaken, (x,y))

def draw_menu():
    #gameDisplay.blit(button, (but1x,but1y))
    pygame.draw.rect(gameDisplay, (50,200,50), (10,  ypos+10,     50,ypos), 5)
    pygame.draw.rect(gameDisplay, (100,200,100), (10,((ypos+10)*2), 50,ypos), 5)
    pygame.draw.rect(gameDisplay, (100,100,200), (10,((ypos+10)*3), 50,ypos), 5)
    pygame.draw.rect(gameDisplay, (100,200,100), (10,((ypos+10)*4), 50,ypos), 5)
    pygame.draw.rect(gameDisplay, (100,100,200), (10,((ypos+10)*5), 50,ypos), 5)
    pygame.draw.rect(gameDisplay, (50,200,50),   (10,((ypos+10)*6), 50,ypos), 5)
    pygame.draw.rect(gameDisplay, (200,100,200), (10,((ypos+10)*7), 50,ypos), 5)
    pygame.draw.rect(gameDisplay, (50,200,50),   (10,((ypos+10)*8), 50,ypos), 5)
    pygame.draw.rect(gameDisplay, (50,200,50), (10,((ypos+10)*9), 50,ypos), 5)
    pygame.draw.rect(gameDisplay, (50,200,50), (10,((ypos+10)*10), 50,ypos), 5)
    pygame.draw.rect(gameDisplay, (50,200,50), (10,((ypos+10)*11), 50,ypos), 5)
    pygame.draw.rect(gameDisplay, (50,200,50), (10,((ypos+10)*12), 50,ypos), 5)


box_Rect = pygame.Rect(10, ypos+10, 50, ypos)
box2_Rect = pygame.Rect(10, ((ypos+10)*2), 50, ypos)
box3_Rect = pygame.Rect(10, ((ypos+10)*3), 50, ypos)
box4_Rect = pygame.Rect(10, ((ypos+10)*4), 50, ypos)
box5_Rect = pygame.Rect(10, ((ypos+10)*5), 50, ypos)
box6_Rect = pygame.Rect(10, ((ypos+10)*6), 50, ypos)
box7_Rect = pygame.Rect(10, ((ypos+10)*7), 50, ypos)
box8_Rect = pygame.Rect(10, ((ypos+10)*8), 50, ypos)
box9_Rect = pygame.Rect(10,  ((ypos+10)*9), 50, ypos)
box10_Rect = pygame.Rect(10, ((ypos+10)*10), 50, ypos)
box11_Rect = pygame.Rect(10, ((ypos+10)*11), 50, ypos)
box12_Rect = pygame.Rect(10, ((ypos+10)*12), 50, ypos)


##
## Initial Image collection before loop starts;
##
gameDisplay.fill((255,255,255))
#current photo
c_photo = photo()
pil_c_photo = Image.open(c_photo)
numpy_pic = numpy.array(pil_c_photo)
#previous photo
b_photo = photo()
pil_b_photo = Image.open(b_photo)
numpy_pic_b = numpy.array(pil_b_photo)
#masks
mask  = numpy_pic_b > numpy_pic + 30 #the +30 gets rid of noise
mask2 = numpy_pic_b < numpy_pic - 30
e_pic = numpy_pic.copy()
e_pic[:,:,:] = 0  #hash this out to start with a photo

margin = 25
num = 0
colour_values = []
font = pygame.font.SysFont("comicsansms", 72)

def t_impcent(part):
    return 100 * float(part)/float(1096704000)
def s_impcent(part):
    return 100 * float(part)/float(365568000)


but1x = 30
but1y = 50
persistant = 0
show_style = 0
denoise = 1
mask_option = 1  # used in menu


while not crashed:
    gameDisplay.fill((240,255,240))
    for eve in pygame.event.get():
        #print("-------------")
        #print event
        #print("-------------")
        if eve.type == pygame.QUIT:
            crashed = True
        elif eve.type ==  pygame.MOUSEBUTTONDOWN:
            posx = int(eve.pos[0])
            posy = int(eve.pos[1])
            Mouse_Rect = pygame.Rect(posx, posy, 2, 2)
            if box_Rect.contains(Mouse_Rect):
                print("Blanking the edited pics")
                pygame.draw.rect(gameDisplay, (200,50,200), (15,65, 40,40), 15)
                e_pic[:,:,:] = 0
                old_e[:,:,:] = 0
            elif box2_Rect.contains(Mouse_Rect):
                print("cycling persistance up")
                persistant = persistant + 1
            elif box3_Rect.contains(Mouse_Rect):
                print("cycling persistance down")
                persistant = persistant - 1
                #if persistant <= -1:
                #    persistant = -1
            elif box4_Rect.contains(Mouse_Rect):
                print("increasing margin")
                margin = margin + 1
            elif box5_Rect.contains(Mouse_Rect):
                print("margin going down...")
                margin = margin - 1
                if margin <= 0:
                    margin = 0
            elif box6_Rect.contains(Mouse_Rect):
                print("---SHOW STYLE---")
                pygame.draw.rect(gameDisplay, (200,50,200), (15,365, 40,40), 15)
                show_style = show_style + 1
                if show_style >= 8:
                    show_style = 0
                print show_style
            elif box7_Rect.contains(Mouse_Rect):
                print("denoise cycle...")
                pygame.draw.rect(gameDisplay, (200,50,200), (15,425, 40,40), 15)
                denoise = denoise + 1
                if denoise >= 6:
                    denoise = 0
            elif box8_Rect.contains(Mouse_Rect):
                print("mask cycle...")
                pygame.draw.rect(gameDisplay, (200,50,200), (15,485, 40,40), 15)
                mask_option = mask_option + 1
                if mask_option >= 9:
                    mask_option = 1



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

    #mask  = numpy_pic_b > numpy_pic + 30 #the +30 gets rid of noise
    #mask2 = numpy_pic_b < numpy_pic - 30


    #numpy_pic[mask] = [0, 0, 255]


    #    if show1 == '1':
    #        e_pic = ((e_pic/4) - (numpy_pic))*3
    #        e_pic = e_pic / 3 + old_e / 2
    #    elif show1 == 'tripsy':
    #        e_pic = ((e_pic/4) - (numpy_pic))*3
    #        e_pic = e_pic - old_e / 2
    ##    elif show1 == 'waa':
    #        e_pic = ((e_pic/4) - (numpy_pic))*3
    #        #e_pic = old_e * 0.8 + e_pic * 0.2
    #    Image.fromarray(e_pic).save(e_photo)







  #define, name and blank images
    e_photo= "numpy_"+str(str(time.time()).split(".")[0])+".jpg"   #name to save the edited photo as
    num = num + 1                        #frame count
    b_photo = c_photo                    #current photo becomes before photo.
    numpy_pic_b = numpy_pic.copy()       #and for the numpy loaded image
    c_photo = photo()                    #take a new photo for the current image
    pil_c_photo = Image.open(c_photo)    #load the just taken photo
    numpy_pic = numpy.array(pil_c_photo) #turn it into a numpy array
    #print numpy_pic.size
    old_e = e_pic.copy()                 #current edited pic becomes old edited pic
    e_pic[:,:,:] = 0                     #current edited pic is blanked
    mask_b_pic = e_pic.copy()            #blank the b mask (brighter pixels)
    mask_d_pic = e_pic.copy()            #blank the d mask (darker pixels)
    mask_m_pic = e_pic.copy()            #blank the m mask (all that isn't mask)

    pygame.display.set_caption(str(margin))
    maskr = numpy_pic[:, :, 0] < numpy_pic_b[:, :, 0] - margin
    maskg = numpy_pic[:, :, 1] < numpy_pic_b[:, :, 1] - margin
    maskb = numpy_pic[:, :, 2] < numpy_pic_b[:, :, 2] - margin
    maskr2 = numpy_pic[:, :, 0] > numpy_pic_b[:, :, 0] + margin
    maskg2 = numpy_pic[:, :, 1] > numpy_pic_b[:, :, 1] + margin
    maskb2 = numpy_pic[:, :, 2] > numpy_pic_b[:, :, 2] + margin
    mask_all_b = numpy_pic[:, :, :] > numpy_pic_b[:, :, :] + margin
    mask_all_d = numpy_pic[:, :, :] < numpy_pic_b[:, :, :] + margin

  #mask_m options
    if mask_option == 1:
        mask_m_pic[mask_all_b] = 255
        #m_mask = mask_b_pic[:, :, :] < 254
        #mask_m_pic[m_mask] = 100
        mask_text = "all b"
    elif mask_option == 2:
        mask_m_pic[mask_all_d] = 255
        #m_mask = mask_d_pic[:, :, :] < 254
        #mask_m_pic[m_mask] = 0
        mask_text = "all d"
    elif mask_option == 3:
        mask_b_pic[maskr] = [255, 255, 255]
        mask_b_pic[maskg] = [255, 255, 255]
        mask_b_pic[maskb] = [255, 255, 255]
        mask_d_pic[maskr2] = [0, 0, 0]
        mask_d_pic[maskg2] = [0, 0, 0]
        mask_d_pic[maskb2] = [0, 0, 0]
        mask_m_pic = mask_b_pic + mask_d_pic
        mask_text = "Two Tone Movement Mask"
    elif mask_option == 4:
        mask_b_pic[maskr] = [0, 0, 0]
        mask_b_pic[maskg] = [0, 0, 0]
        mask_b_pic[maskb] = [0, 0, 0]
        mask_d_pic[maskr2] = [255, 255, 255]
        mask_d_pic[maskg2] = [255, 255, 255]
        mask_d_pic[maskb2] = [255, 255, 255]
        mask_m_pic = mask_b_pic + mask_d_pic
        mask_text = "Two Tone b Movement Mask"
    elif mask_option == 5:
        mask_b_pic[maskr] = [200, 10, 10]
        mask_b_pic[maskg] = [10, 200, 10]
        mask_b_pic[maskb] = [10, 10, 200]
        mask_d_pic[maskr2] = [255, 255, 255]
        mask_d_pic[maskg2] = [255, 255, 255]
        mask_d_pic[maskb2] = [255, 255, 255]
        mask_m_pic = mask_b_pic + mask_d_pic
        mask_text = "RGB and Black Movement Mask"
    elif mask_option == 6:
        mask_b_pic[maskr] = [200, 10, 10]
        mask_b_pic[maskg] = [10, 200, 10]
        mask_b_pic[maskb] = [10, 10, 200]
        mask_d_pic[maskr2] = [200, 10, 10]
        mask_d_pic[maskg2] = [10, 200, 10]
        mask_d_pic[maskb2] = [10, 10, 200]
        mask_m_pic = mask_d_pic + mask_b_pic
        mask_text = "RGB and RGB Movement Mask"
    elif mask_option == 7:
        mask_b_pic[maskr] = [188, 5, 5]
        mask_b_pic[maskg] = [91, 217, 54]
        mask_b_pic[maskb] = [213, 217, 32]
        mask_d_pic[maskr2] = [188, 5, 5]
        mask_d_pic[maskg2] = [91,217,54]
        mask_d_pic[maskb2] = [213, 217, 32]
        mask_m_pic = mask_d_pic
        mask_text = "Rasta Movement Mask"
    elif mask_option == 8:
        mask_b_pic[maskr] = [188, 5, 5]
        mask_b_pic[maskg] = [91, 217, 54]
        mask_b_pic[maskb] = [213, 217, 32]
        mask_d_pic[maskr2] = [188, 5, 5]
        mask_d_pic[maskg2] = [91,217,54]
        mask_d_pic[maskb2] = [213, 217, 32]
        mask_m_pic = mask_d_pic / mask_b_pic
        mask_text = "Rasta Movement Mask"
 #change text
    mask_text = font.render(str(mask_text), True, (0, 128, 0))
    mask_button = font.render("M:"+str(mask_option), True, (50, 100, 50))
    gameDisplay.blit(mask_button, (6, (ypos+10)*8))


  #denoise option
    denoise_text = ""
    if denoise == 1:
        e_pic = median_filter(e_pic, 3)
        denoise_text = "Denoising edited image"
    elif denoise == 2:
        mask_m_pic = median_filter(mask_m_pic, 3)
        denoise_text = "Denoising m mask"
    elif denoise == 3:
        mask_d_pic = median_filter(mask_d_pic, 3)
        denoise_text = "Denoising d mask"
    elif denoise == 4:
        mask_b_pic = median_filter(mask_b_pic, 3)
        denoise_text = "Denoising b mask"
    elif denoise == 5:
        denoise_text = ""
    denoise_text = font.render(str(denoise_text), True, (0, 128, 0))
    de_button = font.render(str(denoise), True, (50, 100, 50))
    gameDisplay.blit(de_button, (12, (ypos+10)*7))
    print denoise_text



#Persist option
    if persistant == 0:
        print("-no persist")
        e_pic = mask_m_pic
    elif persistant <= -1: #deducts multipul of prior edited image
        e_pic = mask_m_pic - ((old_e * abs(persistant) / (abs(persistant)-1)))
    elif persistant == 1:  #simple addition with prior edited image
        e_pic = mask_m_pic + old_e
    elif persistant >= 2:  #fade increases as number increases
        e_pic = mask_m_pic + ((old_e/persistant)*(persistant-1))
    text = font.render(str(persistant), True, (0, 128, 0))
    gameDisplay.blit(text, (20, 120))
#show style option
    if show_style == 0:
        show_pic = e_pic + (numpy_pic/2)
        text = ("Showing; edited pic and half the original image")
    elif show_style == 2:
        show_pic = e_pic
        text = ("Showing; edit pic only")
    elif show_style == 1:
        show_pic = e_pic + numpy_pic
        text = ("Showing; edit pic plus original pic")
    elif show_style == 3:
        show_pic = mask_m_pic
        text = ("Showing; showing the current m mask")
    elif show_style == 4:
        show_pic = mask_b_pic
        text = ("Showing; showing current b mask")
    elif show_style == 5:
        show_pic = mask_d_pic
        text = ("Showing; shiwing current d mask")
    elif show_style == 6:
        show_pic = mask_b_pic + mask_d_pic
        text = ("Showing; show d mask plus b mask")
    elif show_style == 7:
        show_pic = numpy_pic
        text = ("Showing; orginal image")
    text = font.render(str(text), True, (50, 128, 0))
    show_button = font.render(str(show_style), True, (50, 128, 0))
    gameDisplay.blit(show_button, (15, (ypos+10)*6))
    gameDisplay.blit(text, (2, y_dim+2))
#


    #show_pic = imresize(show_pic, (500, 500))
    #show_pic = gaussian_filter(show_pic, sigma=3)
    #show_pic = median_filter(show_pic, 3)






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
    if to_graph == True:
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



    onscreen = pygame.image.load(e_photo)
    gameDisplay.blit(onscreen, (75,0))
    if to_graph == True:

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

    #largeText = pygame.font.Font('freesansbold.ttf',115)
    #TextSurf, TextRect = text_objects("A bit Racey", largeText)
    #TextRect.center = ((display_width/2),(display_height/2))
    #gameDisplay.blit(TextSurf, TextRect)


    draw_menu()
    gameDisplay.blit(denoise_text, (2, y_dim-55))
    gameDisplay.blit(mask_text,  (2, y_dim-95))
    pygame.display.update()


    if trig == True:
        print("Waiting for input before taking next image...")
        tp = raw_input("press return to take picture; ")
        if tp == "q":
            print("---bye!")
            exit()
        clock.tick(20)
    if loop == True:
        print("waiting; " + str(wait_num))
        pygame.time.wait(wait_num)
        clock.tick(20)
    elif trig == False and loop == False:
        crashed = True

#while True:
    #pygame.time.wait(1000)
    #clock.tick(20)

pygame.quit()
quit()
