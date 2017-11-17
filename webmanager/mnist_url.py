import os
import shutil
import sys
import urllib2


mnist = 'mnisturl.txt'
path = '/home/ubuntu/data/mnist_png/'
t_path = '/mnist_png/training'
with open(mnist, 'w') as ff:
	ff.write('28\n')
	ff.write('0,1,2,3,4,5,6,7,8,9\n')
	for i in  range(0, 10):
		temp = os.path.join(path, 'training', str(i))
		ff.write("{}\n".format(i))
		#print os.listdir(temp)
		print temp
		for filename in os.listdir(temp):
			ff.write('http://127.0.0.1:8000'+os.path.join(t_path, str(i), filename)+'\n')
		ff.write('.\n')
		
	
	
