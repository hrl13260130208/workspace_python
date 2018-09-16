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
        put_url_0(self.names)
        condition=self.names.get_condition(self.num)
        done_name=self.names.get_done_name_value(self.names.get_done_name(self.num))
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
        condition=self.names.get_condition(self.num)
        list_name=self.names.get_list_name(self.num)
        done_name = self.names.get_done_name_value( self.names.get_done_name( self.num ) )
        while (True):
            if (condition.acquire()):
                if not redis_.llen(list_name) == 0:
                    get_url_1(self.names)
                else:
                    if redis_.get(done_name)=="True":
                        break
                    condition.wait()
                condition.release()
        print(list_name+" done!")

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
        before_done_name = self.names.get_done_name_value( self.names.get_done_name( self.num-1 ))
        after_condition=self.names.get_condition(self.num)
        #after_list_name = self.names.get_list_name( self.num)
        after_done_name = self.names.get_done_name_value( self.names.get_done_name( self.num ) )
        while (True):
            if (before_condition.acquire()):
                if not redis_.llen(before_list_name) == 0:
                    middle_url_1(self.names)
                else:
                    if redis_.get(before_done_name)=="True":
                        break
                    before_condition.wait()
                before_condition.release()

        while (True):
            if (after_condition.acquire()):
                redis_.getset(after_done_name, str(True))
                after_condition.notify_all()
                after_condition.release()
                break
        print(before_list_name + " done!")


class Name_Manager(object):
    condition=[]
    def __init__(self,name,num):
        self.name=name
        self.num=num

    def create(self):
        for i in range(self.num):
            redis_.lpush(self.name+"_list",self.name+"_list_"+str(i))
            redis_.lpush(self.name + "_done", self.name+"_str_"+str(i))
            redis_.set(self.name+"_str_"+str(i),str(False))
            self.condition.append(threading.Condition())

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

def check_schedule(names,num):
    for i in range(num):
        done=names.get_done_name_value(names.get_done_name(num))

        if  done == "True":
            pass
        else:
            if num==0:
                clear_all()
            else:
                pass




def clear_all():
    for key in redis_.keys(names.name+".*"):
        redis_.delete( key )


#获取各个地区对应的URLs
def put_url_0(names):
    for i in range(5):
        put_url_redis("t0_"+str(i),names.get_list_name(0))
    print("url_0:",redis_.lrange(names.get_list_name(0),0,redis_.llen(names.get_list_name(0))))


#获取各个地区内公告的URLs
def middle_url_1(names):
    while(True):
        name0=get_url_redis(names.get_list_name(0))
        if name0 ==None:
            break
        for i in range(5):
            put_url_redis(name0+"_t1_"+str(i),names.get_list_name(1))

        print("m_url_1:",redis_.lrange(names.get_list_name(0),0,redis_.llen(names.get_list_name(0))))
        print("m_url_1",redis_.lrange(names.get_list_name(1),0,redis_.llen(names.get_list_name(1))))


#获取公告内的详细信息
def get_url_1(names):
    while (True):
        name1 = get_url_redis( names.get_list_name( 1) )
        if name1 ==None:
            break
        print("g_url_1",name1)
        print("g_url_1",redis_.lrange( names.get_list_name( 1 ), 0, redis_.llen( names.get_list_name( 1 ) ) ) )



if __name__ == '__main__':
    url = "http://cz.fjzfcg.gov.cn/3500/openbidlist/f9ebc6637c3641ee9017db2a94bfe5f0/"

    names=Name_Manager("t1",2)
    names.create()

    put_url_0(names)
    middle_url_1(names)
    get_url_1(names)

    '''
    p=Put_Thread(names=names,num=0,url=url)

    m=Middle_Thread(names=names,num=1)

    g=Get_Thread(names=names,num=1)

    p.start()
    m.start()
    g.start()

    p.join()
    m.join()
    g.join()

'''
