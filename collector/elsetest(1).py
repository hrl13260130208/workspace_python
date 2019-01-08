# -*- coding:utf-8 -*-
# encoding=utf8 
import sys
import socket
import os
import urllib
import requests
import random
from bs4 import BeautifulSoup
import redis
from faker import Factory
import os
import sys
import traceback
import progressbar
import time


fake = Factory.create()

def get_host_ip():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		ip = s.getsockname()[0]
		
	finally:
		s.close()
 
	return ip



def redis_connection(redis_setname,ip_addr):

	def add_r(redis_setname):
		with open('url.txt','r+') as f:
			for count,url in enumerate(f):
				redis_connect.sadd(redis_setname,url)
				print (count)

	if get_host_ip() == ip_addr:

		redis_connect = redis.Redis(host = 'localhost',port = 6379,db = 1)
		urls = redis_connect.smembers(redis_setname)
		if len(urls) > 0:
			print ('request data already exists!')
			pass
		else:
			print ('start import redis!')
			add_r(redis_setname)
	else:
		redis_connect = redis.Redis(host = ip_addr,port = 6379,db = 1)
		urls = redis_connect.smembers(redis_setname)
		if len(urls) > 0:
			print ('request data already exists!')
			pass
		else:
			print ('start import redis!')
			add_r(redis_setname)

	return urls

def headers():
	header = {
		#'Host': 'www.sciencedirect.com',
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': fake.user_agent(),
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
		
	}
	return header


def pdf_download_fun(url,path,rename,extend):

	def Schedule(a,b,c):
		per = 100.0 * a * b / c
		if per > 100 :
			per = 100
		print ('%.2f%%' % per)

	local = os.path.join(path,rename + '.' + extend)
	urllib.urlretrieve(url,local,Schedule)

def calculate_part(part,num_of_part,urls):

	length = len(urls)
	b = length / part
	start = b * (num_of_part - 1)
	end = b * num_of_part
	return start,end

def main_fun(part,num_of_part,download_path,redis_setname,ip_addr):

	urls = redis_connection(redis_setname,ip_addr)

	if not os.path.exists(download_path):
		os.makedirs(download_path)

	for count,pdf_url in enumerate(urls):
		
		try:
			s,e = calculate_part(part,num_of_part,urls)
			print (count,s,e)
			if count >= s and count < e:
				if os.path.exists(os.path.join(download_path,str(count) + '.pdf')):
					print (str(count) + '.pdf already download!')
					pass
				else:
					print (pdf_url)
					test_str = BeautifulSoup(requests.get(str(pdf_url).strip().replace('\n','')).content,'html.parser').find(attrs = {'id':'redirectURL'}).get('value').replace('%3A',':').replace('%2F','/').replace('%3F','?')
					print (test_str)
					if 'Dihub' in test_str:
						r = requests.get(test_str, headers=headers())
						print ('start requests main_url')
						soup = BeautifulSoup(r.content,'html.parser')
						print ('get main_url page')
						a = soup.find_all('meta')
						for i in a:
							if i.get('name') == "citation_pdf_url":
									#print (i.get('content'))
									pdf_re = requests.get(i.get('content'), headers=headers())
									print ('request child_url')
									pdf_download = BeautifulSoup(pdf_re.content,'html.parser').find('a').get('href')
									
									print (pdf_download)
									print ('start download 1 pdf')

									try:
										size = 0
										#pdf_download_fun(pdf_download,download_path,str(count),'pdf')
										other_p = requests.get(pdf_download,headers = headers(),stream = True,timeout = 10)
										total_length = int(other_p.headers.get("Content-Length"))
										with open(download_path + '/' + str(count) + '.pdf','wb') as f:
											print ('start download')
											widgets = ['Progress: ', progressbar.Percentage(), ' ',progressbar.Bar(marker='#', left='[', right=']'),' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
											pbar = progressbar.ProgressBar(widgets=widgets, maxval=total_length).start()
											for chunk in other_p.iter_content():
												if chunk:
													size += len(chunk)
													f.write(chunk)
												pbar.update(size)
											pbar.finish()
											f.flush()


									except Exception as e:
										print (e)
										with open('downloadError.txt','a+') as f:
											f.write(str(pdf_url) + '\n')
									with open(download_path + '.txt','a+') as f:
										f.write(str(pdf_url).replace('\n','') + '$$$$' + str(count) + '.pdf' + '$$$$' + pdf_download + "\n")
					else:
						r = requests.get(test_str, headers=headers())
						print ('start requests main_url')
						soup = BeautifulSoup(r.content,'html.parser')
						print ('get main_url page')
						a = soup.find_all('meta')
						for i in a:
							if i.get('name') == "citation_pdf_url":
								print ('start download 2 pdf')
								pdf_download = i.get('content')
								try:
									size = 0
									other_p = requests.get(pdf_download,headers = headers(),stream = True,timeout = 10)
									total_length = int(other_p.headers.get("Content-Length"))
									with open(download_path + '/' + str(count) + '.pdf','wb') as f:
										print ('start download')
										widgets = ['Progress: ', progressbar.Percentage(), ' ',progressbar.Bar(marker='#', left='[', right=']'),' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
										pbar = progressbar.ProgressBar(widgets=widgets, maxval=total_length).start()
										for chunk in other_p.iter_content():
											if chunk:
												size += len(chunk)
												f.write(chunk)
											pbar.update(size)
										pbar.finish()
										f.flush()

								except:
									with open('downloadError.txt','a+') as f:
										f.write(pdf_url + '\n')
								with open(download_path + '.txt','a+') as f:
									f.write(pdf_url.replace('\n','') + '$$$$' + str(count) + '.pdf' + '$$$$' + pdf_download + "\n")

							# data save setup!

							
		except Exception as e:
			print (e)
			continue	
if __name__ == '__main__':

	# 从左到右 跑分布式的总机数 以及现在是第几台机器 下载pdf的文件夹，redis数据库所在机器的ip地址，
	
	main_fun(31,1,'else11_29','else11_29','localhost')
	end = time.time()
	
	#print (s,e)
		