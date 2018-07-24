
import csv
import sys,math
from lib.pathCheck import createFolder
from lib.mapTool import *
# def tile2long(x,z) :
#     #return min longtitude of a tile x
#     return (x/math.pow(2,z)*360-180)

# def tile2lat(y,z) :
#     #return min latitude of a tile y
#     n=math.pi-2*math.pi*y/math.pow(2,z);
#     return (180/math.pi*math.atan(0.5*(math.exp(n)-math.exp(-n))))

# def getTileBound(zoomRange):
#     minZoomRange=20
#     xmin = math.floor(807815/(2**(minZoomRange-zoomRange)))
#     xmax = math.floor(831941/(2**(minZoomRange-zoomRange)))
#     ymin = math.floor(463368/(2**(minZoomRange-zoomRange)))
#     ymax = math.floor(507913/(2**(minZoomRange-zoomRange)))
#     return (zoomRange,xmin,xmax,ymin,ymax)

def splitCSV(zoomRange,tile):
    print('splitCSV ',zoomRange,tile)

    lt=(tile2lat(tile[1],zoomRange),tile2long(tile[0],zoomRange))
    rb=(tile2lat(tile[1]+1,zoomRange),tile2long(tile[0]+1,zoomRange))
    outputFile   = "C:/Workspace/mm/gisToHist2d/plotHeatmap/output/zoom{0}/data{0}/data_{0}_{1}_{2}.csv".format(zoomRange,tile[0],tile[1])
    createFolder("C:/Workspace/mm/gisToHist2d/plotHeatmap/output/zoom{0}/data{0}".format(zoomRange))
    try:
        c = m.connect(host='localhost', user='root', passwd='', db='test2')
        cur = c.cursor()  
        cur.execute('SET NAMES utf8;')
        cur.execute("SELECT VERSION()")
        sql = "SELECT lat,lon,spd FROM temp WHERE (lat BETWEEN {1} AND {2}) AND (lon BETWEEN {3} AND {4}) INTO OUTFILE \"{0}\" FIELDS TERMINATED BY \",\" LINES TERMINATED BY \"\n\"".format(outputFile,rb[0],lt[0],lt[1],rb[1])
        print(sql)
        sql = sql.encode('utf-8')

        try:
            cur.execute(sql)
            c.commit()

        except:
            c.rollback()
            print('splitCSV fail!!')

    except m.Error:
        print('Failed to Connect to Database')
        

    if c:
        c.close()


zoomRange,xmin,xmax,ymin,ymax = getTileBound(3)
for x in range(xmin,xmax+1):
    for y in range(ymin,ymax+1):
        splitCSV(zoomRange,(x,y))