# MapHistPlot
Plot Heatmap from latitude and longtitude using Python.

## Overview

## How to use
### 0. Iitialize
  Apache and MySQL
### 1. Clean data
  p1-ImportCSVToDB.py is used to import raw data in form of .csv file to database. The format of data is shown in table below.
  
ID | latitude | longtitude | speed | date | direction | xx 
--- | --- | --- | --- | --- | --- | ---
int | float | float | float | date | int | int


An example of source file is in the Example folder.

We run function in the following order:
```
p1CreateCSVImport()
```
Create table name "CSVImport" in "test2" database.

```
p2ImportToTable(filePath)
```
Import .csv file from "filePath" to CSVImport table

```
p3CreateTemp()
```
Create table name "temp" in "test2" database to store data after cleaning.

```
p4UpsertTemp(chunk,totalRows)
```
Create table name "temp" in "test2" database to store data after cleaning.

### 2. Export rows to csv file
  p2-splitCSV.py exports data from database into CSV file.
  
```
splitCSV(zoomRange,tile)
```

Read table "temp" from database name "test2" then export data in given zoomRange and tile(x,y). Tile must be in [Google Map tile](http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/) format.
  
The output will be stored in /output/zoomZ/dataZ, where Z is zoomRange. For example, if zoomRange = 10, CSV file will be stored in /output/zoom10/data10.
  
  
### 3. Plot data in to image files
  p3-plotHist2D.py
  
