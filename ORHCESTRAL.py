from __future__ import division
from PIL import Image, ImageChops
import os
os.chdir('C:\Users\jleig\Documents\python\Sheet Music')

img = Image.open('1.jpg')                                                       #Defines 16:9 resolution as a function of the height of the first image ('1.jpg')
dummy, heightc = img.size
widthc = int(heightc * 16 / 9)

f = 1
str1 = str(f) + '.jpg'

while str1 in os.listdir('.'):
    if str1.endswith('.jpg'):

        img = Image.open(str1)                                                  #Defines scalar constant, resizes for constant height on all images.
        width, height = img.size
        scalar = heightc / height
        size = int(scalar * width), int(scalar * height)
        img.thumbnail(size)

        imgBG = Image.new('L', (widthc, heightc), 255)
        if f % 2 == 1:                                                          #Odd number, page on left.
            imgBG.paste(img, (int((widthc - 2 * width) / 4), 0))
            imgBG.save(str1)
        else:                                                                   #Even number, page on right.
            imgBG.paste(img, (int((3 * widthc - 2 * width) / 4), 0))
            imgBG.save(str1)

            str2 = str(f - 1) + '.jpg'                                          #Opens previous odd numbered image, multiplies images together, deletes previous odd numbered image
            img2 = Image.open(str2)
            imgBG2 = ImageChops.multiply(imgBG, img2)
            imgBG2.save(str1)
            os.remove(str2)

        f = f + 1
        str1 = str(f) + '.jpg'

f = 2
str1 = str(int(f)) + '.jpg'

while str1 in os.listdir('.'):                                                  #Renames files by halving number
    str2 = str(int(f / 2)) + '.jpg'
    os.rename(str1, str2)

    f = f + 2
    str1 = str(int(f)) + '.jpg'

str1 = str(int(f - 1)) + '.jpg'                                                 #Checks for possible remaining odd-numbered file, renames
if os.path.isfile(str1):
    str2 = str(int(f / 2)) + '.jpg'
    os.rename(str1, str2)
