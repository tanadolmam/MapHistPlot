import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--mode", nargs=1,  dest="arg0" , help="'speed' or 'density'")
parser.add_argument("--min", nargs=1,  dest="arg1" , help="Minimum zoomRange to plot(default =  0)")
parser.add_argument("--max", nargs=1,  dest="arg2" , help="Maximum zoomRange to plot(default = 20)")
parser.add_argument("--opacity", nargs=1,  dest="arg3" , help="Opacity of background[0-255] (default = 130)")
args = parser.parse_args()

m=args.arg0[0]
x=args.arg1[0]
y=args.arg2[0]
z=args.arg3[0]


import csv,os
import sys,math
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image,ImageChops
from matplotlib.colors import LinearSegmentedColormap
from lib.mapTool import *
from lib.pathCheck import createFolder


def generateCmap():
    rgba=[] 
    cmap = plt.cm.get_cmap('hot')
    for i in range(290):
        rgba.append(cmap(i/290))
    rgba=rgba[30:]
    rgba[0] = (0, 0, 0,0)
    return rgba


def createHist2d(lonList,latList, binSize,imgName,lt,rb,cm):
    print('plotting...')
    print(len(latList))
    plt.subplots_adjust(0.05, 0.05, 1.05, 0.95)
    plt.axis('equal')
    
    plt.hist2d(lonList,latList, bins=binSize,cmap=cm, vmin=0, vmax=290,range=[(lt[1],rb[1]),(rb[0],lt[0])])     #color scale can be change by value of vmin,vmax
    plt.axis('equal')
    cur_axes = plt.gca()
    cur_axes.axes.get_xaxis().set_ticks([])
    cur_axes.axes.get_yaxis().set_ticks([])
    plt.axis('equal')

    plt.savefig(imgName,transparent=True,bbox_inches='tight',dpi=720)
    print('saving figure: ',imgName)
    plt.hold(False)
    print(' ')

def plotting(Z,xmin,xmax,ymin,ymax,cm,mode):

    # chunkSize = number of rows for plotting 1 image
    # if 1 tile contain more than 400,000 rows(lat,lon pairs), it will plot and merge as layer to previous image
    chunkSize= 400000                        
    for i in range(xmin,xmax+1):
        for j in range(ymin,ymax+1):
            lt=(tile2lat(j,Z),tile2long(i,Z))
            rb=(tile2lat(j+1,Z),tile2long(i+1,Z))
            filePath   = "output/zoom{0}/data{0}/data_{0}_{1}_{2}.csv".format(Z,str(i),str(j))
            createFolder("output/zoom{0}/raw{0}".format(Z))
            print(filePath)
            if(os.path.isfile(filePath)):
                count=0
                lonList = [rb[0]]*300
                latList = [lt[1]]*300
                lonList+= [lt[0],lt[0]]
                latList+= [lt[1],rb[1]]
                part=0
                for line in open(filePath):
                    k = (line.split(",")[0],line.split(",")[1])
                    # print(mode)
                    if(mode == "speed"):
                        spd=float(line.split(",")[2])
                    elif(mode == "density"):
                        spd=float(line.split(",")[3])
                    lat=float(k[0])
                    if(lat<rb[0]):
                        print('lat= ',lat,' is out of bound')
                        break

                    lon=float(k[1])
                    if (5.6 <= lat <= 20.5) and (97.3 <= lon <= 105.6):
                        if(lt[1]<=lon<=rb[1]) and (rb[0]<=lat<=lt[0]) and (math.ceil(spd)<300):

                            count+=1
                            latList += [lat] * math.ceil(float(spd)+1)
                            lonList += [lon] * math.ceil(float(spd)+1)
                            if(count%chunkSize==0):
                                print('n=',i,j)

                                createHist2d(lonList,latList, 720,'output/zoom{2}/raw{2}/test{2}_{0}_{1}_part'.format(i,j,Z)+str(part)+'.png',lt,rb,cm)
                                if(part != 0):
                                    background = Image.open('output/zoom{2}/raw{2}/test{2}_{0}_{1}_part'.format(i,j,Z)+str(0)+'.png')
                                    foreground = Image.open('output/zoom{2}/raw{2}/test{2}_{0}_{1}_part'.format(i,j,Z)+str(part)+'.png')
                                    background.paste(foreground, (0, 0), foreground)
                                    background.save('output/zoom{2}/raw{2}/test{2}_{0}_{1}_part'.format(i,j,Z)+str(0)+'.png',"PNG")
                                    os.remove('output/zoom{2}/raw{2}/test{2}_{0}_{1}_part'.format(i,j,Z)+str(part)+'.png')
                                    print("merge part: ",part)
                                latList = [lt[0],lt[0],rb[0],rb[0]]
                                lonList = [lt[1],rb[1],lt[1],rb[1]]
                                part+=1
                createHist2d(lonList,latList, 720,'output/zoom{2}/raw{2}/test{2}_{0}_{1}_part'.format(i,j,Z)+str(part)+'.png',lt,rb,cm)
                if(part != 0):
                    background = Image.open('output/zoom{2}/raw{2}/test{2}_{0}_{1}_part'.format(i,j,Z)+str(0)+'.png')
                    foreground = Image.open('output/zoom{2}/raw{2}/test{2}_{0}_{1}_part'.format(i,j,Z)+str(part)+'.png')
                    background.paste(foreground, (0, 0), foreground)
                    background.save('output/zoom{2}/raw{2}/test{2}_{0}_{1}_part'.format(i,j,Z)+str(0)+'.png',"PNG")
                    os.remove('output/zoom{2}/raw{2}/test{2}_{0}_{1}_part'.format(i,j,Z)+str(part)+'.png')
                    print("merge part: ",part)

