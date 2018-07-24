import os

def createFolder(filePath):
	if not os.path.exists(filePath):
		os.makedirs(filePath)
		print('create folder: ',filePath)

# for i in range(1,21):
# 	zoomFolder = "zoom{}".format(i)
# 	dataFolder = "zoom{0}/data{0}".format(i)
# 	tempFolder = "zoom{0}/temp{0}".format(i)

# 	if not os.path.exists(zoomFolder):
# 		os.makedirs(zoomFolder)

# 	if not os.path.exists(dataFolder):
# 		os.makedirs(dataFolder)

# 	if not os.path.exists(tempFolder):
# 		os.makedirs(tempFolder)

# if not os.path.exists("TMSimage"):
# 	os.makedirs("TMSimage")

