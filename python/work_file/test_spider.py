#!/usr/bin/env python
# coding=utf-8

import re
import json
import requests
from bs4 import BeautifulSoup

def get_html(url):
    data = requests.get( url )
    data.encoding = 'gbk'
    data = data.text
    return data




url="http://www.gdgpo.gov.cn/queryMoreInfoList.do"

header={
    "Cookie":"PortalCookie=XjLmLx62fjxUYbo7sbHzgJgF7xNLbLgivsnF1OlCJQI4MGnwKmrk!-435088654; ManageSystemCookie=bSDmLyKdQclMeRsMuzqcAZeHENjop8daDC-MoSrKSDqUoAxk8ylx!-1106207408",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
}

p={
    'channelCode': int("00051"),
    'pointPageIndexId': 1,
    'pageIndex': 5,
    'pageSize': 15,
    'pointPageIndexId': 4,
                  }
data = requests.post(url, data=json.dumps(p))
print(data)
soup=BeautifulSoup( data.text, "html.parser" )
print(soup.find_all("ul",class_="m_m_c_list"))
'''
for url in soup.find_all("ul",class_="m_m_c_list"):
    print(url)
'''
'''



header={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language":" zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": 268,
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "PortalCookie=XjLmLx62fjxUYbo7sbHzgJgF7xNLbLgivsnF1OlCJQI4MGnwKmrk!-435088654; ManageSystemCookie=bSDmLyKdQclMeRsMuzqcAZeHENjop8daDC-MoSrKSDqUoAxk8ylx!-1106207408",
    "Host": "www.gdgpo.gov.cn",
    "Origin": "http://www.gdgpo.gov.cn",
    "Referer": "http://www.gdgpo.gov.cn/queryMoreInfoList.do",
    "Upgrade-Insecure-Requests": 1,
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36"
}


p={
    'channelCode': int("00005"),
    'issueOrgan':'',
    'operateDateFrom':'',
    'operateDateTo':'',
    'performOrgName':'',
    'pointPageIndexId': 1,
    'purchaserOrgName':'',
    'regionIds':'',
    'sitewebId': '4028889705bebb510105bec068b00003',
    'sitewebName':'',
    'stockIndexName':'',
    'stockNum':'',
    'stockTypes':'',
    'title':'',
    'pageIndex': 3,
    'pageSize': 15,
    'pointPageIndexId': 2,
                  }

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