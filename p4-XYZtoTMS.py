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

import os,math,shutil,sys
from lib.mapTool import getTileBound
from PIL import Image

def clearDirectory(folder): 				# clear the folder if it is not empty
	print('clear ',folder)
	if os.listdir(folder):
		for the_file in os.listdir(folder):
		    file_path = os.path.join(folder, the_file)
		    try:
		        if os.path.isfile(file_path):
		            os.unlink(file_path)
		        elif os.path.isdir(file_path): shutil.rmtree(file_path)
		    except Exception as e:
		        print(55)


def toTMS(zoom,xmin,xmax,ymin,ymax,mode,opacity=130):
	print(zoom)
	extraTile = 13-zoom				#Draw extra blank tiles to fill the missing tiles.
	if(extraTile>0):
		xmin-=extraTile
		xmax+=extraTile
		ymin-=extraTile
		ymax+=extraTile
	im = Image.new('RGBA',(512,512),(0,0,0,opacity))
	for i in range(xmin,xmax+1):
		for j in range(ymin,ymax+1):
			yTMS = (2 ** zoom)-j-1
			src = "output/zoom{0}/{0}-{1}{2}.png".format(zoom,i,j)		# source png file
			dst = "TMSimage{3}/{0}/{1}/{2}.png".format(zoom-1,i,yTMS,mode)		# new TMS png file

			if not (os.path.exists("TMSimage{2}/{0}/{1}".format(zoom-1,i,mode))):
				os.makedirs("TMSimage{2}/{0}/{1}".format(zoom-1,i,mode))
			
			if(os.path.isfile(src)):
				shutil.copy(src, dst) 
			else:
				im.save(dst)			#Draw extra blank if not exists.


def main(mode,minZoomRange=0,maxZoomRange=20,opacity=130):
	for i in range(maxZoomRange,minZoomRange-1,-1):
		toTMS(*getTileBound(i),mode,opacity)
	print('[Done]')


if __name__ == "__main__":
    mode = str(m)
    minZoomRange = int(x)
    maxZoomRange = int(y)
    opacity = int(z)
    main(mode,minZoomRange,maxZoomRange,opacity) 

# main("density",5,10,170)