

import threading
import logging
import traceback
import os
import spider.spider_modules.name_manager as nm
import datetime
import time

logger=logging.getLogger("logger")
class StandardSpider(threading.Thread):

    def get(self,url):
        pass

    def run(self):
        pass

class attr:
    def __init__(self,names,step):
        self.names = names
        # 标识线程是否是起始或结束线程
        self.start_thread = False
        self.end_thread = False
        self.step=step

    def is_start_thread(self):
        return self.start_thread

    def set_start_thread(self):
        self.start_thread = True

    def is_end_thread(self):
        return self.end_thread

    def set_end_thread(self):
        self.end_thread = True




class ThreadingSpider(StandardSpider):

    def __init__(self,nm,attr):
        threading.Thread.__init__(self)
        self.attr=attr
        self.nm=nm
        self.url_increment=increment(self.nm)

    def run(self):
        logger.info("thread \'" + self.__class__.__name__ + "\' run as " + self.getName() + " ...")

        if self.attr.is_end_thread():
            self.check_file()
        while (True):
            url_0 = ""
            if not self.attr.is_start_thread():
                if self.nm.has_next(self.attr.step):
                    url_0 = self.nm.get_url_redis(self.attr.step)
                else:
                    if self.is_previous_done():
                        break
                    else:
                        logger.info("当前任务已完成，等待新任务...")
                        time.sleep(10)
                        continue
            try:
                logger.info("run url :"+url_0)
                urls = self.get(url_0)

            except BaseException as e:
                logger.error(self.getName()+" - "+url_0,exc_info = True)
                logger.info("thread \'" + self.__class__.__name__ + "\' of " + self.getName()+" has err!!! get back!!!")
                self.nm.put_url_redis(self.attr.step,url_0)
                continue

            if  self.attr.is_end_thread():
                self.write(urls)
            else:
                self.put_urls(urls)

            if self.attr.is_start_thread():
                break

        if  self.attr.is_end_thread():
            logger.info("thread \'" + self.__class__.__name__ + "\' of " + self.getName()+ " all finsh!!!")

        self.nm.set_done_name(self.attr.step, True)

    def write(self,urls):
        self.file.write(self.nm.name+"##"+urls)


    def is_previous_done(self):
        '''
        判断上一步的线程是否已完成
        :return:
        '''

        return self.nm.get_done_value(self.attr.step-1) == "True"


    def put_urls(self,urls):
        '''
        遍历urls将其放入redis中，然后唤醒下一步的线程
        :param urls:
        :return:
        '''
        for url in urls:
            self.nm.put_url_redis(self.attr.step+1, url)


    def check_file(self):
        file_path_ = "C:/SpiderResultFile/"
        file_path = "C:/SpiderResultFile/" + self.nm.name
        file_name = "part-"
        file_num = 0
        if not os.path.exists(file_path):
            if not os.path.exists(file_path_):
                os.mkdir(file_path_)
            os.mkdir(file_path)
        else:
            list = os.listdir(file_path)
            file_num = list.__len__()
        self.file = open(file_path + "/" + file_name + str(file_num).zfill(4), "a+", encoding="utf-8")

class increment():
    def __init__(self,names):
        self.nm=names
        self.format="%Y-%m-%d"
        self.default_date="2018-12-01"
        self.current_date=None
        self.last_date=None

    def get_date(self):
        ld = self.nm.get_last_date()
        if ld == None:
            self.last_date = datetime.datetime.strptime(self.default_date, self.format)
        else:
            self.last_date = datetime.datetime.strptime(ld, self.format)

    def is_increment(self,url,date):
        '''
            判断所传的url是否是增量，会按照传入的日期判断
        :param url:
        :param date: 日期格式为：XXXX-XX-XX
        :return:
        '''

        if self.last_date ==None:
            self.get_date()
        url_date=datetime.datetime.strptime(date,self.format)
        if url_date>=self.last_date:
            result=self.nm.is_increment(url)
            if result :
                if self.current_date == None:
                    self.current_date = url_date
                if url_date > self.current_date:
                    self.current_date = url_date
            return  result
        else:
            return False

    def date_check(self):
        if self.current_date != None:
            while True:
                if self.nm.get_lock():
                    condition_date_str=self.nm.get_last_date()
                    if condition_date_str == None:
                        condition_date = datetime.datetime.strptime(self.default_date, self.format)
                    else:
                        condition_date = datetime.datetime.strptime(condition_date_str, self.format)
                    if self.current_date>condition_date:
                        if self.current_date>datetime.datetime.now():
                            self.current_date=datetime.datetime.now()
                        self.nm.set_last_date(str(self.current_date.date()))
                    self.nm.release_lock()
                    break
                else:
                    time.sleep(1)

if __name__ == '__main__':
    print(datetime.datetime.now())



