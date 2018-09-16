#!/usr/bin/env python
# coding=utf-8
from urllib import request
import requests
import time
from bs4 import BeautifulSoup
import random
from faker import Factory

list = []
urls = []
detail_url = []


def get_html(url,f):
    ua = f.user_agent()
    data = requests.get(url, headers={"Uesr-Agent": ua})
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
            detail_url.append("http://cz.fjzfcg.gov.cn"+a_tag["href"])



def get_next_page(html):
    soup = BeautifulSoup(html, "html.parser")
    for div_tag in soup.find_all("div",class_="pageGroup"):
        num=-1
        for active_tag in div_tag.find_all("button",class_="active"):
            num=active_tag.get_text()
        for next in div_tag.find_all("button"):
            if "下一页" == next.get_text().strip():
                return int(num)+1
        return

#获取各个地区对应的URLs
def get_urls():
    for argv in list:
        new_url = url + "?zone_code=" + argv[0] + "&zone_name=" + argv[1]
        urls.append(new_url)

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


if __name__ == '__main__':
    url = "http://cz.fjzfcg.gov.cn/3500/openbidlist/f9ebc6637c3641ee9017db2a94bfe5f0/"
    file_path= "C:/file/ResultFile/fjzfcg_spider_result.txt"

    faker = Factory.create()
    html = get_html(url,faker)
    get_url_argv(html)
    get_urls()
    f=open(file_path,"a+",encoding="utf-8")

    for f_url in  urls:
        page_url=f_url
        while(True):
            f_html=get_html(page_url,faker)
            get_detail_url(f_html)
            for s_url in detail_url:
                print(s_url + " 开始下载...")
                time.sleep(random.random()*8)
                s_html=get_html(s_url,faker)
                date=get_date(s_html)
                title=get_title(s_html)
                text=get_text(s_html)

                f.write(s_url+"##"+date + "##" + title + "##" + text + "\n")

                detail_url.remove(s_url)

            num=get_next_page(f_html)
            if not num is None:
                page_url=f_url+"&page="+str(num)
            else:
                break











'''

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


'''





