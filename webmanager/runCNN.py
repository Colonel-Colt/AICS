import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression
import os
import shutil
import dataset
import imageFromUrl as iurl
def runCNN(files, download = True, urlfile = 'url.txt', path = '/home/ubuntu/data/download', image_size = 32, model_file = 'model.pkl', nclasses = 10):
	if download:
		iurl.downloadImage(urlfile, path)
	X, num = dataset.load_run(files, path, image_size)
	X = X.reshape([-1, image_size, image_size, 1])
	network = input_data(shape=[None, image_size, image_size, 1], name='input')
        network = conv_2d(network, 16, 3, activation='relu', regularizer="L2")
        network = max_pool_2d(network, 2)
        network = local_response_normalization(network)
        network = conv_2d(network, 32, 3, activation='relu', regularizer="L2")
        network = max_pool_2d(network, 2)
        network = local_response_normalization(network)
        network = fully_connected(network, 32, activation='tanh')
        network = dropout(network, 0.8)
        network = fully_connected(network, 64, activation='tanh')
        network = dropout(network, 0.8)
        network = fully_connected(network, nclasses, activation='softmax')
        network = regression(network, optimizer='adam', learning_rate=0.0005, loss='categorical_crossentropy', name='target')
	model = tflearn.DNN(network)
	model.load(model_file)
	Y = model.predict(X)
	print (Y)
	return Y

def init(username, img, path):
	image_size = 0
	classes = []
	try:
		pp = os.path.join(os.getcwd(), username, 'classes')
		f = open(pp, 'r')
		image_size = int(f.readline()[:-1])
		while True:
			aclass = f.readline()
			if not aclass: break
			while aclass[-1] =='\n' or aclass[-1] == '\r': aclass = aclass[:-1]
			classes.append(aclass)
	except:
		print("Error when read image_size and classes")
	index = 1
	try:
		os.mkdir(path)
	except:
		print('path existed')
	files = []
	for item in img:
		print "LALAL", item, os.path.join(path, str(index) + '.jpg')
		shutil.copy(item, os.path.join(path, str(index) + '.jpg'))
		files.append(os.path.join(path, str(index) + '.jpg'))
		index += 1
	print files
	return image_size, classes, files

def output(classes, Y):
	result = []
	n = len(classes)
	print classes
	for y in Y:
		max = -1.0
		maxi = 0
		i = 0
		for p in y:
			if p>max:
				max = p
				maxi = i
			i += 1
		result.append([True, classes[maxi], max])
	return result

def run(username, img):
	username = 'user/' + username
	path = os.path.join(os.getcwd(), username)
	temp = os.path.join(path, 'temp')
	model = os.path.join(path, 'cnn.model')
	image_size, classes, files = init(username, img, temp)
	print image_size, classes, files
	url = []
	try:
		Y = runCNN(files, False, url, temp, image_size, model, len(classes))
	except:
		print "Run CNN error"
		return [[False,"",[]]]
	return output(classes, Y)
#print run('temp', ['/home/ubuntu/data/mnist_png/testing/0/1995.png','/home/ubuntu/data/mnist_png/testing/1/3148.png', '/home/ubuntu/data/mnist_png/testing/2/418.png', '/home/ubuntu/data/mnist_png/testing/3/5479.png', '/home/ubuntu/data/mnist_png/testing/4/6417.png', '/home/ubuntu/data/mnist_png/testing/5/7448.png',
#	'/home/ubuntu/data/mnist_png/testing/6/8771.png','/home/ubuntu/data/mnist_png/testing/7/9864.png','/home/ubuntu/data/mnist_png/testing/8/179.png','/home/ubuntu/data/mnist_png/testing/9/273.png'])
#print run('temp', ['/home/ubuntu/data/train/cats/2.jpg','/home/ubuntu/data/train/dogs/3.jpg'])
#url = 'minist_test.txt'
#path = '/home/ubuntu/data/download/'
#image_size = 28
#model = '/home/ubuntu/CS6203/project/server/minist_model.pkl'
#runCNN(True, url, path, image_size, model)
