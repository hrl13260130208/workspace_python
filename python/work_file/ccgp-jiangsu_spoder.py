#!/usr/bin/env python
# coding=utf-8


import requests
import threading
from bs4 import BeautifulSoup
import time
import redis
import random
import re
'''
此爬虫使用了redis和生产者消费者模式，程序执行方式如下：
    首先启动一个put_thread，其需要一个初始页面的url、管理name的names对象、表示第几层的num
        put_thread会从初始页面获取下一级需要的url，并将其放到redis中
    然后如果put_thread生产的url就是内容页面，则创建一个get_thread（从内容页爬取数据）
        否则启动一个middle_thread，从上一个url中获取下一个url中并存入redis中

中途退出处理：如果程序因为各种原因退出，重新启动程序时，其会到redis中去查询上次爬取的进度，然后接着之前的继续爬取




'''
redis_ = redis.Redis(host="127.0.0.1",port=6379,decode_responses=True)
err_url=[]


class Put_Thread(threading.Thread):
    def __init__(self,url=None,names=None,num=None):
        threading.Thread.__init__(self)
        self.names=names
        self.num=num
        self.url=url

    def run(self):
        print("Put_Thread start...")
        urls=put_url_0(self.url)
        name=self.names.get_list_name(self.num)
        for url in urls:
            put_url_redis(name,url)
        condition=self.names.get_condition(self.num)
        done_name=self.names.get_done_name(self.num)

        while (True):
            if (condition.acquire()):
                redis_.getset(done_name,str(True))
                condition.notify_all()
                condition.release()
                break

class Get_Thread(threading.Thread):
    def __init__(self,fun=None,names=None,num=None,file=None):
        threading.Thread.__init__(self)
        self.fun=fun
        self.names=names
        self.num=num
        self.file=file
    def run(self):
        print("Get_Thread start...")
        condition=self.names.get_condition(self.num-1)
        list_name=self.names.get_list_name(self.num-1)


        while (True):
            if (condition.acquire()):

                if not redis_.llen(list_name) == 0:
                    url = get_url_redis(list_name)
                    get_url_1(url,self.file)
                else:
                    done_name_value = self.names.get_done_name_value( self.names.get_done_name( self.num-1 ) )
                    if done_name_value=="True":
                        break
                    condition.wait()
                condition.release()
        print("get_thread:"+list_name+" done!")
        print("err url:",err_url)

class Middle_Thread(threading.Thread):
    def __init__(self,fun=None,names=None,num=None):
        threading.Thread.__init__(self)
        self.fun=fun
        self.names=names
        self.num=num


    def run(self):
        print("Middle_Thread start...")
        before_condition=self.names.get_condition(self.num-1)
        before_list_name=self.names.get_list_name(self.num-1)

        after_condition=self.names.get_condition(self.num)
        after_done_name=self.names.get_done_name( self.num )

        while (True):
            if (before_condition.acquire()):
                if not redis_.llen(before_list_name) == 0:
                    name0 = self.names.get_list_name(self.num-1)
                    name1 = self.names.get_list_name(self.num)
                    condition = self.names.get_condition(self.num)
                    while (True):
                        url_0 = get_url_redis(name0)
                        if url_0 is None:
                            break
                        else:
                            urls=middle_url_1(url_0)
                            for url in urls:
                                put_url_redis(name1,url)
                                if (condition.acquire()):
                                    print("middle notify get")
                                    condition.notify_all()
                                    condition.release()
                else:
                    before_done_name_value = self.names.get_done_name_value( self.names.get_done_name( self.num - 1 ) )
                    if before_done_name_value=="True":
                        break
                    before_condition.wait()
                before_condition.release()

        while (True):
            if (after_condition.acquire()):
                redis_.getset(after_done_name, str(True))
                after_condition.notify_all()
                after_condition.release()
                break
        print("get_thread:"+before_list_name + " done!")


