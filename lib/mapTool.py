from PIL import Image,ImageEnhance
import os.path,cv2,random,math

def tile2long(x,z) :
    #return min longtitude of a tile x
    return (x/math.pow(2,z)*360-180)

def tile2lat(y,z) :
    #return min latitude of a tile y
    n=math.pi-2*math.pi*y/math.pow(2,z);
    return (180/math.pi*math.atan(0.5*(math.exp(n)-math.exp(-n))))
        
def getTileBound(zoomRange):
    minZoomRange=20
    xmin = math.floor(807815/(2**(minZoomRange-zoomRange)))
    xmax = math.floor(831941/(2**(minZoomRange-zoomRange))) 
    ymin = math.floor(463368/(2**(minZoomRange-zoomRange)))
    ymax = math.floor(507913/(2**(minZoomRange-zoomRange)))
    return (zoomRange,xmin,xmax,ymin,ymax)

def mercLat2Norm(lat):
    x=math.tan(math.pi*(0.25+lat/360.0))
    new= math.log(x) * 180.0/math.pi
    return new

def bgColor(zoom,opacity=130):
	print("bgColor: ",zoom)
	zoom,xmin,xmax,ymin,ymax=getTileBound(zoom)
	totalFile = []
	for x in range(xmin,xmax+1):
		for y in range(ymin,ymax+1):
			imgName = "output/zoom{0}/temp{0}/{0}-{1}.png".format(zoom,str(x)+str(y))
			# imgName = "output/zoom10/temp10/test.png" 
			saveFile="output/zoom{0}/{0}-{1}.png".format(zoom,str(x)+str(y)) 
			# print(imgName)
			if (os.path.isfile(imgName)):
				# break
				foreground = Image.open(imgName)
				# background = Image.open(random.choice(bgcolor))
				# background = background.resize((foreground.size), Image.ANTIALIAS)
				background = Image.new('RGBA', foreground.size,(0,0,0,opacity))
				background.paste(foreground, (0, 0), foreground)
				temp=background
				
				# print('saving image... ',saveFile)  
				temp.save(saveFile,"PNG")
			else:
				print('image not found '+imgName)
def retouch(zoom,brightness=1,contrast=1,color=1,sharpness=1):
	print('retouch: ',zoom)
	zoom,xmin,xmax,ymin,ymax=getTileBound(zoom)
	for x in range(xmin,xmax+1):
		for y in range(ymin,ymax+1):
		
			imgName ="output/zoom{0}/{0}-{1}.png".format(zoom,str(x)+str(y))
			saveFile="output/zoom{0}/{0}-{1}.png".format(zoom,str(x)+str(y)) 
			
			if (os.path.isfile(imgName)==True):
				# break
				k = Image.open(imgName)
				# foreground.show()
				
				k= ImageEnhance.Contrast(k).enhance(contrast)
				k= ImageEnhance.Color(k).enhance(color)
				k= ImageEnhance.Sharpness(k).enhance(sharpness)
				k= ImageEnhance.Brightness(k).enhance(brightness)
				k.save(saveFile)
			else:
				print('file not found')
