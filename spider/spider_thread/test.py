from concurrent.futures import  ThreadPoolExecutor,as_completed,Future
import requests
from bs4 import  BeautifulSoup
import spider.spider_modules.standard_spider as ss
import spider.spider_modules.name_manager as nm
import spider.spider_modules.job as job
import re
import time



def get_html(url):
    data = requests.get( url )
    data.encoding = 'utf-8'
    data = data.text
    return data

class first(ss.ThreadingSpider):

    def get(self,url):
        urls = []
        for i in range(1000):
            urls.append(i)
        return urls

class second(ss.ThreadingSpider):

    def get(self,url):
        urls = []
        for i in range(1000):
            urls.append(str(url)+"_"+str(i))
        return urls


class thrid(ss.ThreadingSpider):
    def get(self,url):

        line=url+"_th"
        return line


if __name__ == '__main__':


    j = job.Job("test8")
    j.set_speed()
    j.submit("first","second","thrid",pyname="test")


'''

class tt(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("hello: " )
        time.sleep(100)

def sayhello(a):
    print("hello: "+a)
    time.sleep(2)

if __name__ == '__main__':
    seed = ["a", "b", "c"]
    start1 = time.time()
    for each in seed:
        sayhello(each)
    end1 = time.time()
    print("time1: " + str(end1 - start1))
    start2 = time.time()
    with ThreadPoolExecutor(3) as executor:
        for each in seed:
            f=executor.submit(sayhello,each)
            print(f.result())


    end2 = time.time()
    print("time2: " + str(end2 - start2))
    start3 = time.time()
    with ThreadPoolExecutor(3) as executor1:
        executor1.map(sayhello,each)
    end3 = time.time()
    print("time3: " + str(end3 - start3))
    
f=__import__("spider_modules.spider_thread.fpo",fromlist=True)

first=getattr(f,"first")
#print(first())
di={}

di.setdefault(di.__len__(),"sfsf")
di.setdefault(di.__len__(),"dfsdf")
di.setdefault(di.__len__(),"sdfsdf")
di.setdefault(di.__len__(),"dsfsdf")
print(di)
for i in di:
    print(i)

#threads=getattr(f,"first")

'''
