#!/usr/bin/env python
# coding=utf-8

import re
import requests
from bs4 import BeautifulSoup

def get_html(url):
    data = requests.get( url )
    data.encoding = 'gbk'
    data = data.text
    return data

def get_title(html):
    print(html)
    str4 = '<span style="font-size: 20px;font-weight: bold">.*\n?.*</span>'
    patten4 = re.compile( str4 )
    result4 = patten4.findall( html )
    print(result4)
    soup = BeautifulSoup(result4[0], "html.parser")
    return soup.find_all("span")[0].get_text().strip().replace("\n"," ")

url = "http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/t20180911_1025538.html"
#url="http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/t20180911_1025603.html"


html=get_html(url)
print(get_title(html))





'''
def get_text(html):
    test_result = re.search( '<div align="left" style="padding-left:30px;">', html )
    data_div_front = html[test_result.span()[1]:]
    test_result = re.search( '</div>', data_div_front )
    data_div = data_div_front[0:test_result.span()[0]]

    str=""

    soup = BeautifulSoup( data_div, "html.parser" )
    [ s.extract() for s in soup('style')]

    for tag in soup.find_all( "p" ):
        str=str+tag.get_text().strip()

    return str.replace("\n","")


def get_next_page(html):
    print(html)
    patten = re.compile( '</span>.*</a>' )
    result = patten.findall( html )
    soup = BeautifulSoup(result[0], "html.parser")
    a_tag = soup.find_all("a")
    next_page_url = "http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/" +a_tag[0]["href"]
    return next_page_url

'''