import pymysql as m
import numpy as np
import csv,math
import sys
from numpy import genfromtxt


def getTotalRows():
    print('get total row')
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
            
        except:
            c.rollback()
            print('get total row fail!!')

    except m.Error:
        print('Failed to Connect to Database')

    if c:
        c.close()
    print('totalRows = ',totalRows)
    return totalRows
    
def p1CreateCSVImport():
    print('Creating CSVImport')
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

        except:
            c.rollback()
            print('create CSVImport fail!!')

    except m.Error:
        print('Failed to Connect to Database')
        

    if c:
        c.close()
def p2ImportToTable(filePath):
    print('Importing to table')
    try:
        c = m.connect(host='localhost', user='root', passwd='', db='test2')
        cur = c.cursor()  
        cur.execute('SET NAMES utf8;')
        cur.execute("SELECT VERSION()")
        sql = "LOAD DATA INFILE \"{}}\" INTO TABLE CSVImport COLUMNS TERMINATED BY \",\" OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"' LINES TERMINATED BY \"\n\"".format(filePath)
        sql = sql.encode('utf-8')
        
        try:
            cur.execute(sql)
            c.commit()
            
        except:
            c.rollback()
            print('Import data fail!!')

    except m.Error:
        print('Failed to Connect to Database')

    if c:
        c.close()
def p3CreateTemp():
    print('Creating table temp')
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
                print('Updating temp Pk')
                sql2="ALTER TABLE `temp` ADD PRIMARY KEY( `lat`, `lon`);"
                cur.execute(sql2)
                c.commit()
            except:
                c.rollback()
                print('Assign Pk fail!!')
        except:
            c.rollback()
            print('Create temp fail!!')

    except m.Error:
        print('Failed to Connect to Database')

    if c:
        c.close()
def p4UpsertTemp(chunk,totalRows):
    print('Start upsert data to temp')
    c = None
    #chunkSize=10**( int( math.log10(totalRows/chunk) ) )
    chunkSize=1000000
    
    try:
        c = m.connect(host='localhost', user='root', passwd='', db='test2')
        cur = c.cursor()  
        cur.execute('SET NAMES utf8;')
        for i in range(31,chunk+1):
            print(i)
            start=(i*chunkSize)
            print(start)
            if(i==(chunk)):
                chunkSize=(totalRows%chunkSize)
                print(chunkSize)
            try:
                sql = "INSERT INTO temp SELECT * FROM csvimport LIMIT {0},{1} ON DUPLICATE KEY UPDATE temp.spd = ((temp.spd*temp.flag)+csvimport.spd)/(temp.flag+1),temp.flag=temp.flag+1".format(start,chunkSize)
                print(sql)
                sql = sql.encode('utf-8')
                cur.execute(sql)
                c.commit()
            except:
                c.rollback()
                print('cleaning fail, roll back db')

    except m.Error:
        print('Failed to Connect to Database')
        

    if c:
        c.close()
  
#main
chunk = 54
p1CreateCSVImport()
p2ImportToTable("full_mappoint.csv")
p3CreateTemp()
totalRows = getTotalRows()
p4UpsertTemp(chunk,totalRows)

