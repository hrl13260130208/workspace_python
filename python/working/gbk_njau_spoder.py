#!/usr/bin/env python
# coding=utf-8


import requests
import threading
from bs4 import BeautifulSoup
import re
import redis

'''
此爬虫使用了redis和生产者消费者模式，程序执行方式如下：
    首先启动一个put_thread，其需要一个初始页面的url、管理name的names对象、表示第几层的num
        put_thread会从初始页面获取下一级需要的url，并将其放到redis中
    然后如果put_thread生产的url就是内容页面，则创建一个get_thread（从内容页爬取数据）
        否则启动一个middle_thread，从上一个url中获取下一个url中并存入redis中
        
    锁机制和命名机制：两个线程之间通过锁来进行相互间的等待和唤醒。命名机制：初始化的时候会创建
    一个_done和一个_list的列表，存储所有需要的名称（一个表示线程是否完成的值的名称，一个产生
    的url的存储列表的名称）

中途退出处理：如果程序因为各种原因退出，重新启动程序时，其会到redis中去查询上次爬取的进度，然后接着之前的继续爬取




'''
redis_ = redis.Redis(host="127.0.0.1",port=6379,decode_responses=True)

class Put_Thread(threading.Thread):
    '''
    构造方法：url 爬取路径
    names NameManager对象
    num 执行顺序从0开始（该对象一般为0）
    '''
    def __init__(self,url=None,names=None,num=None):
        threading.Thread.__init__(self)
        self.names=names
        self.num=num
        self.url=url

    def run(self):
        '''

        获取页面信息、存入redis中
        需要单独实现获取页面信息的方法
        :return:
        '''
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

    def __init__(self,  names=None, num=None, file=None):
        '''
        构造方法：  names NameManager对象
        num  线程的执行顺序从0开始
        file 写入的文件对象

        '''
        threading.Thread.__init__(self)
        self.names = names
        self.num = num
        self.file = file

    def run(self):
        '''
        从redis中获取url，从URL中获取页面信息，存入文件中
        需要单独实现获取页面信息的方法和写入文件

        :return:
        '''
        print("Get_Thread start...")
        condition=self.names.get_condition(self.num-1)
        list_name=self.names.get_list_name(self.num-1)


        while (True):
            if (condition.acquire()):

                if not redis_.llen(list_name) == 0:
                    url = get_url_redis(list_name)
                    get_url_1(url,self.file)
                else:
                    done_name_value = self.names.get_done_name_value( self.names.get_done_name( self.num ) )
                    if done_name_value=="True":
                        break
                    condition.wait()
                condition.release()
        print("get_thread:"+list_name+" done!")

class Middle_Thread(threading.Thread):
    def __init__(self, names=None, num=None):
        '''
         构造方法：  names NameManager对象
                    num  线程的执行顺序从0开始
        :param names:
        :param num:
        '''
        threading.Thread.__init__(self)
        self.names = names
        self.num = num


    def run(self):
        '''
        从redis中获取上一级的url
        然后获取页面里的下一级的url（需要单独实现方法为：middle_url_1(url_0)）
        然后将其放到redis中

        :return:
        '''
        print("Middle_Thread start...")
        before_condition = self.names.get_condition(self.num - 1)
        before_list_name = self.names.get_list_name(self.num - 1)

        after_condition = self.names.get_condition(self.num)
        after_done_name = self.names.get_done_name(self.num)

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
                            urls = middle_url_1(url_0)
                            for url in urls:
                                put_url_redis(name1, url)
                                if (condition.acquire()):
                                    print("middle notify get")
                                    condition.notify_all()
                                    condition.release()
                else:
                    before_done_name_value = self.names.get_done_name_value(self.names.get_done_name(self.num - 1))
                    if before_done_name_value == "True":
                        break
                    before_condition.wait()
                before_condition.release()

        while (True):
            if (after_condition.acquire()):
                redis_.getset(after_done_name, str(True))
                after_condition.notify_all()
                after_condition.release()
                break
        print("get_thread:" + before_list_name + " done!")


class Name_Manager(object):
    '''
    负责管理每一个线程向redis中存入数据的名称与线程之间的锁（condition对象）

    '''
    condition=[]

    def __init__(self,name,num):
        '''

        :param name: 整爬虫的名称
        :param num:  整爬虫的线程数
        '''
        self.name=name
        self.num=num
        for i in range(num-1):
            self.condition.append( threading.Condition() )

    def create(self):
        '''
        在redis中创建爬虫需要的名称

        :return:
        '''
        redis_.set(self.name,"True")
        for i in range(self.num):
            if not i==0:
                redis_.rpush(self.name+"_list",self.name+"_list_"+str(i))

            redis_.rpush(self.name + "_done", self.name+"_done_"+str(i))
            redis_.set(self.name+"_done_"+str(i),str(False))


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
    当程序重新启动的时候，检查之前程序爬取的进度，然后根据其进度启动对应的线程

    :param names: NameManager对象
    :param num: 线程数
    :param thread: 包含所有线程的list
    :return:
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
    '''
    清除对应names在redis中的数据
    :param names:
    :return:
    '''
    for key in redis_.keys(names.name+"*"):
        redis_.delete( key )


'''
下面的方法对应着上面三个thread类在实际处理页面HTML的处理
使用方法：直接编写方法，对应线程会调用该方法，put和middle需要返回一个包含url的list
'''
def put_url_0(url):
    urls=[]
    urls_t=["http://zbb.njau.edu.cn/pgoods","http://zbb.njau.edu.cn/pservices","http://zbb.njau.edu.cn/pprojects","http://zbb.njau.edu.cn/pquick"]

    for url in urls_t:
        html = get_html(url + "/index.jhtml")

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup.find_all("div", class_="lpage"):
            tt = tag.get_text()
            n = re.search("/.*页", tag.get_text()).span()
            num = tt[n[0] + 1:n[1] - 1]
            for i in range(int(num)):
                if i == 0:
                    urls.append(url + "/index.jhtml")
                else:
                    urls.append(url + "/index_" + str(i + 1) + ".jhtml")
    return urls


#获取各个地区内公告的URLs
def middle_url_1(url):
    print("m_u_1 start...")
    urls=[]
    html = get_html(url)

    soup = BeautifulSoup(html, "html.parser")

    dl_tag = soup.find("dl", class_="llist")
    for dd_tag in dl_tag.find_all("dd", cid="4"):
        url = dd_tag.find("a")["href"]
        urls.append(url)
    return urls





#获取公告内的详细信息
def get_url_1(url,file):
    print("g_u_1 start...")
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("div", class_="lright cright")
    ctitle = tag.find("div", class_="ctitle")
    text = tag.find_all(attrs={'class': 'ccontent'})[0].get_text().strip()
    title = tag.find("h1").get_text()
    date = ctitle.find("i").get_text().strip()[6:]
    text = "".join(text.split())
    line=url+"##"+date+"##"+title+"##"+text
    file.write(str(line.encode('gbk',errors="ignore")).replace("b'",'').replace("'",'')+ '\n')



def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data


if __name__ == '__main__':
    print("start")

    url = " "
    file_path = "C:/file/ResultFile/njau_spider_result.txt"

    names=Name_Manager("njau",3)
    thread=[]
    f = open(file_path, "a+")

    p=Put_Thread(names=names,num=0,url=url)
    m=Middle_Thread(names=names,num=1)
    g=Get_Thread(names=names,num=2,file=f)

    thread.append(p)
    thread.append( m )
    thread.append( g )
    check_schedule(names,3,thread)


