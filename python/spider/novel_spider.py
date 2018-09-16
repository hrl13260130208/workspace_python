# coding=utf-8
import string
import requests
import json
import os

import re
import sys

url="https://www.biquge5200.com/xiaoshuodaquan/"
#url=sys.argv[0]
url_list=['www.biquge5200.com', 'www.biquge5200.com/','www.biquge5200.com/xuanhuanxiaoshuo/','www.biquge5200.com/xiuzhenxiaoshuo/','www.biquge5200.com/dushixiaoshuo/','www.biquge5200.com/chuanyuexiaoshuo/','www.biquge5200.com/wangyouxiaoshuo/','www.biquge5200.com/kehuanxiaoshuo/', 'www.biquge5200.com/paihangbang/','www.biquge5200.com/xiaoshuodaquan/']
character_list=["/","\?","\*"]
error_url_chapter_is_null=[]
usd_url=[]
usd_url_path = "d:/tensorflow/dataset/novel/usd_url.txt"

data=requests.get(url)
data.encoding='gbk'
data=data.text
#print(data)

str1="<a href.*</a>"
patten1=re.compile(str1)
result1=patten1.findall(data)
#print(result1)


def getUrls(results):
    """
    将正则表达式匹配到的连接转换成一个字典，key值为链接地址，value值为a标签的值
    :param results:
    :return:
   '''
   关于url去重，可以创建一个元组将访问过的链接存储到元组中
   本次可以将特定的几个链接去掉就行
   '''
   """
    string1='www.*"'
    string2='">.*</a>'
    pat1=re.compile(string1)
    pat2=re.compile(string2)
    urls = {}
    for result in results:
        keys=pat1.findall(result)
        values=pat2.findall(result)
        for i in range(keys.__len__()):
            key=keys[i][0:-1]
            value=values[i][2:-4]
            if key not in url_list:
                urls[key]=value
    return urls

def format(name):
    for c in character_list:
        name=re.sub(c,"_",name,count=0)
    return name


urls=getUrls(result1)
print(urls)
#print(urls.keys())
str2='<a href.*>第.*章.*</a>'
patten2=re.compile(str2)
str3='>.*<br'
patten3=re.compile(str3)

for key in urls.keys():
    print("爬取小说："+urls.get(key))
    resq=requests.get('http://'+key)
    resq.encoding="gbk"
    resq=resq.text
    result2=patten2.findall(resq)
    chapterUrls=getUrls(result2)
    #print(urls.get(key)+":",chapterUrls)
    if not chapterUrls:
        print(urls.get(key)+":chapterUrls为空值！")
        error_url_chapter_is_null.append(key)
        continue
    try:
        for url in chapterUrls:
            name=format(chapterUrls.get(url))
            print("开始爬取："+name+"...")
            response=requests.get("http://"+url)
            response.encoding="gbk"
            response=response.text
            result3=patten3.findall(response)[0][1:-3]
            path="d:/tensorflow/dataset/novel/"+urls.get(key)+"/"
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path+name+".txt","w",encoding="utf-8") as f:
                f.write(result3)
    finally :
        with open( usd_url_path, 'w', encoding="utf-8" ) as f:
            f.write( usd_url.__str__() )

    usd_url.append(key)


error_path="d:/tensorflow/dataset/novel/error_url_chapter_is_null.txt"
with open( error_path, 'w',encoding="utf-8" ) as f:
    f.write( error_url_chapter_is_null.__str__() )






