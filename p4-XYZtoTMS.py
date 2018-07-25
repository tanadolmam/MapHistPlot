import argparse
parser = argparse.ArgumentParser()
parser.add_argument("minZoomRange", help="Minimum zoomRange to plot(default =  0)")
parser.add_argument("maxZoomRange", help="Maximum zoomRange to plot(default = 20)")
args = parser.parse_args()


import os,math,shutil,sys
from lib.mapTool import getTileBound
from PIL import Image

def clearDirectory(folder):
	print('clear ',folder)
	if os.listdir(folder):
		for the_file in os.listdir(folder):
		    file_path = os.path.join(folder, the_file)
		    # print(the_file)
		    try:
		        if os.path.isfile(file_path):
		            os.unlink(file_path)
		        elif os.path.isdir(file_path): shutil.rmtree(file_path)
		    except Exception as e:
		        print(55)
def toTMS(zoom,xmin,xmax,ymin,ymax,opacity=130):
	print(zoom)
	extraTile = 13-zoom				#Draw extra blank tiles to fill the missing tiles.
	if(extraTile>0):
		xmin-=extraTile
		xmax+=extraTile
		ymin-=extraTile
		ymax+=extraTile
	# print(xmin,xmax,ymin,ymax)
	im = Image.new('RGBA',(512,512),(0,0,0,opacity))
	# im.show()
	# clearDirectory('TMSimage/{}'.format(zoom-1))
	for i in range(xmin,xmax+1):
		for j in range(ymin,ymax+1):
			yTMS = (2 ** zoom)-j-1
			src = "output/zoom{0}/{0}-{1}{2}.png".format(zoom,i,j)

			dst = "TMSimage/{0}/{1}/{2}.png".format(zoom-1,i,yTMS)

			if not (os.path.exists("TMSimage/{0}/{1}".format(zoom-1,i,yTMS))):
				os.makedirs("TMSimage/{0}/{1}".format(zoom-1,i,yTMS))
			
			if(os.path.isfile(src)):
				# print(src)
				# os.remove(dst)
				shutil.copy(src, dst) 
				# print("move "+src+" to "+dst)
			else:
				im.save(dst)
				
print('running...XYZtoTMS')

def main(minZoomRange=0,maxZoomRange=20):
	# zoomRange = 10
	for i in range(maxZoomRange,minZoomRange-1,-1):
		toTMS(*getTileBound(i),130)


if __name__ == "__main__":
    minZoomRange = int(sys.argv[1])
    maxZoomRange = int(sys.argv[2])
    main(minZoomRange,maxZoomRange) 