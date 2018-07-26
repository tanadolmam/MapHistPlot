# MapHistPlot
Plot Heatmap from latitude and longtitude using Python. Then make it work with Tile Map Service. It also has option between speed and density.

## Overview
  To draw a heatmap, it requires several programs. I divide them it to 4 parts:
  
![alt text](https://raw.githubusercontent.com/tanadolmam/MapHistPlot/master/images/workflow.png)



 1. Clean data
  
    This method handles duplicate latitude,longtitude points using MySQL.
  
 2. Divide data into small pieces
  
    Sometimes, data is too large to load into memory at once. We should split them into chunks and process one by one. Remind that we need to normallize them to make color looks smooth.
  
 3. Process each piece
  
    After we split data, 1 chunk means 1 tile. We plot each tile and crop them to make them fit to map. Then we will have a full heatmap of 1 zoom level. To get the other levels we don't need to clean,split and plot them again. We just stitch four tiles as one and recursively do this to a lower zoom level. 
    
_Note that you cannot use this method to a higher zoom level._
  
 4. Arrange the output
  
    This method is required if we use TMS. It will modify file's name and location to the correct form.
  
  


## How to use
Firstly, install the following modules:
[PyMySQL](https://github.com/PyMySQL/PyMySQL),
[NumPy](https://github.com/numpy/numpy),
[Matplotlib](https://github.com/matplotlib/matplotlib) and 
[Pillow](https://github.com/python-pillow/Pillow).



### Windows
1. Create database by Apache, MySQL and name it "test2".
2. Open Command Prompt
3. Change directory to your python directory  `cd C:\Users\user\Documents\GitHub`

4. Run each file in order:

Example of plotting heatmap from zoomRange 6 to 12

`python p1-importToDB.py "/Users/user/Documents/GitHub/MapHistPlot/GPSData/mappoint.csv"` --> Clean data and import them to database.

`python p2-splitCSV.py --zoom 12`  --> Create csv for each tile where zoomRange=12.

`python p3-plotHist2d.py --min 6 --max 12 --opacity 130 --mode "speed"` --> Draw heatmap of zoomRange=12 then recursively stitch them to make heatmap for zoom level 6-11 descending.

`python p4-XYZtoTMS.py --min 6 --max 12 --opacity 130 --mode "speed"`  --> Arrange images in zoomRange 6 to 12 in the correct format.


5. Open __mymap.html__ to see the result. Learn more about [Longdo Map API](https://map.longdo.com/longdo-map-api).



## Documentation

### p1-ImportToDB.py

* `--csvPath:string` - location of raw CSV file
 
  Import raw data in format of .csv file to database. The form of data is shown in table below.
  
ID | latitude | longtitude | speed | date | direction | xx 
--- | --- | --- | --- | --- | --- | ---
int | float | float | float | date | int | int


An example of source file is in the "GPSData" folder.


```
p1CreateCSVImport()
```
Create table name "CSVImport" in "test2" database.

```
p2ImportToTable(filePath)
```
* `filePath:string` - location of raw CSV file

Import .csv file from `filePath` to CSVImport table. The [uploading size limit](https://stackoverflow.com/questions/3958615/import-file-size-limit-in-phpmyadmin) may cause an error.


```
p3CreateTemp()
```
Create table name "temp" in "test2" database to store data after cleaning. The primary keys are `lat` and `lon`.


```
getTotalRows()
```
Return total count of row of table "CSVImport" in database "test2".


```
p4UpsertTemp(totalRows)
```
* `chunkSize:int` - limit of reading rows
* `totalRows:int` - total rows of raw CSV file

Insert rows from "CSVImport" to "temp". The duplicate primary key will be recalculate to a new row.




### p2-splitCSV.py

* `--zoom:int` - Range of zoom

   Export data from database into CSV file.
  
```
splitCSV(zoomRange,tile)
```

Read table "temp" from database name "test2" then export data in given `zoomRange` and `tile`(x,y). Tile must be in [Google Map tile](http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/) format.
  
The output will be stored in "/output/zoomZ/dataZ", where Z is `zoomRange`. For example, if `zoomRange = 10`, CSV file will be stored in "/output/zoom10/data10".
  
  
### p3-plotHist2D.py

* `--minZoomRange:int` - minimunm range of zoom
* `--maxZoomRange:int` - maximunm range of zoom
* `--mode:string` - "speed" or "density"
* `--opacity:int` - opacity of background image(between 0-255)

   Plot data into 512x512 PNG files. The format can be use in Google Map Overlay an Longdo Map Layer.
  
```
generateCmap()
```
Return hot array colormap but first 
nt(minimum value) will be transparent. 

```
plotting(zoomRange,xmin,xmax,ymin,ymax,colorMap)
```
* `zoomRange:int` - Range of zoom
* `xmin:int` - most left value of x axis in map tile system
* `xmax:int` - most right value of x axiss in map tile system
* `ymin:int` - top value of y axis in map tile system
* `ymax:int` - bottom value of y axis in map tile system
* `colorMap:list` - list of 4-tuples in format of (R,G,B,A)

Read CSV file from "output/zoomZ/dataZ" and store in 2 lists, __latitude__ and __longtitude__. This function will append point to a list equal to __speed__ of that point.
For example, if (lat,lon,spd) = (10.3,15.2,120). The __latitude__ list will append 10.2 equal to 120 times.
After this function read 500,000 rows of data or read to the end of csv soruce file, it will call `createHist2d(...)`.

```
createHist2d(lonList,latList, binSize,imgName,lt,rb,cm)
```
* `latList:float` - array of latitude
* `lonList:float` - array of longtitude
* `binSize:int` - matplotlib.pyplot.hist2d bins
* `imgName:string` - output file name(need .png at the end)
* `lt:(float,float)` - (lat,lon) of left top point of a bound
* `rb:(float,float)` - (lat,lon) of bottom right point of a bound
* `cm:list` - list of 4-tuples in format of (R,G,B,A)

Draw 2D histogram on canvas size equal to `lt` and `rb` bound and save to `imgName`.
  
```
cropImage(zoomRange,xmin,xmax,ymin,ymax)
```
* `zoomRange:int` - Range of zoom
* `xmin:int` - most left value of x axis in map tile system
* `xmax:int` - most right value of x axiss in map tile system
* `ymin:int` - top value of y axis in map tile system
* `ymax:int` - bottom value of y axis in map tile system

Create template images for cropping and trim all images in `zoomRange` using bounding box range from `getRange()`.

```
getRange(zoomRange,x,y)
```
* `zoomRange:int` - Range of zoom
* `x:int` - x coordinate for reference tile (template image)
* `y:int` - y coordinate for reference tile (template image)

Return ranges of x axis and y axis in pixel .These ranges will be used for cropping other images.

```
stitchTile(zoomRange)
```
* `zoomRange:int` - Range of zoom

Create a new tile in given `zoomRange` by stitching 4 tiles(images) from `zoomRange+1` as one.


### p4-XYZtoTMS.py

* `--minZoomRange:int` - minimunm range of zoom
* `--maxZoomRange:int` - maximunm range of zoom
* `--mode:string` - "speed" or "density"
* `--opacity:int` - background opacity of border image(between 0-255)

   Change file's name and organize them in Tile Map Service format.
  
```
toTMS(zoomRange,xmin,xmax,ymin,ymax)
```
* `zoomRange:int` - Range of zoom
* `xmin:int` - most left value of x axis in map tile system
* `xmax:int` - most right value of x axiss in map tile system
* `ymin:int` - top value of y axis in map tile system
* `ymax:int` - bottom value of y axis in map tile system

Organize files to make them work with Longdo Map API(TMS).


### Extra
  These files are used as library, they locate in lib folder.
  1. pathCheck.py
```
createFolder(filePath)
```
* `filePath:string` - Location for new folder

Check for `filePath`, if not exist, create it.
 
 
 2. mapTool.py
```
tile2long(x,z) 
```
* `x:int` - x coordinate of a tile
* `z:int` - zoomRange

Return a minimum longtitude of all tiles in `x` axis.

```
tile2lat(y,z) 
```
* `y:int` - y coordinate of a tile
* `z:int` - zoomRange

Return a minimum latitude of all tiles in `y` axis.

```
getTileBound(zoomRange) 
```
* `zoomRange:int` - Range of zoom

Return bouding coordinate (x,y) of all tiles those cover Thailand, the output has 5 parameters. (`zoomRange`,`xmin`,`xmax`,`ymin`,`ymax`).

```
bgColor(zoomRange,opacity) 
```
* `zoomRange:int` - Range of zoom
* `opacity:int` - opacity of background (integer between 0-255), default=130

Fill image background with black.

```
retouch(zoomRange,brightness,contrast,color,sharpness) 
```
* `zoomRange:int` - Range of zoom
* `brightness:int` - adjust brightness of an image
* `contrast:int` - adjust contrast of an image
* `color:int` - adjust color of an image
* `sharpness:int` - adjust sharpness of an image

More information about [ImageEnhance](https://pillow.readthedocs.io/en/3.0.x/reference/ImageEnhance.html).

## References

<https://www.strava.com/heatmap>

<http://www.maptiler.org/google-maps-coordinates-tile-bounds-projection/>

<https://medium.com/strava-engineering/the-global-heatmap-now-6x-hotter-23fc01d301de>

<http://api.longdo.com/map/doc/>




