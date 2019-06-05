import os, sys
from PIL import Image

### TERMINAL ARGUMENTS ###

# -h      := help
# -q      := quiet
# -single := forced one page per slide
args = sys.argv[1:]


# -h, print README and quit
if "-h" in args:
    with open('./README.md') as f:
        print(f.read())
    quit()

# -q, toggle print statements
loud = True
if "-q" in args:
    loud = False

# -single, toggle forced single image per slide
double = True
if "-single" in args:
    double = False
    
def verifyDirectory(dirname):
    if not os.path.isdir(dirname):
        try:
            os.mkdir(dirname)
        except OSError:
            if loud: print("Could not create {} directory.".format(dirname))
            quit()
verifyDirectory('./Sheets')
if not os.listdir('./Sheets'): # Empty sheets directory
    if loud: print("No images to convert.")
verifyDirectory('./Slides')



### IMAGE MANIPULATION ###

# Is better suited for a double slide (two tall images side by side)?
def isTall(img):
    # img = Image.open(img)
    return img.size[0] / img.size[1] < (16/9)

 # White dimensioned BG image
def bgImg(size):
    return Image.new('RGB', size, (255,255,255))

def singleImage(img):
    W, H = img.size
    if W/H > (16/9):
        size = W, int((9/16) * W)
    else:
        size = int((16/9) * H), H
    # size = tuple(buff*x for x in size)
    imgBG = bgImg(size)
    imgBG.paste(img, (int((size[0] - W) / 2), int((size[1] - H) /2))) # Centered on BG
    return imgBG

def twoImage(img1, img2):
    # img1 = Image.open('./Sheets/{}'.format(img1))
    # img2 = Image.open('./Sheets/{}'.format(img2))
    W1, H1 = img1.size
    W2, H2 = img2.size
    imgBG = bgImg((W1 + W2, max(H1, H2)))
    if H1 < H2:
        imgBG.paste(img1, (0,int((H2-H1)/2)))
        imgBG.paste(img2, (W1,0))
    else: # H1 = H2 reduces to either case.
        imgBG.paste(img1, (0,0))
        imgBG.paste(img2, (W1,int((H1-H2)/2)))
    return singleImage(imgBG)

def main():
    imageFormats = ('.jpg', '.png') # If adding image formats, check compatibility with PIL.
    pages = list(filter(lambda x: x.endswith(imageFormats), sorted(os.listdir('./Sheets'))))
    pages = list(map(lambda x: Image.open('./Sheets/{}'.format(x)), pages))
    os.chdir('./Slides')
    filenum = 0
    if double:
        while pages:
            if not pages[1:]:
                singleImage(pages[0]).save('{}.png'.format(filenum))
                if loud: print('e',pages[0])
                break
            elif isTall(pages[0]) and isTall(pages[1]):
                twoImage(pages[0], pages[1]).save('{}.png'.format(filenum))
                if loud: print('d',pages[0],pages[1])
                pages = pages[2:]
            else:
                singleImage(pages[0]).save('{}.png'.format(filenum))
                if loud: print('s',pages[0])
            filenum += 1
    else: # -single
        for page in pages:
            singleImage(page).save('{}.png'.format(filenum))
            filenum += 1

if __name__ == "__main__":
    main()
