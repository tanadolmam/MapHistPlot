import argparse
parser = argparse.ArgumentParser()
parser.add_argument("csvPath", help="(string) Directory of a source csv file")
args = parser.parse_args()

import pymysql as m
import csv,math,os
import sys
from numpy import genfromtxt


def getTotalRows():					# Count table 'CSVImport' rows
    print('\ngetTotalRows')
    try:
        c = m.connect(host='localhost', user='root', passwd='', db='test2')
        cur = c.cursor()  
        cur.execute('SET NAMES utf8;')
        cur.execute("SELECT VERSION()")
        sql = "SELECT COUNT(*) FROM CSVImport"
        sql = sql.encode('utf-8')
        try:
            cur.execute(sql)
            re = cur.fetchall()
            for row in re:
                totalRows=row[0]
            
        except m.InternalError as error:
            c.rollback()
            print('>>> get total row fail!!')
            print('>>> error : ',error)

    except m.Error:
        print('>>> Failed to Connect to Database')

    if c:
        c.close()
    print('>>> totalRows = ',totalRows)
    return totalRows
    
def p1CreateCSVImport():			# Create table 'CSVImport'
    print('Creating table "CSVImport"')
    try:
        c = m.connect(host='localhost', user='root', passwd='', db='test2')
        cur = c.cursor()  
        cur.execute('SET NAMES utf8;')
        cur.execute("SELECT VERSION()")
        sql = "CREATE TABLE CSVImport (id INT(10) UNSIGNED ,lat double NOT NULL,lon double NOT NULL,spd float(10) NOT NULL,date DATE,direction INT(10) UNSIGNED ,xx INT(5) UNSIGNED,flag INT(5) NOT NULL DEFAULT 1 )"
        sql = sql.encode('utf-8')
        try:
            cur.execute(sql)
            c.commit()

        except m.InternalError as error:
            c.rollback()
            print('>>> create CSVImport fail!!')
            print('>>> error : ',error)

    except m.Error:
        print('>>> Failed to Connect to Database')
        

    if c:
        c.close()

def p2ImportToTable(filePath):			# Import .csv file from filePath to CSVImport table.
    print('\nImporting to table')
    if not (os.path.isfile(filePath)):
        print(">>> Invalid filePath : csv file not found")
    try:
        c = m.connect(host='localhost', user='root', passwd='', db='test2')
        cur = c.cursor()  
        cur.execute('SET NAMES utf8;')
        cur.execute("SELECT VERSION()")
        sql = "LOAD DATA INFILE \"{}\" INTO TABLE CSVImport COLUMNS TERMINATED BY \",\" OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"' LINES TERMINATED BY \"\n\"".format(filePath)
        print('>>> '+sql)
        sql = sql.encode('utf-8')
        
        try:
            cur.execute(sql)
            c.commit()
            
        except m.InternalError as error:
            c.rollback()
            print('>>> Import data fail!!')
            print('>>> error : ',error)

    except m.Error:
        print('>>> Failed to Connect to Database')

    if c:
        c.close()
def p3CreateTemp():					# Create table name "temp" in "test2" database to store data after cleaning.
    print('\nCreating table "temp"')
    try:
        c = m.connect(host='localhost', user='root', passwd='', db='test2')
        cur = c.cursor()  
        cur.execute('SET NAMES utf8;')
        sql = "CREATE TABLE temp LIKE CSVImport;"
        sql = sql.encode('utf-8')
        try:
            cur.execute(sql)
            c.commit()
            try:
                print('>>> Updating temp Pk')
                sql2="ALTER TABLE `temp` ADD PRIMARY KEY( `lat`, `lon`);"		# The primary keys are lat and lon.
                cur.execute(sql2)
                c.commit()
            except m.InternalError as error:
                c.rollback()
                print('>>> Assign Pk fail!!')
                print('>>> error : ',error)
        except m.InternalError as error2:
            c.rollback()
            print('>>> Create temp fail!!')
            print('>>> error : ',error2)

    except m.Error:
        print('>>> Failed to Connect to Database')

    if c:
        c.close()
def p4UpsertTemp(totalRows):			# Insert rows from "CSVImport" to "temp". The duplicate primary key will be recalculate to a new row.
   
    print('\nStart upsert data to temp')
    c = None
    chunkSize=1000000
    chunk = math.ceil(totalRows/chunkSize)
    print('chunk= ',chunk)
    
    try:
        c = m.connect(host='localhost', user='root', passwd='', db='test2')
        cur = c.cursor()  
        cur.execute('SET NAMES utf8;')
        for i in range(chunk+1):
            print(i)
            start=(i*chunkSize)
            print(start)
            if(i==(chunk)):
                chunkSize=(totalRows%chunkSize)
            try:
                sql = "INSERT INTO temp SELECT * FROM csvimport LIMIT {0},{1} ON DUPLICATE KEY UPDATE temp.spd = ((temp.spd*temp.flag)+csvimport.spd)/(temp.flag+1),temp.flag=temp.flag+1".format(start,chunkSize)
                print('>>> '+sql)
                sql = sql.encode('utf-8')
                cur.execute(sql)
                c.commit()
            except m.InternalError as error:
                c.rollback()
                print('>>> cleaning fail, roll back db')
                print('>>> error : ',error)

    except m.Error:
        print('>>> Failed to Connect to Database')
        

    if c:
        c.close()
  
def main(csvPath): 
    p1CreateCSVImport()
    p2ImportToTable(csvPath)
    p3CreateTemp()
    totalRows = getTotalRows()
    p4UpsertTemp(totalRows)
    print('[Done]')
if __name__ == "__main__":
    csvPath = sys.argv[1]
    main(csvPath)
# main("../GPSData/clean.csv")