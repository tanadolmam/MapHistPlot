# XYZ to TMS
import os,math,shutil
from lib.mapTool import getTileBound

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
def toTMS(zoom,xmin,xmax,ymin,ymax):
	print(zoom)
	# clearDirectory('TMSimage/{}'.format(zoom-1))
	for i in range(xmin,xmax+1):
		for j in range(ymin,ymax+1):
			yTMS = (2 ** zoom)-j-1
			src = "output/zoom{0}/{0}-{1}{2}.png".format(zoom,i,j)

			dst = "TMSimage/{0}/{1}/{2}.png".format(zoom-1,i,yTMS)
					#copyfile(src, dst)

			if not (os.path.exists("TMSimage/{0}/{1}".format(zoom-1,i,yTMS))):
				os.makedirs("TMSimage/{0}/{1}".format(zoom-1,i,yTMS))
			
			if(os.path.isfile(src)):
				# print(src)
				# os.remove(dst)
				shutil.copy(src, dst) 
				# print("move "+src+" to "+dst)
			else:
				print('file not found('+src+')')
print('running...XYZtoTMS')


zoomRange = 10
for i in range(zoomRange,1,-1):
# toTMS(*getTileBound(12))
# toTMS(*getTileBound(11))
# toTMS(*getTileBound(10))
# toTMS(*getTileBound(9))
# toTMS(*getTileBound(8))
# toTMS(*getTileBound(7))
# toTMS(*getTileBound(6))
# toTMS(*getTileBound(5))
# toTMS(*getTileBound(4))
	toTMS(*getTileBound(i))
