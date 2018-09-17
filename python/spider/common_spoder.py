#!/usr/bin/env python
# coding=utf-8


import requests
import threading
from bs4 import BeautifulSoup
import time
import redis

'''
此爬虫使用了redis和生产者消费者模式，程序执行方式如下：
    首先启动一个put_thread，其需要一个初始页面的url、管理name的names对象、表示第几层的num
        put_thread会从初始页面获取下一级需要的url，并将其放到redis中
    然后如果put_thread生产的url就是内容页面，则创建一个get_thread（从内容页爬取数据）
        否则启动一个middle_thread，从上一个url中获取下一个url中并存入redis中

中途退出处理：如果程序因为各种原因退出，重新启动程序时，其会到redis中去查询上次爬取的进度，然后接着之前的继续爬取




'''
redis_ = redis.Redis(host="127.0.0.1",port=6379,decode_responses=True)

class Put_Thread(threading.Thread):
    def __init__(self,url=None,names=None,num=None):
        threading.Thread.__init__(self)
        self.names=names
        self.num=num
        self.url=url

    def run(self):
        print("Put_Thread start...")
        urls=put_url_0(self.url,self.names)
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
                    url = get_url_redis(list_name)
                    get_url_1(url)
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
        after_done_name=self.names.get_done_name( self.num )

        while (True):
            if (before_condition.acquire()):
                if not redis_.llen(before_list_name) == 0:
                    name0 = self.names.get_list_name(0)
                    name1 = self.names.get_list_name(1)
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
def put_url_0(url,names):
    print("请编写方法")


#获取各个地区内公告的URLs
def middle_url_1(names,num):
    print("请编写方法")


#获取公告内的详细信息
def get_url_1(names):
    print("请编写方法")





if __name__ == '__main__':
    print("start")


    '''
    
    #用法示例
    
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

'''
