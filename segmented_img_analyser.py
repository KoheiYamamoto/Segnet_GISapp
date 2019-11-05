from PIL import Image
import numpy as np
import glob
import csv
from datetime import datetime, timedelta, timezone

class PixelSet:
    def __init__(self):
        self.sky = 0
        self.building = 0
        self.pole = 0
        self.pavement = 0
        self.road = 0
        self.tree = 0
        self.signsymbol = 0
        self.fence = 0
        self.car = 0
        self.pedestrian = 0
        self.bicyclist = 0
        self.road_marking = 0
        self.unlabelled = 0

    def getImageArray(self, file):
        # img_pixels[100][0] r
        # img_pixels[100][1] g
        # img_pixels[100][2] b
        img = Image.open(file)
        width, height = img.size
        img_pixels = []
        for y in range(height):
          for x in range(width):
            img_pixels.append(img.getpixel((x,y)))
        img_pixels = np.array(img_pixels)
        return img_pixels

    # Color Palette
        # Sky:> [128,128,128] Gray => Sky
        # Building:> [128,0,0] Dark Red => Building
        # Pole:> [192,192,128] Light Cream => Pole
        # Road_marking:> [255,69,0] Orange => Pavement 
        # Road:> [128,64,128] Dark Pink => Road (not Pavement)
        # Pavement:> [60,40,222] Dark Blue => Tree
        # Tree:> [128,128,0] Ochre Green => SignSymbol
        # SignSymbol:> [192,128,128] Pale Orange => Fence
        # Fence:> [64,64,128] Navy => Car
        # Car:> [64,0,128] Purple => Pedestrian 
        # Pedestrian:> [64,64,0] Dirty Green => Bicyclist
        # Bicyclist:> [0,128,192] Light Blue => Road_marking ??? (sceptical)
        # Unlabelled:> [0,0,0] Black => Unlabelled
    def analyseClass(self, pixels, instance):
        for pixel in pixels:
            if pixel[0] == 128 and pixel[1] == 128 and pixel[2] == 128:
                instance.sky += 1
            elif pixel[0] == 128 and pixel[1] == 0 and pixel[2] == 0:
                instance.building += 1
            elif pixel[0] == 192 and pixel[1] == 192 and pixel[2] == 128:
                instance.pole += 1
            elif pixel[0] == 255 and pixel[1] == 69 and pixel[2] == 0:
                instance.pavement += 1
            elif pixel[0] == 128 and pixel[1] == 64 and pixel[2] == 128:
                instance.road += 1
            elif pixel[0] == 60 and pixel[1] == 40 and pixel[2] == 222:
                instance.tree += 1
            elif pixel[0] == 128 and pixel[1] == 128 and pixel[2] == 0:
                instance.signsymbol += 1
            elif pixel[0] == 192 and pixel[1] == 128 and pixel[2] == 128:
                instance.fence += 1
            elif pixel[0] == 64 and pixel[1] == 64 and pixel[2] == 128:
                instance.car += 1
            elif pixel[0] == 64 and pixel[1] == 0 and pixel[2] == 128:
                instance.pedestrian += 1
            elif pixel[0] == 64 and pixel[1] == 64 and pixel[2] == 0:
                instance.bicyclist += 1
            elif pixel[0] == 0 and pixel[1] == 128 and pixel[2] == 192:
                instance.road_marking += 1
            else:
                instance.unlabelled += 1

    def parseFilename(self, path):
        s = path.lstrip('./out/').rstrip('_out.png').split('_')
        return s[0], s[1], s[2]

    def Addout2CSV(self, la, ln, de, insta):
        with open('pixel_parsed_report.csv', 'a') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({'lat': la, 'long': ln, 'degree': de, 'sky': insta.sky, 'building': insta.building, 'pole': insta.pole, 'pavement': insta.pavement, 'road': insta.road, 'tree': insta.tree, 'signsymbol': insta.signsymbol, 'fence': insta.fence, 'car': insta.car, 'pedestrian': insta.pedestrian, 'bicyclist': insta.bicyclist, 'road_marking': insta.road_marking, 'unlabelled': insta.unlabelled})

path2dir = './out/'
fieldnames = ['lat', 'long', 'degree', 'sky', 'building', 'pole', 'pavement', 'road', 'tree', 'signsymbol', 'fence', 'car', 'pedestrian', 'bicyclist', 'road_marking', 'unlabelled']
def makeCSV():
    with open('pixel_parsed_report.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

def getfilenames():
    paths = glob.glob(path2dir + '*')
    names = []
    for path in paths:
        names.append(path)
    return names

def main():
    starttime = datetime.now(timezone(timedelta(hours=+8)))
    
    makeCSV()
    files = getfilenames() # Get all the image paths
    for file in files:
        print("Analysing image: ", files.index(file)+1, '/', len(files))
        p_instance = PixelSet() # Constractor
        pixeled = p_instance.getImageArray(file) # Pixel arr of an image    
        p_instance.analyseClass(pixeled, p_instance) # Assign pixel to each class
        lat, lng, deg = p_instance.parseFilename(file) # parse filename
        p_instance.Addout2CSV(lat, lng, deg, p_instance) # Write out to csv 
    
    print('start time: ', starttime)
    print('  end time: ', datetime.now(timezone(timedelta(hours=+8))))

if __name__ == '__main__':
    main()