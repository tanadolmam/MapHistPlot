import os

def createFolder(filePath):
	if not os.path.exists(filePath):
		os.makedirs(filePath)
		print('create folder: ',filePath)




