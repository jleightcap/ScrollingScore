from __future__ import division
from PIL import Image
import os
os.chdir('C:\Users\jleig\Documents\python\Sheet Music')

img = Image.open('1.jpg')                                                       #Defines 16:9 resolution as a function of the height of the first image ('1.jpg')
dummy, heightc = img.size
widthc = int(heightc * 16 / 9)

for f in os.listdir('.'):
    if f.endswith('.jpg'):

        img = Image.open(f)                                                     #Defines scalar constant, resizes for constant height on all images.
        width, height = img.size
        scalar = heightc / height
        size = int(scalar * width), int(scalar * height)
        img.thumbnail(size)

        imgBG = Image.new('L', (widthc, heightc), 255)                          #Creates 16:9 white image with height equal to height of first image (imgBG), centers img(f) on imgBG.
        imgBG = Image.new('L', (widthc, heightc), 255)
        imgBG.paste(img, (int((widthc - width) / 2), 0))
        imgBG.save(f)
