import cv2
import dataset
import imageFromUrl as iurl
import os
import glob
import random
import runCNN
import numpy as np
from sklearn import svm
from sklearn.externals import joblib
def runSVM(files, path, urlFile, image_size = 32, model_file = 'model.pkl', download = True):
	print('Predict with HOG feature and SVM')
	if download:
		print('Downloading images')
		iurl.download(urlfile, path)
	X, num = dataset.load_run(files, path, image_size, True)
#	print("Number of data:{}".format(num))
	clf = joblib.load(model_file)
	result = clf.predict_proba(X).tolist()
#	print 'result is ',result
	return result

def run(username, img):
	username = 'user/' + username
	path = os.path.join(os.getcwd(), username)
	temp = os.path.join(path, 'temp')
	model = os.path.join(path, 'svm.model')
#	print "what happened" 
	image_size, classes, files = runCNN.init(username, img, temp)
#	print "files is ", files
	urlFile = []
	try:
		Y = runSVM(files, temp, urlFile, image_size, model, False)
	except:
		print "Run SVM error"
		return [[False, "", 0]]
	return runCNN.output(classes, Y)
#print run('temp', ['/home/ubuntu/data/train/cats/2.jpg','/home/ubuntu/data/train/dogs/3.jpg'])
