

import threading
import logging
import traceback
import os

logger=logging.getLogger("spiderlog")
logger.setLevel(logging.INFO)
fh=logging.FileHandler("C:/File/ResultFile/spider.log")
ch=logging.StreamHandler()

log_file=open("C:/File/ResultFile/spider.log","a+",encoding="utf-8")
fh.setLevel(logging.ERROR)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)



class StandardSpider(threading.Thread):

    def get(self,url):
        pass

    def run(self):
        pass


class ThreadSpider(StandardSpider):

    def run(self):
        url=self.r_get()
        urls=self.get(url)
        self.r_put(urls)



class ThreadingSpider(StandardSpider):

    def __init__(self,names):
        threading.Thread.__init__(self)
        self.names=names



    def set_parm(self):
        if self.num==-1:
            print("请设置线程的顺序标识数字")

        if not self.is_start_thread():
            self.set_get_condition()
            self.set_get_done_name()
            self.set_get_list_name()

        if not self.is_end_thread():
            self.set_put_condition()
            self.set_put_done_name()
            self.set_put_list_name()

    #标识线程是否是起始或结束线程
    start_thread=False
    end_thread=False

    def is_start_thread(self):
        return self.start_thread

    def set_start_thread(self):
        self.start_thread = True

    def is_end_thread(self):
        return self.end_thread

    def set_end_thread(self):
        self.end_thread = True


    #在redis中存储url的list的名称
    put_list_name=""
    get_list_name=""

    def set_put_list_name(self):
        self.put_list_name=self.names.get_list_name(self.num)

    def set_get_list_name(self):
        self.get_list_name=self.names.get_list_name(self.num-1)


    #线程之间的锁
    put_condition=None
    get_condition=None

    def set_put_condition(self):
        self.put_condition=self.names.get_condition(self.num)

    def set_get_condition(self):
        self.get_condition=self.names.get_condition(self.num-1)

    #标识线程是否已完成的值
    put_done_name=""
    get_done_name=""

    def set_put_done_name(self):
        self.put_done_name = self.names.get_done_name(self.num)

    def set_get_done_name(self):
        self.get_done_name = self.names.get_done_name(self.num-1)

    def change_put_done_name(self,bool):
        self.names.set_done_name(self.put_done_name,bool)

    #设定将爬虫结果写入的文件
    file=""
    def set_file(self,file):
        self.file=file

    #设定爬虫线程的执行顺序
    num=-1
    def set_num(self,num):
        self.num=num

    url=""

    def run(self):
        self.set_parm()
        logger.info("run thread num : "+str(self.num))

        if self.is_end_thread():
            self.check_file(self.names)
        if self.is_start_thread():
            self.run_start_put()
        else:
            while (True):
                if (self.get_condition.acquire()):
                    if self.names.has_next(self.get_list_name):
                        url_0 = self.names.get_url_redis(self.get_list_name)
                        try:
                            logger.info( "threading "+str(self.num)+" get runing ...")
                            urls = self.get(url_0)
                            logger.info("threading "+str(self.num)+" get run finsh!!!")
                        except BaseException as e:
                            logger.error(url_0)
                            logger.error(e)
                            traceback.print_exc(file=log_file)

                            logger.info("has err!!! get back!!!")
                            self.names.put_url_redis(self.get_list_name,url_0)

                        if not self.is_end_thread():
                            self.put_urls(urls)
                    else:
                        if self.is_previous_done():
                            break
                        self.get_condition.wait()
                    self.get_condition.release()

        if not self.is_end_thread():
            self.done_put_notify()
        else:
            logger.info("all finsh!!!")
            self.change_put_done_name(True)

    def is_previous_done(self):
        '''
        判断上一步的线程是否已完成
        :return:
        '''
        get_done_name_value = self.names.get_done_name_value(self.get_done_name)
        return get_done_name_value == "True"


    def put_urls(self,urls):
        '''
        遍历urls将其放入redis中，然后唤醒下一步的线程
        :param urls:
        :return:
        '''
        for url in urls:
            self.names.put_url_redis(self.put_list_name, url)
        self.put_notifiy()

    class NotifyThread(threading.Thread):
        def __init__(self, condition):
            threading.Thread.__init__(self)
            self.condition=condition

        def run(self):
            if (self.condition.acquire()):
                self.condition.notify()
                self.condition.release()

    def put_notifiy(self):
        '''
        唤醒下一步的线程
        :return:
        '''
        logger.info("threading " + str(self.num) + " notify next thread!!!")
        self.NotifyThread(self.put_condition).start()

    def done_put_notify(self):
        '''
        线程完成，将redis中的标识（done_name）的值设为True，然后唤醒下一步的线程
        :return:
        '''
        while (True):
            if (self.put_condition.acquire()):
                logger.info("thread " + str(self.num) + " finsh! notify next thread!!!")
                self.change_put_done_name(True)
                self.put_condition.notify_all()
                self.put_condition.release()
                break

    def run_start_put(self):
        '''
        获取页面信息、存入redis中
        需要单独实现获取页面信息的方法
        :return:
        '''
        logger.info("threading "+str(self.num)+" start...")
        urls = self.get(self.url)
        for put_url in urls:
            self.names.put_url_redis(self.put_list_name, put_url)

    def check_file(self, names):
        file_path_ = "C:/SpiderResultFile/"
        file_path = "C:/SpiderResultFile/" + names.name
        file_name = "part-"
        file_num = 0
        if not os.path.exists(file_path):
            if not os.path.exists(file_path_):
                os.mkdir(file_path_)
            os.mkdir(file_path)
        else:
            list = os.listdir(file_path)
            file_name = list.__len__()
        self.file = open(file_path + "/" + file_name + str(file_name).zfill(4), "a+", encoding="utf-8")

