#!/usr/bin/env python
# coding=utf-8

import re
import json
import requests
import time
from bs4 import BeautifulSoup



def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data


url="http://www.ccgp-jiangsu.gov.cn/cgxx/cggg/"
urls=[]

def get_next_page_url(url,urls):
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    div_tag = soup.find_all("div", class_="fanye")[0]
    script = div_tag.find_all("script", language="JavaScript")
    string = script[0].get_text().strip()
    num = re.search(',', string).span()[0]
    max_page = string[15:num]
    for i in range(int(max_page)):
        if i==0:
            urls.append(url+"index.html")
            continue
        urls.append(url+"index_"+str(i)+".html")
        print(url+"index_"+str(i)+".html")

get_next_page_url(url,urls)
'''
url = "http://www.hngp.gov.cn/henan/content?infoId=1536140453418362&channelCode=H740601&bz=0"

html=get_html(url)
soup = BeautifulSoup(html, "html.parser")
print(url + "  start...")

html = get_html(url)
soup = BeautifulSoup(html, "html.parser")
div_tag = soup.find_all("div", class_="BorderEEE BorderRedTop")[0]
print(div_tag)
[s.extract() for s in div_tag('style')]
title = div_tag.find_all("h1")[0].get_text().strip().replace("\n", "")
print(title)
date = div_tag.find_all("span", class_="Blue")[2].get_text().strip().replace("\n", "")
text = div_tag.find_all("div", id="content")#[0].get_text().strip().replace("\n", "")

print(date)
print(text)








url = "http://www.hnggzy.com/hnsggzy/infodetail/?infoid=91b808ef-79d6-4d45-858f-fe4bbbd49548&categoryNum=002001001"


def get_url_1(url):
    print(url+"  start...")
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    table_tag =soup.find_all("table", width="887")[0]
    [s.extract() for s in table_tag('br')]
    title= table_tag.find_all("td", height="76")[0].get_text().strip().replace("\n", "")
    print("title  "+title)
    date=table_tag.find_all("td", height="30")[0].get_text().strip().replace("\n", "")[10:19]
    print("date "+date)

    text= table_tag.find_all("td", style="padding:26px 40px 10px;")[0].get_text().strip()
    print("text ",text)
    #print("all:"+url + "##" + date + "##" + title + "##" + text + "\n")


def get_html(url):
    data = requests.get( url )
    data.encoding = 'gb2312'
    data = data.text
    return data


get_url_1(url)

'''


