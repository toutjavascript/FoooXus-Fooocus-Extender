import os
import glob
from PIL import Image


def formatBytes(B, round_to=2):
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2) # 1,048,576
    GB = float(KB ** 3) # 1,073,741,824
    TB = float(KB ** 4) # 1,099,511,627,776

    if B < KB:
        return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        return "{0:.2f} KB".format(B/KB)
    elif MB <= B < GB:
        return "{0:.2f} MB".format(B/MB)
    elif GB <= B < TB:
        return "{0:.2f} GB".format(B/GB)
    elif TB <= B:
        return "{0:.2f} TB".format(B/TB)
    

def formatFrequencies(H, round_to=1):
    H = float(H)
    KH = float(1000)
    MH = float(KH ** 2) # 1,048,576
    GH = float(KH ** 3) # 1,073,741,824
    TH = float(KH ** 4) # 1,099,511,627,776

    if H < KH:
        return '{0} {1}'.format(H,'Hz' if 0 == H > 1 else 'Hz')
    elif KH <= H < MH:
        return "{0:.2f} KHz".format(H/KH)
    elif MH <= H < GH:
        return "{0:.2f} MHz".format(H/MH)
    elif GH <= H < TH:
        return "{0:.2f} GHz".format(H/GH)

# create a folder if it doesn't exist    
def checkFolder(directory):
    if not os.path.exists(directory):
        print("Creating directory: " + directory)
        os.makedirs(directory)

# resize and compress an image 
def resizeAndCompressImage(imageSource, width, height, quality, imageDestination):
    img = Image.open(imageSource)
    img.thumbnail((width, height), Image.LANCZOS)
    img.save(imageDestination, optimize=True, quality=quality)
    return True


def getFiles(dir, extension):
    if extension[0]==".":
        extension=extension[1:]
    files = glob.glob(os.path.join(dir,"*." + extension))
    for i in range(len(files)):
        files[i] = files[i].replace(dir+'\\', "")
    return files