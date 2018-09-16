#!/usr/bin/env python
# coding=utf-8


import requests
import threading
from bs4 import BeautifulSoup
import time
import redis


redis_ = redis.Redis(host="127.0.0.1",port=6379,decode_responses=True)

class Put_Thread(threading.Thread):
    def __init__(self,url=None,names=None,num=None):
        threading.Thread.__init__(self)
        self.names=names
        self.num=num
        self.url=url

    def run(self):
        print("Put_Thread start...")
        put_url_0(self.url,self.names)
        condition=self.names.get_condition(self.num)
        done_name=self.names.get_done_name(self.num)

        while (True):
            if (condition.acquire()):
                redis_.getset(done_name,str(True))
                condition.notify_all()
                condition.release()
                break

class Get_Thread(threading.Thread):
    def __init__(self,fun=None,names=None,num=None):
        threading.Thread.__init__(self)
        self.fun=fun
        self.names=names
        self.num=num

    def run(self):
        print("Get_Thread start...")
        condition=self.names.get_condition(self.num-1)
        list_name=self.names.get_list_name(self.num-1)


        while (True):
            if (condition.acquire()):

                if not redis_.llen(list_name) == 0:
                    get_url_1(self.names)
                else:
                    done_name_value = self.names.get_done_name_value( self.names.get_done_name( self.num ) )
                    if done_name_value=="True":
                        break
                    condition.wait()
                condition.release()
        print("get_thread:"+list_name+" done!")

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
        #after_list_name = self.names.get_list_name( self.num)
        after_done_name=self.names.get_done_name( self.num )
        after_done_name_value = self.names.get_done_name_value( self.names.get_done_name( self.num ) )
        while (True):
            if (before_condition.acquire()):

                if not redis_.llen(before_list_name) == 0:
                    middle_url_1(self.names,self.num)
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
        redis_.set(names.name,"True")
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

def put_url_redis(url,name):
    redis_.lpush(name,url)
    #print(url)

def get_url_redis(name):
    return redis_.rpop(name)

def check_schedule(names,num,thread):
    if redis_.get(names.name) == "None":
        print("check_schedule create")
        names.create()

    for i in range(num):
        done=names.get_done_name_value(names.get_done_name(i))

        if  done == "True":
            pass
        else:
            if i==0:
                clear_all()
                names.create()
                thread[0].start()
            else:
                thread[i].start()



def clear_all():
    for key in redis_.keys(names.name+"*"):
        redis_.delete( key )


#获取各个地区对应的URLs
def put_url_0(url,names):
    print("put_url_0 run...")
    html=get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    for ul_tag in soup.find_all("ul", class_="nav-second-level"):
        for a_tag in ul_tag.find_all("a", class_="zc"):
            codes = a_tag["codes"]
            name = a_tag.get_text()
            new_url = "http://cz.fjzfcg.gov.cn/3500/openbidlist/f9ebc6637c3641ee9017db2a94bfe5f0/" + "?zone_code=" + \
                      codes + "&zone_name=" + name
            put_url_redis(new_url,names.get_list_name(0))
    print( "put_url_0 run complete!" )

#获取各个地区内公告的URLs
def middle_url_1(names,num):
    print( "middle_url_ run..." )
    name0=names.get_list_name(0)
    name1=names.get_list_name(1)
    condition=names.get_condition(num)
    while(True):
        url_0=get_url_redis(name0)
        if url_0 is None:
            break
        else:
            page_url=url_0
            while (True):
                f_html = get_html(page_url)
                get_detail_url(f_html,name1)
                num = get_next_page(f_html)
                if not num is None:
                    page_url = url_0 + "&page=" + str(num)
                else:
                    break
                if (condition.acquire()):
                    print("middle notify get")
                    condition.notify_all()
                    condition.release()

#获取公告内的详细信息
def get_url_1(names):
    print( "get_url_1 run..." )
    name1=names.get_list_name(1)

    s_url = get_url_redis(name1)
    print(s_url)
    s_html = get_html(s_url)
    date = get_date(s_html)
    print(date)
    title = get_title(s_html)
    print(title)
    text = get_text(s_html)
    print(text)

def get_date(html):
    soup = BeautifulSoup( html, "html.parser" )
    span=[]
    for div_tag in soup.find_all("div",class_="clearfix"):
        span = div_tag.find_all("span")
    return span[2].get_text()

def get_title(html):
    soup = BeautifulSoup( html, "html.parser" )
    return soup.find_all("h2")[0].get_text()

def get_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.find_all("div",class_="notice-con")[0].get_text().strip().replace("\n", "")

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

def get_detail_url(html,name):

    soup = BeautifulSoup(html, "html.parser")
    for table in soup.find_all("table"):
        for a_tag in table.find_all("a"):
            print("put datail url")
            put_url_redis("http://cz.fjzfcg.gov.cn"+a_tag["href"],name)

def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data




if __name__ == '__main__':
    url = "http://cz.fjzfcg.gov.cn/3500/openbidlist/f9ebc6637c3641ee9017db2a94bfe5f0/"

    names=Name_Manager("t1",3)
    thread=[]

    p=Put_Thread(names=names,num=0,url=url)
    m=Middle_Thread(names=names,num=1)
    g=Get_Thread(names=names,num=2)

    thread.append(p)
    thread.append( m )
    thread.append( g )
    check_schedule(names,3,thread)