class Name_Manager(object):
    condition=[]
    def __init__(self,name,num):
        self.name=name
        self.num=num
        for i in range(num-1):
            self.condition.append( threading.Condition() )

    def create(self):
        redis_.set(self.name,"True")
        for i in range(self.num):
            if not i==0:
                redis_.rpush(self.name+"_list",self.name+"_list_"+str(i))

            redis_.rpush(self.name + "_done", self.name+"_done_"+str(i))
            redis_.set(self.name+"_str_"+str(i),str(False))


    def get_condition(self,num):
        return self.condition[num]


    def get_list_name(self,num):
        return redis_.lindex(self.name+"_list",num)

    def get_done_name(self,num):
        return redis_.lindex(self.name + "_done",num)

    def get_done_name_value(self,name):
        return redis_.get(name)

def put_url_redis(name,url):
    redis_.lpush(name,url)

def get_url_redis(name):
    return redis_.rpop(name)

def check_schedule(names,num,thread):
    '''
    该方法会先到redis中检查传入的names的name是否被创建，若无则创建一个
    然后遍历thread并从Redis中查询其是否已完成，若完成则不启动对应线程

    :param names: NameManager的对象
    :param num: 使用的线程的个数
    :param thread: 使用的线程，要求必须是一个list，且其中的线程必须是按执行的顺序排好

    '''
    if redis_.get(names.name) == "None":
        print("check_schedule create")
        names.create()

    for i in range(num):
        done=names.get_done_name_value(names.get_done_name(i))

        if  done == "True":
            pass
        else:
            if i==0:
                clear_all(names)
                names.create()
                thread[0].start()
            else:
                thread[i].start()

def clear_all(names):
    for key in redis_.keys(names.name+"*"):
        redis_.delete( key )


'''
下面的方法对应着上面三个thread类在实际处理页面HTML的处理
使用方法：将方法放入对应的thread的run方法的相应位置
'''
def put_url_0(url):
    urls = []
    print("put_url_0 run...")
    list=['shengji/','nanjing/','suzhou/','wuxi/','changzhou/','zhenjiang/','nantong/','taizhou/','yangzhou/','yancheng/','huaian/','suqian/','lianyungang/','xuzhou/']
    get_next_page_url(url,urls)
    for i in list:
        i_url = "http://www.ccgp-jiangsu.gov.cn/cgxx/cggg/" +i

        get_next_page_url(i_url,urls)
    print("put_url_0 finsh...")
    return urls

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




#获取各个地区内公告的URLs
def middle_url_1(url):
    print(url)
    urls = []
    print("middle_url_1 start ...")
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    num = re.search("/index", url).span()[0]
    url = url[:num]
    div=soup.find("div",class_="list_list")
    if div is None:
        div=soup.find("div",class_="list_list02")
    for li_tag in div.find_all("li"):

        a_tag = li_tag.find("a")["href"]
        next_url = url + a_tag[1:]
        urls.append(next_url)

    return urls



#获取公告内的详细信息
def get_url_1(url,file):

    print(url + "  start...")
    try:
        html = get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        [s.extract() for s in soup('script')]
        [s.extract() for s in soup('style')]
        title = soup.find("h1").get_text().strip().replace("\n", "")
        date_div = soup.find("div", class_="detail_bz")
        date = date_div.find("span").get_text().strip().replace("\n", "")[6:]
        text = soup.find("div", class_="detail_con").get_text().strip().replace("\n", "")

        file.write(url + "##" + date + "##" + title + "##" + text + "\n")
    except:
        print(url+" has err!")
        err_url.append(url)

def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data



if __name__ == '__main__':
    print("start")
    
    #用法示例
    
    url = "http://www.ccgp-jiangsu.gov.cn/cgxx/cggg/"
    file_path = "C:/file/ResultFile/ccgp-jiangsu_spider_result.txt"

    names=Name_Manager("ccgp-jiangsu",3)
    thread=[]
    f = open(file_path, "a+", encoding="utf-8")

    p=Put_Thread(names=names,num=0,url=url)
    m=Middle_Thread(names=names,num=1)
    g=Get_Thread(names=names,num=2,file=f)

    thread.append(p)
    thread.append( m )
    thread.append( g )
    check_schedule(names,3,thread)


