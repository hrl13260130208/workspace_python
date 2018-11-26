

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

class attr:
    def __init__(self,names):
        self.names = names
        # 标识线程是否是起始或结束线程
        self.start_thread = False
        self.end_thread = False
        # 在redis中存储url的list的名称
        self.put_list_name = ""
        self.get_list_name = ""
        # 线程之间的锁
        self.put_condition = None
        self.get_condition = None
        # 标识线程是否已完成的值
        self.put_done_name = ""
        self.get_done_name = ""


    def is_start_thread(self):
        return self.start_thread

    def set_start_thread(self):
        self.start_thread = True

    def is_end_thread(self):
        return self.end_thread

    def set_end_thread(self):
        self.end_thread = True

    def set_put_list_name(self,num):
        self.put_list_name=self.names.get_list_name(num)

    def get_put_list_name(self):
        return self.put_list_name

    def set_get_list_name(self,num):
        self.get_list_name=self.names.get_list_name(num-1)

    def get_get_list_name(self):
        return self.get_list_name

    def set_put_condition(self,num):
        self.put_condition=self.names.get_condition(num)

    def set_get_condition(self,num):
        self.get_condition=self.names.get_condition(num-1)

    def get_put_condition(self):
       return self.put_condition

    def get_get_condition(self):
       return self.get_condition

    def set_put_done_name(self,num):
        self.put_done_name = self.names.get_done_name(num)

    def set_get_done_name(self,num):
        self.get_done_name = self.names.get_done_name(num-1)

    def get_put_done_name(self):
        return  self.put_done_name

    def get_get_done_name(self):
        return  self.get_done_name




class ThreadingSpider(StandardSpider):

    def __init__(self,names,attr):
        threading.Thread.__init__(self)
        self.attr=attr
        self.names=names

    def run(self):
        logger.info("thread \'" + self.__class__.__name__ + "\' run as " + self.getName() + " ...")

        if self.attr.is_end_thread():
            self.check_file(self.names)
        while (True):
            url_0 = ""
            if not self.attr.is_start_thread():
                if self.names.has_next(self.attr.get_get_list_name()):
                    url_0 = self.names.get_url_redis(self.attr.get_get_list_name())
                else:
                    if self.is_previous_done():
                        break
                    self.attr.get_get_condition().acquire()
                    self.attr.get_get_condition().wait()
                    continue
            try:
                urls = self.get(url_0)

            except BaseException as e:
                logger.error(self.getName()+" - "+url_0)
                logger.error(e)
                traceback.print_exc(file=log_file)

                logger.info("thread \'" + self.__class__.__name__ + "\' of " + self.getName()+" has err!!! get back!!!")
                self.names.put_url_redis(self.attr.get_get_list_name(),url_0)
                continue

            if  self.attr.is_end_thread():
                self.write(urls)
            else:
                self.put_urls(urls)

            if self.attr.is_start_thread():
                break

        if not self.attr.is_end_thread():
            self.done_put_notify()
        else:
            logger.info("thread \'" + self.__class__.__name__ + "\' of " + self.getName()+ " all finsh!!!")
            self.change_put_done_name(True)
            self.notify_main()


    def write(self,urls):
        self.file.write(urls)

    def change_put_done_name(self, bool):
        self.names.set_done_name(self.attr.get_put_done_name(), bool)

    def is_previous_done(self):
        '''
        判断上一步的线程是否已完成
        :return:
        '''
        get_done_name_value = self.names.get_done_name_value(self.attr.get_get_done_name())
        return get_done_name_value == "True"


    def put_urls(self,urls):
        '''
        遍历urls将其放入redis中，然后唤醒下一步的线程
        :param urls:
        :return:
        '''
        for url in urls:
            self.names.put_url_redis(self.attr.get_put_list_name(), url)
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
        self.NotifyThread(self.attr.get_put_condition()).start()

    def done_put_notify(self):
        '''
        线程完成，将redis中的标识（done_name）的值设为True，然后唤醒下一步的线程
        :return:
        '''
        while (True):
            if (self.attr.get_put_condition().acquire()):
                logger.info("thread \'" + self.__class__.__name__ + "\' of " + self.getName()+ " finsh! notify next thread!!!")
                self.change_put_done_name(True)
                self.attr.get_put_condition().notify_all()
                self.attr.get_put_condition().release()
                break

        self.notify_main()

    def notify_main(self):
        '''
        唤醒主线程
        :return:
        '''
        while (True):
            if (self.names.get_mian_condition().acquire()):
                logger.info("thread \'" + self.__class__.__name__ + "\' of " + self.getName()+ " finsh! notify main thread!!!")
                self.names.get_mian_condition().notify_all()
                self.names.get_mian_condition().release()
                break


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
            file_num = list.__len__()
        self.file = open(file_path + "/" + file_name + str(file_num).zfill(4), "a+", encoding="utf-8")

