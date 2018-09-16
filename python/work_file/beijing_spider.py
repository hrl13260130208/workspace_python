#!/usr/bin/env python
# coding=utf-8
from urllib import request
import re
import requests
import json
import os
import sys
from bs4 import BeautifulSoup


url="http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/index.html"
resout_file_path="C:/file/python/work_file/result.txt"

data=requests.get(url)
data.encoding='gbk'
data=data.text
#print(data)

detail_url=[]
next_page_url=""

str1='<a href=".*html"'
patten1=re.compile(str1)
result1=patten1.findall(data)
print(result1)


str2='</span>.*</a>'
patten2=re.compile(str2)
result2=patten2.findall(data)
print(result2)

next_page_url="http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/"+result2[0][46:58]
print(next_page_url)


for str in result1:
    url="http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/"+str[11:-1]
    detail_url.append(url)

def getDetail(urls):
    for url in urls:
        print(url)


data0=requests.get(detail_url[0])
data0.encoding='gbk'
data0=data0.text
print(data0)


str3='<span class="datetime" style="float:right;margin-right: 52px">.*</span>'
patten3=re.compile(str3)
result3=patten3.findall(data0)
print(result3)
date=result3[0][62:-7]
print(date)


str4='<span style="font-size: 20px;font-weight: bold">.*</span>'
patten4=re.compile(str4)
result4=patten4.findall(data0)
print(result4)
title=result4[0][48:-7]
print(title)



test_result=re.search('<div align="left" style="padding-left:30px;">',data0)
data_div_front=data0[test_result.span()[1]:]
print(data_div_front)
test_result=re.search('</div>',data_div_front)
data_div=data_div_front[0:test_result.span()[0]]
print(data_div)

p_file=re.findall("<p.*?>(\W+?)</p>",data_div)
print(p_file.__len__())

soup=BeautifulSoup(data_div,"html.parser")

print("+++++++++++++++soup结果+++++++++++++++++++++")
str=""
list=[]
print(type(str))
for tag in soup.find_all("p"):
    str=str+tag.get_text()

print("txet:"+str.strip())

f=open(resout_file_path,"a+",encoding="utf-8")
f.writelines(str.strip())
def get_next_page(html):
    patten = re.compile( '</span>.*</a>' )
    result = patten.findall( html )
    next_page_url = "http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/" + result[0][46:58]
    return next_page_url

def get_detail_url(html):
    patten = re.compile(  '<a href=".*html"' )
    result = patten.findall( html )

    for str in result:
        url = "http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/" + str[11:-1]
        detail_url.append( url )












