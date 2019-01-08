

from bs4 import BeautifulSoup
import requests
import traceback
import logging
import os
from concurrent.futures import ThreadPoolExecutor
import time

import threading

cond=threading.Condition()
class df:
    def __init__(self):
        print(type(self.__class__.__name__))

df()

'''
list=os.listdir("C:/file/ResultFile/")
print(list.__len__())
for i in list:
    print(i)



logger=logging.getLogger("spiderlog")
#fh=logging.FileHandler("C:/File/ResultFile/spider.log")
logger.setLevel(logging.INFO)
ch=logging.StreamHandler()

log_file=open("C:/File/ResultFile/spiderlog","a+",encoding="utf-8")
#fh.setLevel(logging.ERROR)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#fh.setFormatter(formatter)
ch.setFormatter(formatter)
#logger.addHandler(fh)
logger.addHandler(ch)

def get_html(url):
    data = requests.get(url)
    data.encoding = 'utf-8'
    datatext = data.text
    data.close()
    return datatext
try:
    a=0
    b=1

    print(b/a)
except BaseException as e:
    logger.info("sdf")
    traceback.print_exc(file=log_file)








def get_html(url,*code):
    data = requests.get( url )
    if code:
        data.encoding = code[0]
    data = data.text
    return data


url="http://www.ccgp-qinghai.gov.cn/ftl/jilin/noticeDetail.jsp?htmlURL=html/2015/12/16/C000141.html"
#获取公告内的详细信息
def get_url_1(url, file):
    print("g_u_1 start...")

    dnum=re.search("(\d{4}/\d{1,2}/\d{1,2})",url).span()
    date=url[dnum[0]:dnum[1]]

    suffix_num=re.search("htmlURL=",url).span()
    suffix=url[suffix_num[1]:]
    new_url="http://www.ccgp-qinghai.gov.cn/"+suffix
    html = get_html(new_url,'gbk')
    soup = BeautifulSoup(html, "html.parser")

    tag = soup.find("body")

    title=""
    for p_title in tag.find_all("p",align="center"):
        title=title+p_title.get_text().strip()
        p_title.extract()

    [s.extract() for s in tag('input')]

    text=tag.get_text().strip()
    text = "".join(text.split())
    line=url+"##"+date+"##"+title+"##"+text

    file.write(str(line.encode('gbk',errors="ignore")).replace("b'",'').replace("'",'')+ '\n')



get_url_1(url,None)

html = get_html(url)

soup = BeautifulSoup(html, "html.parser")
div = soup.find_all("div", class_="article-info")[0]
[s.extract() for s in div('script')]
[s.extract() for s in div('style')]
title = div.find_all("h1")[0].get_text().strip().replace("\n", "")
date = div.find_all("p", class_="infotime")[0].get_text().strip().replace("\n", "")
text = div.find_all("div")[0].get_text().strip()

text="".join(text.split())
print(text)

import re

file_path = "C:/file/ResultFile/hnggzy_spider_result.txt"
file=open(file_path,encoding="utf-8")


files=file.readlines()
print(files)
str=""
for line in files:
   # print("dsdf"+line)
    if not re.match("http",line):
        #print(line)
        str=str+line

print("============================",str)
'''