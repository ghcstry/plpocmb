#!/usr/bin/python3
#coding: utf-8

import requests
import argparse
import threading
import time

def urls(path):
	with open(path,'r') as f:
		urls = f.readlines()
		return urls

def log(log):
	with open('log.txt','a+',encoding='utf-8') as f:
		f.write(log + '\n')

def ok(ok):
	with open('ok.txt','a+',encoding='utf-8') as f:
		f.write(ok + '\n')

def connect(url,proxies):
	headers = {"Connection":"close","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36","Accept-Encoding":"gzip, deflate","X-Forwarded-For":"127.0.0.1"}
	i = 3
	while i != 0:
		if 'https://' in url or 'http://' in url:
			url = url
		else:
			url = 'https://' + url
		try:
			requests.packages.urllib3.disable_warnings()
			response = requests.get(url=url,headers=headers,proxies=proxies,verify=False,timeout=60)
			return url
		except:
			url = url.replace('https://','http://')
			try:
				response = requests.get(url=url,headers=headers,proxies=proxies,verify=False,timeout=60)
				return url
			except Exception as e:
				i = i - 1
				url = url.replace('http://','')
				out = url + ' ----- 连接出错 ----- ' + str(e)
				print(out)
				time.sleep(3)
	log(out)
	url = ''
	return url

def poc(url,proxies):
	print(url)

def pl(url,proxies,se):
	se.acquire()
	url = connect(url,proxies)
	if url != '':
		poc(url,proxies)
	se.release()

if __name__ == '__main__':

	ap = argparse.ArgumentParser()
	ap.add_argument('-u','--url',help='xx.com or http://xx.com')
	ap.add_argument('-f','--file',help='file path')
	ap.add_argument('-p','--proxy',help='http://127.0.0.1:8080')
	ap.add_argument('-t','--thread',help='xiancheng 10',type=int,default=10)
	args = vars(ap.parse_args())

	if args['proxy'] != None:
		proxies = {'http':args['proxy'],'https':args['proxy']}
	else:
		proxies = {}

	if args['file'] != None:
		se = threading.BoundedSemaphore(args['thread'])
		for u in urls(args['file']):
			u = u.replace('\n','')
			t = threading.Thread(target=pl,args=(u,proxies,se,))
			t.start()

	if args['url'] != None:
		url = connect(args['url'],proxies)
		if url != '':
			poc(url,proxies)
