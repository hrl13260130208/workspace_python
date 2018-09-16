#!/usr/bin/env python
# coding=utf-8
<<<<<<< HEAD


import requests
import threading
from bs4 import BeautifulSoup
import time
import redis


list = []
urls = []
detail_url = redis.Redis(host="127.0.0.1",port=6379,decode_responses=True)
condition=threading.Condition()
done=False


class Put_Thread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        producer(url)

def producer(url):
    global done
    put_url(url)

    while(True):
        if(condition.acquire()):
            done=True
            condition.notify_all()
            condition.release()
            break

def put_url(url):
    print("put start...")
    html = get_html(url)
    get_url_argv(html)
    get_urls()

    for f_url in urls:
        page_url = f_url
        while (True):
            f_html = get_html(page_url)
            get_detail_url(f_html)
            num = get_next_page(f_html)
            if not num is None:
                page_url = f_url + "&page=" + str(num)
            else:
                break
            if (condition.acquire()):
                condition.notify_all()
                condition.release()

class Get_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        consumer()

def consumer():
    global done
    while (True):
        if(condition.acquire()):
            if  not detail_url.llen("detail_url")==0:
                get_url()
            else:
                if done:
                    break
                condition.wait()
            condition.release()
            time.sleep(2)

def get_url():
    print("get start...")
    time.sleep(2)
    print(detail_url.llen("detail_url"))
    while(not detail_url.llen("detail_url")==0):
        s_url = detail_url.rpop("detail_url")
        print(s_url)
        s_html = get_html(s_url)
        date = get_date(s_html)
        print(date)
        title = get_title(s_html)
        print(title)
        text = get_text(s_html)
        print(text)
=======
from urllib import request
import re
import requests
import json
import os
import sys
from bs4 import BeautifulSoup
>>>>>>> github/master

def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data

def get_url_argv(html):
    soup = BeautifulSoup(html, "html.parser")
    for ul_tag in soup.find_all("ul", class_="nav-second-level"):
        for a_tag in ul_tag.find_all("a", class_="zc"):
            codes = a_tag["codes"]
            name = a_tag.get_text()
            list.append([codes, name])

def get_detail_url(html):
    soup = BeautifulSoup(html, "html.parser")
    for table in soup.find_all("table"):
        for a_tag in table.find_all("a"):
<<<<<<< HEAD
            detail_url.lpush("detail_url","http://cz.fjzfcg.gov.cn"+a_tag["href"])
=======
            detail_url.append("http://cz.fjzfcg.gov.cn"+a_tag["href"])
>>>>>>> github/master



def get_next_page(html):
    soup = BeautifulSoup(html, "html.parser")
    for div_tag in soup.find_all("div",class_="pageGroup"):
        num=-1
        for active_tag in div_tag.find_all("button",class_="active"):
            num=active_tag.get_text()
        for next in div_tag.find_all("button"):
<<<<<<< HEAD
            if "下一页" == next.get_text().strip():
                return int(num)+1
        return

#获取各个地区对应的URLs
def get_urls():
    for argv in list:
        new_url = url + "?zone_code=" + argv[0] + "&zone_name=" + argv[1]
        urls.append(new_url)

=======
            print("next:"+next.get_text())
            if "下一页" == next.get_text().strip():
                return num
        return

>>>>>>> github/master
def get_date(html):
    soup = BeautifulSoup( html, "html.parser" )
    for div_tag in soup.find_all("div",class_="clearfix"):
        span = div_tag.find_all("span")
    return span[2].get_text()

def get_title(html):
    soup = BeautifulSoup( html, "html.parser" )
    return soup.find_all("h2")[0].get_text()

def get_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("div",class_="notice-con")[0].get_text().strip().replace("\n", "")




<<<<<<< HEAD

if __name__ == '__main__':
    url = "http://cz.fjzfcg.gov.cn/3500/openbidlist/f9ebc6637c3641ee9017db2a94bfe5f0/"
    t_put=Put_Thread(url)
    t_get=Get_Thread()

    t_put.start()
    t_get.start()

    t_put.join()
    t_get.join()

    print("end")


















'''

=======
>>>>>>> github/master
url="http://cz.fjzfcg.gov.cn/3500/openbidlist/f9ebc6637c3641ee9017db2a94bfe5f0/"

list=[]
urls=[]
detail_url=[]
html=get_html(url)
print("++++++++++++++++++++")
get_url_argv(html)
print(list)


#获取各个地区对应的URLs
for argv in list:
    new_url=url+"?zone_code="+argv[0]+"&zone_name="+argv[1]
    urls.append(new_url)

first_level_url_html=get_html(urls[0])
print(first_level_url_html)
get_detail_url(first_level_url_html)
print(get_next_page(first_level_url_html))
s_html=get_html(detail_url[0])
print(detail_url[0])
print(get_date(s_html))
print(get_title(s_html))

print(get_text(s_html))


<<<<<<< HEAD
'''
=======

>>>>>>> github/master





