import argparse
parser = argparse.ArgumentParser()
parser.add_argument("zoomRange", help="Export rows within lat,lon range of each tile in a zoomRange into .csv files")
args = parser.parse_args()


import pymysql as m
import sys,math,csv
from lib.pathCheck import createFolder
from lib.mapTool import *

def splitCSV(zoomRange,tile):
    print('splitCSV ',zoomRange,tile)

    lt=(tile2lat(tile[1],zoomRange),tile2long(tile[0],zoomRange))
    rb=(tile2lat(tile[1]+1,zoomRange),tile2long(tile[0]+1,zoomRange))
    curr_directory = dir_path = os.path.dirname(os.path.realpath(__file__))         # get current .py file's directory
    curr_directory = curr_directory.replace('\\', '/')
    print(curr_directory)

    outputFile   = "{3}/output/zoom{0}/data{0}/data_{0}_{1}_{2}.csv".format(zoomRange,tile[0],tile[1],curr_directory)
    createFolder("{1}/output/zoom{0}/data{0}".format(zoomRange,curr_directory))
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

        except m.InternalError as error:
            c.rollback()
            print('splitCSV fail!!')
            print('>>> error : ',error)

    except m.Error as mError:
        print('Failed to Connect to Database')
        print(mError)
        

    if c:
        c.close()

def main(zoomRange):
    zoomRange,xmin,xmax,ymin,ymax = getTileBound(zoomRange)
    for x in range(xmin,xmax+1):
        for y in range(ymin,ymax+1):
            splitCSV(zoomRange,(x,y))
    print('[Done]')

if __name__ == "__main__":
    zoomRange = int(sys.argv[1])
    main(zoomRange) 
# main(3)