#!/usr/bin/python3
#coding: utf-8

import requests
import os

def down_file(fileurl,folder,filename):
	fname = folder + filename
	if os.path.exists(fname):
		print(filename,'  ---已存在')
	else:
		with open(fname,'wb') as f:
			try:
				f.write(requests.get(fileurl).content)
				print(filename,'  ---已下载')
			except:
				print(filename,'  ---下载出错')
				os.remove(fname)

if __name__ == '__main__':
	folder = 'files/'
	if os.path.exists(folder) == False:
		os.makedirs(folder)
	fileurl = 'https://xx.com/*.png.jpg.mp3.mp4.pdf.doc...'
	filename = 'xx.png...'
	down_file(fileurl,folder,filename)
