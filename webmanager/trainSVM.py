import cv2
import dataset
import imageFromUrl as iurl
import os
import glob
import random
import numpy as np
import urlParser
from sklearn import svm
from sklearn.externals import joblib
def trainSVM(train_path, classes, image_size = 32, model_file = 'model.pkl', download_flag = False):
	print('Training with HOG feature and SVM')
	if download_flag:
		print('Downloading images')
		for i in classes:
			iurl.downloadImage(os.path.join(train_path,i+'.txt'),os.path.join(train_path, i))
	X, Y, ids, cls, testX, testY, ids, cls, num = dataset.load_train(train_path, image_size, classes, 20, True)
	print ("Number of training data: {}".format(num))
	rand = np.random.RandomState(321)
	shuffle = rand.permutation(len(X))
#	print(X)
#	print(testX)
#	print(Y)
#	print(len(X[:-1]),len(Y))
	
	X = X[shuffle]
	Y = Y[shuffle]
#	print(X)
#	print(Y)
#	pause()
	clf = svm.SVC(probability = True)
	clf.fit(X, Y)
	result = clf.predict(testX)
	mask = result==testY
	correct = np.count_nonzero(mask)
#	print result
	print("Accuracy: {}".format(correct*100.0/len(result)))
	joblib.dump(clf, model_file)

def train(username):
	username = 'user/' + username
	train_path = os.path.join(os.getcwd(), username, 'training_set')
	urlFile = os.path.join(train_path, 'input.txt')
	try:
		os.remove(os.path.join(os.getcwd(), username, "trainOK.*"))
	except:
		print "trainOK.* not existed"
#	try:
	image_size, classes = urlParser.parse(urlFile, train_path)
#	except:
#		print "Parse error here"
#		return False
	try:
		with open(os.path.join(os.getcwd(), username, 'classes'), 'w') as f:
			f.write("%d\n" % image_size)
			for item in classes:
				f.write("%s\n" % item)
	except:
		print "Can't write classes file"
		return False
	model_file = os.path.join(os.getcwd(), username, 'svm.model')
	try:
		trainSVM(train_path, classes, image_size, model_file, True)
	except:
		print "TrainSVM error"
		return False
	try:
		open(os.path.join(os.getcwd(),username,"trainOK.svm"), "w")
	except:
		print "Cannot create trainOK.svm"
		return False
	return True
#train('temp')	
#train_path = '/home/ubuntu/data/train'
#image_size = 64
#classes = ['cats', 'dogs', 'insects', 'horses', 'goldfishes']
#classes = ['cat','dogs','insects', 'horses','goldfishes']
#train_path = '/home/ubuntu/data/mnist_png/training'
#image_size = 28
#classes = ['0','1','2','3','4','5','6','7','8','9']
#model_file = 'svm_model.pkl'
#trainSVM(train_path, classes, image_size, model_file)
					

