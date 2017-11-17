import os
import sys
import shutil

def parse(urlfile,path):
	classes = []
	f = open(urlfile,'r')
	i = 0
	image_size = int(f.readline()[:-1])
	classes = f.readline()[:-1].split(',')
	print classes
	while True:
		url = f.readline()[:-1]
		print url
		if not url: break
		urllist = [url]
		while True:
			url = f.readline()[:-1]
			if url == '.' or url == '.\r': break
			urllist.append(url)
		#print urllist

		with open("{}/{}.txt".format(path, classes[i]), "w") as ff:
			for item in urllist:
				ff.write("%s\n" % item)
		i += 1
	return image_size, classes
#print(parse("/home/ubuntu/CS6203/project/server/example_train.txt","/home/ubuntu"))

