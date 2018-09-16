#!/usr/bin/env python
# coding=utf-8
from urllib import request
import re
import requests
import json
import os
import sys
from bs4 import BeautifulSoup

detail_url=[]

def get_html(url):
    data = requests.get( url )
    data.encoding = 'gbk'
    data = data.text
    return data

def get_next_page(html):
    patten = re.compile( '</span>.*</a>' )
    result = patten.findall( html )
    soup = BeautifulSoup(result[0], "html.parser")
    a_tag = soup.find_all("a")
    next_page_url = "http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/" +a_tag[0]["href"]
    return next_page_url

def has_next():
    return True


def get_detail_url(html):
    patten = re.compile(  '<a href=".*html"' )
    result = patten.findall( html )

    for str in result:
        url = "http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/" + str[11:-1]
        detail_url.append( url )

def get_date(html):
    str3 = '<span class="datetime" style="float:right;margin-right: 52px">.*</span>'
    patten3 = re.compile( str3 )
    result3 = patten3.findall( html )
    date = result3[0][62:-7]
    return date

def get_title(html):
    str4 = '<span style="font-size: 20px;font-weight: bold">.*\n?.*</span>'
    patten4 = re.compile( str4 )
    result4 = patten4.findall( html )
    soup = BeautifulSoup(result4[0], "html.parser")
    return soup.find_all("span")[0].get_text().strip().replace("\n"," ")


def get_text(html):
    test_result = re.search('<div align="left" style="padding-left:30px;">', html)
    data_div_front = html[test_result.span()[1]:]
    test_result = re.search('</div>', data_div_front)
    data_div = data_div_front[0:test_result.span()[0]]

    str = ""

    soup = BeautifulSoup(data_div, "html.parser")
    [s.extract() for s in soup('style')]

    for tag in soup.find_all("p"):
        str = str + tag.get_text().strip()

    return str.replace("\n", "")

if __name__ == '__main__':
    url = "http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/index.html"  #sys.argv[1]
    resout_file_path = "C:/file/python/work_file/ccgp-beijing_spider_result_2.txt"  #sys.argv[2]

    u_url=url
    f = open(resout_file_path, "a+", encoding="utf-8")
    while(True) :
        html = get_html(u_url )
        get_detail_url( html )

        for url in detail_url:
            print(url)
            detail_html = get_html( url )
            date = get_date( detail_html )
            title = get_title( detail_html )
            text = get_text( detail_html )
            print( title+" 下载中...")
            f.write(date+"##"+url+"##"+title+"##"+text+"\n")
            detail_url.remove( url )

        next_page_url = get_next_page( html )
        u_url = next_page_url
'''
    html=get_html(url)

    get_detail_url(html)

    if detail_url :
        next_page_url = get_next_page( html )
        next_html=get_html(next_page_url)
        get_detail_url(next_html)
    else:
        for url in detail_url:
            detail_html=get_html(url)
            date=get_date(detail_html)
            print(date)
            title=get_title(detail_html)
            print(title)
            text=get_text(detail_html)
            print(text)

            detail_url.remove(url)
'''