def getRange(Z,x,y):
    
    lt=(tile2lat(y,Z),tile2long(x,Z))
    rb=(tile2lat(y+1,Z),tile2long(x+1,Z))

    lonList = [rb[1],lt[1],rb[1],lt[1]]
    latList = [rb[0],lt[0],lt[0],rb[0]]
    imgName = "output/zoom{0}/border_zoom{0}_y{1}.png".format(Z,y)
    createHist2d(lonList,latList, 720,imgName,lt,rb,"hsv")              # create new image as a mold for precise cropping range
    im = Image.open(imgName)
    x,y = im.size
    background = Image.new(im.mode, im.size,(0,0,0,255))
    background.paste(im, (0, 0), im)
    bg = Image.new(background.mode, im.size, background.getpixel((0,0)))
    diff = ImageChops.difference(background, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    os.remove(imgName)
    if(bbox):
        xRange = min(bbox[0]-0,x-bbox[2])
        yRange = min(bbox[1]-0,y-bbox[3])
        return (xRange,yRange)
    return(0,0)


def cropImage(Z,xmin,xmax,ymin,ymax):
    createFolder("output/zoom{0}/temp{0}".format(Z))
    for j in range(ymin,ymax+1):
        
        xRange,yRange = getRange(Z,xmin,j)
        print(j,'/',ymax,'---',xRange,yRange)
        for i in range(xmin,xmax+1):
            count=j
            imgName  = "output/zoom{0}/raw{0}/test{0}_{1}_{2}_part0.png".format(Z,str(i), str(j))        
            saveFile = "output/zoom{0}/temp{0}/{0}-{1}.png".format(Z,str(i)+str(j))
            print(imgName)
            if(os.path.isfile(imgName)):
                im = Image.open(imgName)
                x,y=im.size
                if(xRange and yRange):
                    x=im.crop((xRange,yRange,x-xRange,y-yRange))
                    x=x.resize((512,512), Image.ANTIALIAS)
                    x.save(saveFile)
        
def zoomOutTile(tile):              # return tile numbers which required for stitching a new tile
    defaultZoomRange = 5
    tile1=(tile[0]*2,tile[1]*2)
    tile2=(tile[0]*2+1,tile[1]*2)
    tile3=(tile[0]*2,tile[1]*2+1)
    tile4=(tile[0]*2+1,tile[1]*2+1)
    return (tile1,tile2,tile3,tile4)

def stitchTile(zoomRange):
    print('stitchTile(',zoomRange,')')
    zoomRange,xmin,xmax,ymin,ymax=getTileBound(zoomRange)
    createFolder("output/zoom{0}/temp{0}".format(zoomRange))

    for i in range(xmin,xmax+1):
        for j in range(ymin,ymax+1):
            t= zoomOutTile((i,j))
            try:
                tile1=Image.open('output/zoom{0}/temp{0}/'.format(zoomRange+1)+str(zoomRange+1)+'-'+str(t[0][0])+str(t[0][1])+'.png').resize((512,512), Image.ANTIALIAS)   
            except FileNotFoundError:
                tile1 = Image.new('RGBA',(512,512))
            try:
                tile2=Image.open('output/zoom{0}/temp{0}/'.format(zoomRange+1)+str(zoomRange+1)+'-'+str(t[1][0])+str(t[1][1])+'.png').resize((512,512), Image.ANTIALIAS)
            except FileNotFoundError:
                tile2 = Image.new('RGBA',(512,512))
            try:
                tile3=Image.open('output/zoom{0}/temp{0}/'.format(zoomRange+1)+str(zoomRange+1)+'-'+str(t[2][0])+str(t[2][1])+'.png').resize((512,512), Image.ANTIALIAS)
            except FileNotFoundError:
                tile3 = Image.new('RGBA',(512,512))
            try:
                tile4=Image.open('output/zoom{0}/temp{0}/'.format(zoomRange+1)+str(zoomRange+1)+'-'+str(t[3][0])+str(t[3][1])+'.png').resize((512,512), Image.ANTIALIAS)
            except FileNotFoundError:
                tile4 = Image.new('RGBA',(512,512))

            
            (width1, height1) = tile1.size

            result_width  = width1 *2
            result_height = height1 *2

            result = Image.new('RGBA', (result_width, result_height))
            result.paste(im=tile1, box=(0, 0))
            result.paste(im=tile2, box=(width1, 0))
            result.paste(im=tile3, box=(0,height1))
            result.paste(im=tile4, box=(width1,height1))

            saveFile = 'output/zoom{0}/temp{0}/{0}-{1}{2}.png'.format(zoomRange,i,j)
            result = result.resize((512,512), Image.ANTIALIAS)
            result.save(saveFile)


def main(mode,minZoomRange=0,maxZoomRange=20,opacity=130):
    print(mode)
    cm = mpl.colors.ListedColormap(generateCmap())
    plotting(*getTileBound(maxZoomRange),cm,mode)
    cropImage(*getTileBound(maxZoomRange))
    for i in range(maxZoomRange-1,minZoomRange-1,-1):
        stitchTile(i)
    for i in range(maxZoomRange,minZoomRange-1,-1):
        bgColor(i,opacity)
        retouch(i,brightness=(21-i)*1.5)
    bgColor(maxZoomRange,opacity)
    retouch(maxZoomRange,brightness=(21-10)*1.5)
    print('[Done]')


if __name__ == "__main__":
    mode = str(m)
    print(m)
    minZoomRange = int(x)
    maxZoomRange = int(y)
    opacity = int(z)
    main(mode,minZoomRange,maxZoomRange,opacity) 


# main("density",5,10,170)