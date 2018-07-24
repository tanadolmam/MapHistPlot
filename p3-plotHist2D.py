# import numpy as np
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
    
    plt.hist2d(lonList,latList, bins=binSize,cmap=cm, vmin=0, vmax=290,range=[(lt[1],rb[1]),(rb[0],lt[0])])
    plt.axis('equal')
    cur_axes = plt.gca()
    cur_axes.axes.get_xaxis().set_ticks([])
    cur_axes.axes.get_yaxis().set_ticks([])
    # plt.grid(b=True,color='r')
    plt.axis('equal')
    plt.colorbar()
    # if(len(latList)>603):
    if True:
        plt.colorbar()
        plt.savefig(imgName,transparent=True,bbox_inches='tight',dpi=720)
        # plt.show()
        print('saving figure: ',imgName)
    plt.hold(False)
    print(' ')

def plotting(Z,xmin,xmax,ymin,ymax,cm):
    
    #maxspd = getMaxSpeed(dbName,tableName)
    maxspd =  (13.1354, 100.875, 678)
    #lines  = getTotalRows(dbName,tableName)
    lines = 45676614
    chunkSize= 400000
    chunk=int(lines/chunkSize)
    for i in range(xmin,xmax+1):
        for j in range(ymin,ymax+1):
            lt=(tile2lat(j,Z),tile2long(i,Z))
            rb=(tile2lat(j+1,Z),tile2long(i+1,Z))
            filePath   = "output/zoom{0}/data{0}/data_{0}_{1}_{2}.csv".format(Z,str(i),str(j))
            createFolder("output/zoom{0}/raw{0}".format(Z))
            print(filePath)
            # filePath = "../GPSData/clean.csv" if len(sys.argv) <= 1 else sys.argv[1]
            if(os.path.isfile(filePath)):
                count=0
                lonList = [rb[0]]*300
                latList = [lt[1]]*300
                lonList+= [lt[0],lt[0]]
                latList+= [lt[1],rb[1]]
                part=0
                for line in open(filePath):
                    k = (line.split(",")[0],line.split(",")[1],line.split(",")[2])
                    lat=float(k[0])
                    if(lat<rb[0]):
                        print('lat= ',lat,' is out of bound')
                        break

                    lon=float(k[1])
                    if (5.6 <= lat <= 20.5) and (97.3 <= lon <= 105.6):
                        if(lt[1]<=lon<=rb[1]) and (rb[0]<=lat<=lt[0]) and (math.ceil(float(k[2]))<300):

                            count+=1
                            latList += [lat] * math.ceil(float(k[2])+1)
                            lonList += [lon] * math.ceil(float(k[2])+1)
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
                                    # break
                createHist2d(lonList,latList, 720,'output/zoom{2}/raw{2}/test{2}_{0}_{1}_part'.format(i,j,Z)+str(part)+'.png',lt,rb,cm)
                if(part != 0):
                    background = Image.open('output/zoom{2}/raw{2}/test{2}_{0}_{1}_part'.format(i,j,Z)+str(0)+'.png')
                    foreground = Image.open('output/zoom{2}/raw{2}/test{2}_{0}_{1}_part'.format(i,j,Z)+str(part)+'.png')
                    background.paste(foreground, (0, 0), foreground)
                    background.save('output/zoom{2}/raw{2}/test{2}_{0}_{1}_part'.format(i,j,Z)+str(0)+'.png',"PNG")
                    os.remove('output/zoom{2}/raw{2}/test{2}_{0}_{1}_part'.format(i,j,Z)+str(part)+'.png')
                    print("merge part: ",part)
def getRange(imgName):
    im = Image.open(imgName)
    x,y = im.size
    background = Image.new(im.mode, im.size,(0,0,0,255))
    background.paste(im, (0, 0), im)
    bg = Image.new(background.mode, im.size, background.getpixel((0,0)))
    diff = ImageChops.difference(background, bg)
    # diff.show()
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    # print('bbox= ', bbox)
    if(bbox):
        xRange = min(bbox[0]-0,x-bbox[2])
        yRange = min(bbox[1]-0,y-bbox[3])
        #print('xRange= ',xRange,' yRange= ',yRange)
        return (xRange,yRange)
    return(0,0)

def cropImage(Z,xmin,xmax,ymin,ymax):
    
    for j in range(ymin,ymax+1):
        # createHist2d(Z,xmin,j)
        lt=(tile2lat(j,Z),tile2long(xmin,Z))
        rb=(tile2lat(j+1,Z),tile2long(xmin+1,Z))

        lonList = [rb[1],lt[1],rb[1],lt[1]]
        latList = [rb[0],lt[0],lt[0],rb[0]]
        
        createHist2d(lonList,latList, 720,"output/zoom{0}/border_zoom{0}_y{1}.png".format(Z,j),lt,rb,"hsv")
        borderFile = "output/zoom{0}/border_zoom{0}_y{1}.png".format(Z,j)
        xRange,yRange = getRange(borderFile)
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
        os.remove(borderFile)
def zoomOutTile(tile):
    defaultZoomRange = 5
    tile1=(tile[0]*2,tile[1]*2)
    tile2=(tile[0]*2+1,tile[1]*2)
    tile3=(tile[0]*2,tile[1]*2+1)
    tile4=(tile[0]*2+1,tile[1]*2+1)
    return (tile1,tile2,tile3,tile4)
def stitchTile(zoomRange):
    zoomRange,xmin,xmax,ymin,ymax=getTileBound(zoomRange)
    createFolder("output/zoom{0}/temp{0}".format(zoomRange))
    print(zoomRange)

    for i in range(xmin,xmax+1):
        for j in range(ymin,ymax+1):
            blankTile=0
            t= zoomOutTile((i,j))
            print(i,j)
            try:
                tile1=Image.open('output/zoom{0}/temp{0}/'.format(zoomRange+1)+str(zoomRange+1)+'-'+str(t[0][0])+str(t[0][1])+'.png').resize((512,512), Image.ANTIALIAS)   
            except FileNotFoundError:
                tile1 = Image.new('RGBA',(512,512))
                blankTile+=1
            try:
                tile2=Image.open('output/zoom{0}/temp{0}/'.format(zoomRange+1)+str(zoomRange+1)+'-'+str(t[1][0])+str(t[1][1])+'.png').resize((512,512), Image.ANTIALIAS)
            except FileNotFoundError:
                tile2 = Image.new('RGBA',(512,512))
                blankTile+=1
            try:
                tile3=Image.open('output/zoom{0}/temp{0}/'.format(zoomRange+1)+str(zoomRange+1)+'-'+str(t[2][0])+str(t[2][1])+'.png').resize((512,512), Image.ANTIALIAS)
            except FileNotFoundError:
                tile3 = Image.new('RGBA',(512,512))
                blankTile+=1
            try:
                tile4=Image.open('output/zoom{0}/temp{0}/'.format(zoomRange+1)+str(zoomRange+1)+'-'+str(t[3][0])+str(t[3][1])+'.png').resize((512,512), Image.ANTIALIAS)
            except FileNotFoundError:
                tile4 = Image.new('RGBA',(512,512))
                blankTile+=1
            # print('bt = ',blankTile)
            if(blankTile!=4):
            # if tile1 and tile2 and tile3 and tile4:
                (width1, height1) = tile1.size

                result_width  = width1 *2
                result_height = height1 *2

                result = Image.new('RGBA', (result_width, result_height))
                result.paste(im=tile1, box=(0, 0))
                result.paste(im=tile2, box=(width1, 0))
                result.paste(im=tile3, box=(0,height1))
                result.paste(im=tile4, box=(width1,height1))
                # result.show()
                saveFile = 'output/zoom{0}/temp{0}/{0}-{1}{2}.png'.format(zoomRange,i,j)
                result = result.resize((512,512), Image.ANTIALIAS)
                result.save(saveFile)



zoomRange=10
# print(10,799,getTileBound(10)[2],494,getTileBound(10)[4])
cm = mpl.colors.ListedColormap(generateCmap())
# plotting(*getTileBound(zoomRange),cm)
# plotting(10,799,getTileBound(10)[2],getTileBound(10)[3],getTileBound(10)[4],cm)
# cropImage(*getTileBound(zoomRange))

# for i in range(zoomRange-1,1,-1):
#     stitchTile(i)
for i in range(zoomRange-1,1,-1):
    bgColor(i,130)
    retouch(i,brightness=(21-i)*1.25**(21-i))
# bgColor(zoomRange,130)

